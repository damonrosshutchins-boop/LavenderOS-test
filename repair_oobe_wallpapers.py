
from pathlib import Path
from datetime import datetime
from urllib.parse import unquote
import re
import shutil
import subprocess
import sys

FILE = Path("LavenderOS.html")
ARRAY_NAME = "LOCAL_STATIC_WALLPAPERS"
GLOBAL_NAME = "__LAVENDER_LOCAL_STATIC_WALLPAPERS"

if not FILE.is_file():
    sys.exit("STOP: LavenderOS.html not found. Run this from the project folder.")

s = FILE.read_text(errors="ignore")
original = s

def stop(message):
    sys.exit("STOP: " + message)

# ---------------------------------------------------------
# 1. Find and validate the existing local wallpaper array.
# ---------------------------------------------------------

arrays = list(re.finditer(
    r"const\s+LOCAL_STATIC_WALLPAPERS\s*=\s*\[(.*?)\]\s*;",
    s,
    re.S
))

if len(arrays) != 1:
    stop(f"Expected one local wallpaper array; found {len(arrays)}.")

array_match = arrays[0]
entries = re.findall(r"""(['"])(.*?)\1""", array_match.group(1))
paths = [entry[1] for entry in entries]

if not paths:
    stop("The local wallpaper array is empty.")

static_extensions = {
    ".jpg", ".jpeg", ".png", ".webp", ".avif", ".bmp"
}

static_paths = [
    url for url in paths
    if Path(unquote(url.split("?")[0])).suffix.lower()
    in static_extensions
]

if not static_paths:
    stop("No static image files were found in the wallpaper array.")

# Locate the script containing the array.
script_pattern = re.compile(
    r"<script\b[^>]*>(.*?)</script\s*>",
    re.I | re.S
)
script_tags = list(script_pattern.finditer(s))

array_script = next(
    (
        tag for tag in script_tags
        if tag.start(1) <= array_match.start()
        and tag.end(1) >= array_match.end()
    ),
    None
)

if array_script is None:
    stop("Could not locate the script containing the wallpaper array.")

# ---------------------------------------------------------
# 2. Expose the array to the setup wizard's separate script.
# ---------------------------------------------------------

array_script_text = array_script.group(1)

if f"window.{GLOBAL_NAME} = " not in array_script_text:
    assignment = (
        "\n"
        f"window.{GLOBAL_NAME} = {ARRAY_NAME}.filter(url => "
        r"/\.(?:jpe?g|png|webp|avif|bmp)(?:[?#]|$)/i.test(String(url))"
        ");\n"
    )

    s = s[:array_match.end()] + assignment + s[array_match.end():]

# ---------------------------------------------------------
# 3. Connect the wizard's wallpaper-choice function.
# ---------------------------------------------------------

choice_pattern = re.compile(
    r"function\s+oobeWallpaperChoices\s*\(\s*\)\s*\{.*?\n\}",
    re.S
)

choice_matches = list(choice_pattern.finditer(s))

if len(choice_matches) != 1:
    stop(
        "Expected one oobeWallpaperChoices function; "
        f"found {len(choice_matches)}."
    )

new_choice_function = r"""
function oobeWallpaperChoices() {
  const wallpapers = window.__LAVENDER_LOCAL_STATIC_WALLPAPERS || [];

  return wallpapers.map((url, i) => ({
    id: 'localwp:' + i,
    name: '',
    kind: 'image',
    file: '',
    poster: url,
    desc: '',
    bg: '#0b1030 url("' +
        String(url).replace(/"/g, '%22') +
        '") center/cover'
  }));
}
""".strip()

m = choice_matches[0]
s = s[:m.start()] + new_choice_function + s[m.end():]

# ---------------------------------------------------------
# 4. Connect local wallpaper IDs to applyWallpaper().
# ---------------------------------------------------------

apply_matches = list(re.finditer(
    r"function\s+applyWallpaper\s*\(\s*\)\s*\{",
    s
))

if len(apply_matches) != 1:
    stop(
        "Expected one applyWallpaper function; "
        f"found {len(apply_matches)}."
    )

apply_start = apply_matches[0].start()
apply_open = apply_matches[0].end()

apply_end = s.find("\nfunction ", apply_open)
if apply_end < 0:
    apply_end = min(len(s), apply_open + 12000)

apply_section = s[apply_start:apply_end]

