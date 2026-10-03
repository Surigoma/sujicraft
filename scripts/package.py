"""Validate this plugin and create a relocatable ZIP using the standard library."""
import json
import re
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_SKILLS = {
    "commit-message",
    "document-review",
    "engineering-code",
    "engineering-design",
    "engineering-review",
    "plugin-maintenance",
    "ui-design-review",
}


def check(condition, message):
    if not condition:
        raise ValueError(message)


def validate(root):
    manifest = json.loads((root / "plugin.json").read_text(encoding="utf-8"))
    overlay = json.loads((root / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
    claude = json.loads((root / ".claude-plugin/plugin.json").read_text(encoding="utf-8"))
    for field in ("name", "version", "description"):
        check(manifest[field] == claude[field], f"Claude plugin {field} differs")
    check(claude["skills"] == "./skills/", "Invalid Claude skills directory")
    claude_catalog = json.loads((root / ".claude-plugin/marketplace.json").read_text(encoding="utf-8"))
    claude_entry, = claude_catalog["plugins"]
    check(claude_catalog["name"] == "sujicraft", "Claude marketplace name differs")
    check(claude_entry["name"] == manifest["name"], "Claude marketplace plugin differs")
    check(claude_entry["source"] == "./", "Invalid Claude marketplace source")
    grok_catalog = json.loads((root / ".grok-plugin/marketplace.json").read_text(encoding="utf-8"))
    grok_entry, = grok_catalog["plugins"]
    check(grok_entry["name"] == manifest["name"], "Grok marketplace plugin differs")
    check(grok_entry["source"] == {
        "source": "url", "url": "https://github.com/Surigoma/sujicraft.git", "ref": "main"
    }, "Invalid Grok marketplace source")
    catalog = json.loads((root / ".agents/plugins/marketplace.json").read_text(encoding="utf-8"))
    check(manifest["name"] == overlay["name"], "Plugin names differ")
    check(manifest["version"] == overlay["version"], "Plugin versions differ")
    check(manifest["extensions"]["com.openai"]["interface"] == overlay["interface"],
          "Plugin interfaces differ")
    interface = overlay["interface"]
    for field in ("composerIcon", "logo"):
        target = interface.get(field, "")
        check(target.startswith("./assets/"), f"Invalid {field} path")
        asset = (root / target[2:]).resolve()
        check(asset.is_relative_to(root.resolve()) and asset.is_file(),
              f"Missing {field} asset: {target}")
    entry, = catalog["plugins"]
    check(entry["name"] == manifest["name"], "Marketplace name differs")
    check(entry["source"] == {"source": "local", "path": "./"}, "Invalid local source")
    check(overlay["skills"] == "./skills/", "Invalid skills directory")
    skills = sorted((root / "skills").glob("*/SKILL.md"))
    skill_names = {skill.parent.name for skill in skills}
    check(skill_names == EXPECTED_SKILLS,
          f"Unexpected skills: expected {sorted(EXPECTED_SKILLS)}, got {sorted(skill_names)}")
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
    for name in (".codex-plugin", ".claude-plugin", ".grok-plugin", ".agents", "skills", "shared", "assets", "adapters", "validation", "scripts", "tests"):
        paths.extend(path for path in (ROOT / name).rglob("*")
                     if path.is_file() and "__pycache__" not in path.parts)
    with ZipFile(output, "w", ZIP_DEFLATED) as archive:
        for path in sorted(paths):
            archive.write(path, f'{manifest["name"]}/{path.relative_to(ROOT).as_posix()}')
    # ponytail: fixed package folders; add an explicit folder when the package gains resources.
    print(f"Validated {len(EXPECTED_SKILLS)} skills; packaged {len(paths)} files: {output}")


if __name__ == "__main__":
    main()
