"""Vercel build step: publish the Flask static folder through Vercel's CDN.

Vercel serves static files only from public/, so copy web_app/static there (resolving the
images symlink). URLs stay the same (/static/...), so templates need no change.
"""
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "web_app" / "static"
DEST = ROOT / "public" / "static"

if __name__ == "__main__":
    if DEST.exists():
        shutil.rmtree(DEST)
    shutil.copytree(SRC, DEST, symlinks=False, ignore=shutil.ignore_patterns("src"))
    print(f"Copied {SRC} -> {DEST} ({sum(1 for p in DEST.rglob('*') if p.is_file())} files)")