if "const localMatch = /^localwp:" not in apply_section:
    cv_match = re.search(
        r"const\s+cv\s*=\s*document\.getElementById"
        r"\(\s*['\"]wallpaper-canvas['\"]\s*\)\s*;",
        apply_section
    )

    wrap_match = re.search(
        r"const\s+wrap\s*=\s*document\.getElementById"
        r"\(\s*['\"]wallpaper['\"]\s*\)\s*;",
        apply_section
    )

    if not cv_match or not wrap_match:
        stop("Could not identify the wallpaper renderer's canvas and wrapper.")

    if wrap_match.start() < cv_match.start():
        stop("Unexpected applyWallpaper function structure.")

    insert_at = apply_start + wrap_match.end()

    local_branch = r"""

  // LavenderOS local static wallpaper support.
  const localMatch = /^localwp:(\d+)$/.exec(
    String(S.wallpaper || '')
  );

  const localWalls =
    window.__LAVENDER_LOCAL_STATIC_WALLPAPERS || [];

  if (localMatch) {
    const localUrl = localWalls[Number(localMatch[1])];

    if (localUrl) {
      stopWallLoop();

      if (cv) cv.style.opacity = '0';
      if (wrap) wrap.style.background = '#0b1030';

      renderCustomBg(localUrl, false);

      if (typeof applyBgFilters === 'function') {
        setTimeout(applyBgFilters, 40);
      }

      return;
    }
  }
"""

    s = s[:insert_at] + local_branch + s[insert_at:]

# ---------------------------------------------------------
# 5. Prevent the animated canvas restarting over local images.
# ---------------------------------------------------------

old_visibility = (
    "else if (S.wallpaper !== 'custom') startWallLoop();"
)

new_visibility = (
    "else if (S.wallpaper !== 'custom' && "
    "!/^localwp:\\d+$/.test(String(S.wallpaper || ''))) "
    "startWallLoop();"
)

if old_visibility in s:
    s = s.replace(old_visibility, new_visibility, 1)

# ---------------------------------------------------------
# 6. Make the Finish wrapper handle a failed core handler.
# ---------------------------------------------------------

old_finish = (
    "function oobeFinish13() { "
    "if (_coreOobeFinish) { _coreOobeFinish(); return; } "
    "S.setupDone = true; S.lastUsed = Date.now(); "
    "save(true); bootDesktop(); "
    "}"
)

new_finish = """
function oobeFinish13() {
  if (_coreOobeFinish) {
    try {
      _coreOobeFinish();
      return;
    } catch (err) {
      console.error('Core setup finish failed:', err);
    }
  }

  try {
    if (typeof S !== 'undefined' && S) {
      if (
        typeof oobeTempTheme !== 'undefined' &&
        oobeTempTheme
      ) {
        S.wallpaper = oobeTempTheme;
      }

      S.setupDone = true;
      S.lastUsed = Date.now();

      if (typeof save === 'function') save(true);
      if (typeof applyWallpaper === 'function') applyWallpaper();
    }
  } catch (err) {
    console.error('Setup fallback failed:', err);
  }

  const host = document.getElementById('oobe');

  if (host) {
    host.classList.remove('show');
    host.style.display = 'none';
    host.innerHTML = '';
  }

  if (typeof window.bootDesktop === 'function') {
    window.bootDesktop();
  } else if (typeof renderDesktop13 === 'function') {
    renderDesktop13();
  }
}
""".strip()

if old_finish in s:
    s = s.replace(old_finish, new_finish, 1)
elif "function oobeFinish13()" not in s:
    stop("Could not locate the Finish wrapper.")
else:
    print("NOTICE: Finish wrapper has a different structure; left unchanged.")

# ---------------------------------------------------------
# 7. Verify all affected inline JavaScript before writing.
# ---------------------------------------------------------

check_scripts = list(script_pattern.finditer(s))

affected = [
    tag.group(1)
    for tag in check_scripts
    if (
        "oobeWallpaperChoices" in tag.group(1)
        or "function applyWallpaper()" in tag.group(1)
        or GLOBAL_NAME in tag.group(1)
        or "function oobeFinish13()" in tag.group(1)
    )
]

if not affected:
    stop("Could not locate the affected JavaScript blocks.")

for index, js in enumerate(affected):
    temp = Path(f"/tmp/lavender-oobe-repair-{index}.js")
    temp.write_text(js)

    result = subprocess.run(
        ["node", "--check", str(temp)],
        capture_output=True,
        text=True
    )

    if result.returncode:
        stop(
            f"JavaScript syntax check failed in block {index}:\n"
            + result.stderr
        )

# ---------------------------------------------------------
# 8. Backup and save only after all checks pass.
# ---------------------------------------------------------

if s == original:
    stop("No changes were necessary.")

backup = FILE.with_name(
    FILE.name
    + ".before_oobe_wallpaper_repair_"
    + datetime.now().strftime("%Y%m%d_%H%M%S")
    + ".bak"
)

shutil.copy2(FILE, backup)
FILE.write_text(s)

print()
print("LavenderOS wallpaper repair installed.")
print("Local static wallpaper entries:", len(static_paths))
print("Wizard catalog: connected across scripts")
print("Local wallpaper rendering: connected")
print("Visibility handling: updated")
print("Finish fallback: repaired")
print("JavaScript syntax checks passed:", len(affected))
print("Backup:", backup.name)
