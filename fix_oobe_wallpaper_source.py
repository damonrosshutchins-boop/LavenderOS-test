from pathlib import Path
from datetime import datetime
from urllib.parse import unquote
import re
import shutil
import sys

file = Path("LavenderOS.html")
s = file.read_text(errors="ignore")

marker = "LAVENDER_OOBE_LOCAL_WALLPAPER_SOURCE_V1"

if marker in s:
    sys.exit("STOP: This wallpaper patch is already installed.")

# Find the existing local wallpaper catalog.
arrays = list(re.finditer(
    r"const\s+LOCAL_STATIC_WALLPAPERS\s*=\s*\[(.*?)\]\s*;",
    s,
    re.S
))

if len(arrays) != 1:
    sys.exit(
        f"STOP: Expected one local wallpaper array; found {len(arrays)}."
    )

paths = re.findall(r"""(['"])(.*?)\1""", arrays[0].group(1))
paths = [item[1] for item in paths]

if not paths:
    sys.exit("STOP: Local wallpaper array is empty.")

allowed = {".jpg", ".jpeg", ".png", ".webp", ".avif", ".bmp"}

invalid = [
    path for path in paths
    if Path(unquote(path.split("?")[0])).suffix.lower() not in allowed
]

if invalid:
    sys.exit(
        "STOP: Non-static or unsupported files found in local catalog:\n"
        + "\n".join(invalid[:10])
    )

# Replace the wizard's separate built-in/ZIP/video catalog.
pattern = re.compile(
    r"function\s+oobeWallpaperChoices\(\)\s*\{.*?\n\}",
    re.S
)

matches = list(pattern.finditer(s))

if len(matches) != 1:
    sys.exit(
        f"STOP: Expected one wizard wallpaper function; found {len(matches)}."
    )

old_function = matches[0].group()

if "ZIP_WP_LIST" not in old_function or "EXTRA_WP_LIST" not in old_function:
    sys.exit("STOP: Unexpected wallpaper function; refusing to replace it.")

new_function = """function oobeWallpaperChoices() {
  /* LAVENDER_OOBE_LOCAL_WALLPAPER_SOURCE_V1 */
  return LOCAL_STATIC_WALLPAPERS.map((url, i) => ({
    id: 'localwp:' + i,
    name: '',
    kind: 'image',
    file: '',
    poster: url,
    desc: '',
    bg: '#0b1030 url("' + String(url).replace(/"/g, '%22') + '") center/cover'
  }));
}"""

s = s[:matches[0].start()] + new_function + s[matches[0].end():]

# Change old GIF defaults to the first local image.
replacements = [
    ("let oobeTempTheme = 'gifFallen';",
     "let oobeTempTheme = 'localwp:0';"),

    ("let oobeTempBackground = 'gifFallen';",
     "let oobeTempBackground = 'localwp:0';"),

    ("? S.wallpaper : 'gifFallen';",
     "? S.wallpaper : 'localwp:0';"),

    ("oobeTempTheme || oobeTempBackground || 'gifFallen'",
     "oobeTempTheme || oobeTempBackground || 'localwp:0';".rstrip(";"))
]

for old, new in replacements:
    count = s.count(old)
    if count != 1:
        sys.exit(
            f"STOP: Expected one occurrence of:\n{old}\nFound: {count}"
        )
    s = s.replace(old, new, 1)

# Update the wizard's outdated animation description.
old_text = "Animated GIFs and video clips both play on a loop."
if s.count(old_text) != 1:
    sys.exit("STOP: Could not uniquely locate the old wallpaper description.")

s = s.replace(
    old_text,
    "Choose a static wallpaper from your local collection.",
    1
)

# Hide captions so the gallery contains image previews only.
css = """
<style id="lavender-oobe-local-wallpaper-display">
#oobe .oobe-wall-name {
  display: none !important;
}
</style>
"""

head_end = s.lower().find("</head>")
body_start = s.lower().find("<body")

if head_end < 0 or body_start < 0 or head_end > body_start:
    sys.exit("STOP: Could not verify the main document head.")

if s[:head_end].count("<html") != 1:
    sys.exit("STOP: Main document boundary is ambiguous.")

# Create backup before modifying the file.
backup = file.with_name(
    file.name + ".before_oobe_local_wallpapers_" +
    datetime.now().strftime("%Y%m%d_%H%M%S") + ".bak"
)

shutil.copy2(file, backup)

s = s[:head_end] + "\n" + css + "\n" + s[head_end:]
file.write_text(s)

print("Setup wizard wallpaper source replaced.")
print("Local static wallpapers:", len(paths))
print("Animated images and videos: excluded")
print("Wallpaper names: hidden")
print("Pagination: preserved")
print("Default wallpaper: localwp:0")
print("Backup:", backup.name)
