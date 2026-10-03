"""Check relocation, broken-reference detection, and Codex catalog loading."""
import importlib.util
import json
import shutil
import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("package", ROOT / "scripts/package.py")
package = importlib.util.module_from_spec(spec)
spec.loader.exec_module(package)


def main():
    manifest = package.validate(ROOT)
    interface = manifest["extensions"]["com.openai"]["interface"]
    icon = "./assets/branding/sujicraft-icon-joinery.png"
    assert interface["composerIcon"] == icon
    assert interface["logo"] == icon
    archive = ROOT / "dist" / f'{manifest["name"]}-{manifest["version"]}-codex.zip'
    with TemporaryDirectory(prefix="engineering-plugin-check-") as temp:
        with ZipFile(archive) as zipped:
            assert zipped.testzip() is None
            zipped.extractall(temp)
        moved = Path(temp) / manifest["name"]
        package.validate(moved)
        compatibility = moved / ".claude-plugin/plugin.json"
        assert compatibility.read_bytes() == (ROOT / ".claude-plugin/plugin.json").read_bytes()
        original_manifest = compatibility.read_text(encoding="utf-8")
        changed_manifest = json.loads(original_manifest)
        changed_manifest["version"] = "0.0.0"
        compatibility.write_text(json.dumps(changed_manifest), encoding="utf-8")
        try:
            package.validate(moved)
        except ValueError as error:
            assert "Claude plugin version differs" in str(error)
        else:
            raise AssertionError("Mismatched compatibility version went undetected")
        compatibility.write_text(original_manifest, encoding="utf-8")
        for client in ("claude", "grok"):
            executable = shutil.which(client)
            if executable:
                result = subprocess.run([executable, "plugin", "validate", str(moved)],
                                        capture_output=True, text=True, encoding="utf-8")
                assert result.returncode == 0, result.stdout + result.stderr
                print(f"PASS: {client} validates relocated plugin")
            else:
                print(f"SKIP: {client} CLI unavailable")
        for source in (ROOT / "skills").glob("*/SKILL.md"):
            assert source.read_bytes() == (moved / source.relative_to(ROOT)).read_bytes()
        assert (ROOT / "shared/principles.md").read_bytes() == (moved / "shared/principles.md").read_bytes()
        icon_path = Path(icon.removeprefix("./"))
        assert (ROOT / icon_path).read_bytes() == (moved / icon_path).read_bytes()
        codex = shutil.which("codex")
        if codex:
            marketplace = "sujicraft-validation"
            catalog_path = moved / ".agents/plugins/marketplace.json"
            catalog_data = json.loads(catalog_path.read_text(encoding="utf-8"))
            catalog_data["name"] = marketplace
            catalog_path.write_text(json.dumps(catalog_data, ensure_ascii=False, indent=2) + "\n",
                                    encoding="utf-8")
            command = [codex, "-c", f'marketplaces.{marketplace}.source_type="local"',
                       "-c", f'marketplaces.{marketplace}.source={json.dumps(moved.as_posix())}',
                       "plugin", "list", "--marketplace", marketplace,
                       "--available", "--json"]
            result = subprocess.run(command, cwd=moved, text=True, encoding="utf-8",
                                    capture_output=True, check=True)
            catalog = json.loads(result.stdout)
            assert any(item["pluginId"] == f"sujicraft@{marketplace}"
                       and item["version"] == manifest["version"]
                       for item in catalog["available"])
            print("PASS: Codex recognizes relocated plugin")
        else:
            print("SKIP: Codex CLI unavailable")
        icon_bytes = (moved / icon_path).read_bytes()
        (moved / icon_path).unlink()
        try:
            package.validate(moved)
        except ValueError as error:
            assert "asset" in str(error)
        else:
            raise AssertionError("Missing icon asset went undetected")
        (moved / icon_path).write_bytes(icon_bytes)
        (moved / "shared/principles.md").unlink()
        try:
            package.validate(moved)
        except ValueError as error:
            assert "reference" in str(error)
        else:
            raise AssertionError("Missing shared principles went undetected")
    print("PASS: ZIP, relocation, unchanged skills, missing-reference detection")


if __name__ == "__main__":
    main()
