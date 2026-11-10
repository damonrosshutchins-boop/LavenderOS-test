#!/usr/bin/env python3
"""Limit LavenderOS to one locally hosted, metadata-free wallpaper photo.

Applied to the original upstream HTML so LavenderOS.html itself works;
not an iframe wrapper and not an externally hosted image.
"""
from pathlib import Path
import re

html_path = Path("LavenderOS.html")
photo_path = Path("wallpapers/only-background.webp")
assert photo_path.is_file() and photo_path.stat().st_size > 1000, "Missing wallpaper image"
data = html_path.read_text(encoding="utf-8")
marker = "LAVENDER_ONLY_PHOTO_WALLPAPER_20261109"
if marker in data:
    print("Wallpaper lock already installed")
    raise SystemExit(0)

def replace_exact(old, new):
    global data
    found = data.count(old)
    assert found == 1, f"Expected exactly one {old[:90]!r}; found {found}"
    data = data.replace(old, new, 1)

array = re.compile(r"const LOCAL_STATIC_WALLPAPERS\s*=\s*\[[\s\S]*?\]\s*;")
matches = list(array.finditer(data))
assert len(matches) == 1, f"Found {len(matches)} wallpaper arrays"
data = array.sub(
    "/* " + marker + " */\n"
    'const LOCAL_STATIC_WALLPAPERS = ["wallpapers/only-background.webp"];',
    data, count=1,
)
replace_exact(
    "function applyWallpaper() {\n",
    "function applyWallpaper() {\n"
    "  // Reset older saved themes and all attempted background changes.\n"
    "  S.wallpaper = 'localwp:0';\n"
    "  S.customBg = '';\n"
    "  S.customBgType = '';\n",
)
replace_exact(
    "function persistNow() {\n",
    "function persistNow() {\n"
    "  S.wallpaper = 'localwp:0';\n"
    "  S.customBg = '';\n"
    "  S.customBgType = '';\n",
)
replace_exact(
    "function setWallpaper(id) {\n",
    "function setWallpaper(id) {\n"
    "  // Only the provided photo may be selected.\n"
    "  id = 'localwp:0';\n",
)
replace_exact(
    "function setCustomWallpaper(url, opts) {\n",
    "function setCustomWallpaper(url, opts) {\n"
    "  // Disallow arbitrary external image URLs and custom-image uploads.\n"
    "  if (opts && typeof opts.onDone === 'function') opts.onDone(false);\n"
    "  if (typeof toast === 'function') toast('Only the provided photo is available.');\n"
    "  return Promise.resolve(false);\n",
)
replace_exact(
    "function setLocalWallpaper(url, opts) {\n",
    "function setLocalWallpaper(url, opts) {\n"
    "  url = 'wallpapers/only-background.webp';\n",
)
replace_exact(
    "function removeCustomWallpaper() {\n",
    "function removeCustomWallpaper() {\n"
    "  S.wallpaper = 'localwp:0';\n"
    "  S.customBg = '';\n"
    "  S.customBgType = '';\n"
    "  save(true);\n"
    "  applyWallpaper();\n"
    "  return;\n",
)
# Starting the onboarding wizard should also select the one photo.
for old, new in [
    ("let oobeTempTheme = 'gifFallen';", "let oobeTempTheme = 'localwp:0';"),
    ("let oobeTempBackground = 'gifFallen';", "let oobeTempBackground = 'localwp:0';"),
]:
    n = data.count(old)
    if n == 1:
        data = data.replace(old, new, 1)
    elif n > 1:
        raise RuntimeError("Unexpected repeated onboarding wallpaper defaults")

# The gallery and the onboarding picker already map over
# LOCAL_STATIC_WALLPAPERS, which now contains exactly one path.
assert data.count(marker) == 1
assert 'const LOCAL_STATIC_WALLPAPERS = ["wallpapers/only-background.webp"];' in data
assert "function bgWallpaperOpts()" in data
assert "function oobeWallpaperChoices()" in data
assert "return Promise.resolve(false);" in data
html_path.write_text(data, encoding="utf-8")
print("Locked LavenderOS wallpaper gallery, onboarding, custom uploads, and persisted theme")
print("Image:", photo_path.as_posix(), "bytes:", photo_path.stat().st_size)
