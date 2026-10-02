"""Validate this plugin and create a relocatable ZIP using the standard library."""
import json
import re
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

ROOT = Path(__file__).resolve().parents[1]


def check(condition, message):
    if not condition:
        raise ValueError(message)


def validate(root):
    manifest = json.loads((root / "plugin.json").read_text(encoding="utf-8"))
    overlay = json.loads((root / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
    catalog = json.loads((root / ".agents/plugins/marketplace.json").read_text(encoding="utf-8"))
    check(manifest["name"] == overlay["name"], "Plugin names differ")
    check(manifest["version"] == overlay["version"], "Plugin versions differ")
    check(manifest["extensions"]["com.openai"]["interface"] == overlay["interface"],
          "Plugin interfaces differ")
    entry, = catalog["plugins"]
    check(entry["name"] == manifest["name"], "Marketplace name differs")
    check(entry["source"] == {"source": "local", "path": "./"}, "Invalid local source")
    check(overlay["skills"] == "./skills/", "Invalid skills directory")
    skills = sorted((root / "skills").glob("*/SKILL.md"))
    check(len(skills) == 5, "Expected five skills")
    for skill in skills:
        text = skill.read_text(encoding="utf-8")
        match = re.match(r"^---\nname: ([a-z0-9-]+)\ndescription: ([^\n]+)\n---\n", text)
        check(match is not None, f"Invalid frontmatter: {skill}")
        check(match[1] == skill.parent.name and len(match[1]) <= 64,
              f"Invalid skill name: {skill}")
        check(len(match[2]) <= 1024, f"Description too long: {skill}")
    for doc in root.rglob("*.md"):
        text = doc.read_text(encoding="utf-8")
        check(len(text.splitlines()) <= 300, f"Over 300 lines: {doc}")
        check("\ufffd" not in text, f"Invalid encoding: {doc}")
        for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
            if target.startswith(("https://", "http://", "#")):
                continue
            resolved = (doc.parent / target.split("#")[0]).resolve()
            check(resolved.is_relative_to(root.resolve()) and resolved.exists(),
                  f"Broken or external local reference: {doc}: {target}")
    return manifest


def main():
    manifest = validate(ROOT)
    output = ROOT / "dist" / f'{manifest["name"]}-{manifest["version"]}-codex.zip'
    output.parent.mkdir(exist_ok=True)
    paths = [ROOT / name for name in ("plugin.json", "AGENTS.md", "README.md", "CHANGELOG.md")]
    for name in (".codex-plugin", ".agents", "skills", "shared", "adapters", "validation", "scripts", "tests"):
        paths.extend(path for path in (ROOT / name).rglob("*")
                     if path.is_file() and "__pycache__" not in path.parts)
    with ZipFile(output, "w", ZIP_DEFLATED) as archive:
        for path in sorted(paths):
            archive.write(path, f'{manifest["name"]}/{path.relative_to(ROOT).as_posix()}')
    # ponytail: fixed package folders; add an explicit folder when the package gains resources.
    print(f"Validated five skills; packaged {len(paths)} files: {output}")


if __name__ == "__main__":
    main()
