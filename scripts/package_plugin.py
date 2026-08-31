#!/usr/bin/env python3
"""Create a deterministic CNS Skills plugin ZIP and SHA-256 checksum."""

from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = ROOT / "plugins" / "cns-skills"
FIXED_TIME = (2026, 8, 31, 0, 0, 0)


def plugin_version() -> str:
    manifest = json.loads((PLUGIN_ROOT / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"))
    version = manifest.get("version")
    if not isinstance(version, str) or not version:
        raise ValueError("plugin manifest has no version")
    return version


def source_files() -> list[Path]:
    return [
        path
        for path in sorted(PLUGIN_ROOT.rglob("*"))
        if path.is_file() and "__pycache__" not in path.parts and path.suffix != ".pyc"
    ]


def build(output_dir: Path) -> tuple[Path, Path, str]:
    version = plugin_version()
    output_dir.mkdir(parents=True, exist_ok=True)
    archive = output_dir / f"cns-skills-v{version}.zip"
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as bundle:
        for source in source_files():
            relative = source.relative_to(PLUGIN_ROOT).as_posix()
            info = zipfile.ZipInfo(relative, date_time=FIXED_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            bundle.writestr(info, source.read_bytes())
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    checksum = output_dir / f"{archive.name}.sha256"
    checksum.write_text(f"{digest}  {archive.name}\n", encoding="utf-8")
    return archive, checksum, digest


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=Path("dist"))
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    archive, checksum, digest = build(args.output_dir)
    print(f"Created {archive} ({digest})")
    print(f"Created {checksum}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
