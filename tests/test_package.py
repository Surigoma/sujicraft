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
    archive = ROOT / "dist" / f'{manifest["name"]}-{manifest["version"]}-codex.zip'
    with TemporaryDirectory(prefix="engineering-plugin-check-") as temp:
        with ZipFile(archive) as zipped:
            assert zipped.testzip() is None
            zipped.extractall(temp)
        moved = Path(temp) / manifest["name"]
        package.validate(moved)
        for source in (ROOT / "skills").glob("*/SKILL.md"):
            assert source.read_bytes() == (moved / source.relative_to(ROOT)).read_bytes()
        assert (ROOT / "shared/principles.md").read_bytes() == (moved / "shared/principles.md").read_bytes()
        icon = Path("assets/branding/sujicraft-icon-joinery.png")
        assert (ROOT / icon).read_bytes() == (moved / icon).read_bytes()
        codex = shutil.which("codex")
        if codex:
            command = [codex, "-c", 'marketplaces.sujicraft-local.source_type="local"',
                       "-c", f'marketplaces.sujicraft-local.source={json.dumps(moved.as_posix())}',
                       "plugin", "list", "--marketplace", "sujicraft-local",
                       "--available", "--json"]
            result = subprocess.run(command, cwd=moved, text=True, encoding="utf-8",
                                    capture_output=True, check=True)
            catalog = json.loads(result.stdout)
            assert any(item["pluginId"] == "sujicraft@sujicraft-local"
                       and item["version"] == manifest["version"]
                       for item in catalog["available"])
            print("PASS: Codex recognizes relocated plugin")
        else:
            print("SKIP: Codex CLI unavailable")
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
