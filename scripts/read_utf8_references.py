#!/usr/bin/env python3
"""Read auto-listing skill references with UTF-8 on every Windows machine."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


REFERENCE_FILES = [
    "references/verbatim-user-requirements.md",
    "references/full-original-instructions.md",
    "references/ozon-listing-rules.md",
    "references/original-requirements-coverage.md",
    "references/final-audit-checklist.md",
]

MOJIBAKE_MARKERS = [
    "\u8930\u64b6\u657c\u93b4",
    "\u6d93",
    "\u9225",
    "\ufffd",
]


def configure_stdout() -> None:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except AttributeError:
        pass


def skill_root() -> Path:
    return Path(__file__).resolve().parents[1]


def read_utf8(path: Path) -> str:
    text = path.read_text(encoding="utf-8-sig")
    markers = [marker for marker in MOJIBAKE_MARKERS if marker in text]
    if markers:
        raise SystemExit(
            f"Encoding validation failed for {path}: found mojibake marker(s) {markers!r}. "
            "Do not continue from garbled text."
        )
    if not any("\u4e00" <= ch <= "\u9fff" for ch in text):
        raise SystemExit(
            f"Encoding validation failed for {path}: no CJK text detected. "
            "The reference may be damaged or incomplete."
        )
    return text


def main() -> int:
    configure_stdout()
    parser = argparse.ArgumentParser()
    parser.add_argument("--all", action="store_true", help="print all required references")
    parser.add_argument("--check", action="store_true", help="validate all required references")
    parser.add_argument("--file", help="print one reference file, relative to the skill root")
    args = parser.parse_args()

    if not (args.all or args.check or args.file):
        parser.error("use --all, --check, or --file")

    root = skill_root()
    files = [args.file] if args.file else REFERENCE_FILES

    loaded: list[tuple[Path, str]] = []
    for rel in files:
        path = root / rel
        if not path.is_file():
            raise SystemExit(f"Missing required reference: {path}")
        loaded.append((path, read_utf8(path)))

    if args.check:
        print(f"UTF-8 reference check passed: {len(loaded)} file(s).")
        return 0

    for index, (path, text) in enumerate(loaded, start=1):
        if index > 1:
            print("\n\n")
        print("=" * 80)
        print(f"BEGIN UTF-8 REFERENCE: {path}")
        print("=" * 80)
        print(text)
        print("=" * 80)
        print(f"END UTF-8 REFERENCE: {path}")
        print("=" * 80)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
