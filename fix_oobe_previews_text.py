
from pathlib import Path
from datetime import datetime
import shutil
import sys

file = Path("LavenderOS.html")
s = file.read_text(errors="ignore")

# Replace the wizard wallpaper-choice function.
start = s.find("function oobeWallpaperChoices()")
end = s.find("/* The wizard shows the wallpapers", start)

if start < 0 or end < 0:
    sys.exit("Wallpaper function not found.")

new_function = r"""
function oobeWallpaperChoices() {
  const wallpapers = window.__LAVENDER_LOCAL_STATIC_WALLPAPERS || [];

  return wallpapers.map((url, i) => ({
    id: 'localwp:' + i,
    name: '',
    kind: 'image',
    file: '',
    poster: url,
    desc: '',
    bg: '#0b1030 url(' +
      encodeURI(String(url)).replace(/[&()'"\\]/g, ch =>
        '%' + ch.charCodeAt(0).toString(16)
      ) +
      ') center/cover'
  }));
}

"""

s = s[:start] + new_function + s[end:]

# White and lavender typography, plus visible wallpaper previews.
css = """
<style id="lavender-oobe-preview-text-final">

#oobe #oobe-card {
  color: #f5f0ff !important;
}

#oobe .oobe-title,
#oobe .oobe-brand b,
#oobe .oobe-section,
#oobe .oobe-label,
#oobe .oobe-note,
#oobe .oobe-row-main b,
#oobe .oobe-setting-txt b,
#oobe .oobe-font-name {
  color: #f5f0ff !important;
}

#oobe .oobe-subtitle,
#oobe .oobe-hint,
#oobe .oobe-hint b,
#oobe .oobe-row-main > span,
#oobe .oobe-setting-txt > span,
#oobe .oobe-stepcount,
#oobe .oobe-stepname,
#oobe .oobe-brand span,
#oobe .wp-pager-info,
#oobe .oobe-footer {
  color: #d5c7f2 !important;
}

#oobe .oobe-stepcount b,
#oobe .oobe-row-check,
#oobe .oobe-font-check {
  color: #c4b5fd !important;
}

#oobe .oobe-btn,
#oobe .wp-pager-btn {
  color: #f5f0ff !important;
}

#oobe .oobe-btn-primary {
  color: #ffffff !important;
}

/* Wallpaper thumbnails */
#oobe .oobe-wall-thumb {
  display: block !important;
  width: 100% !important;
  height: 108px !important;
  min-height: 108px !important;
  background-color: #171020 !important;
  background-position: center !important;
  background-repeat: no-repeat !important;
  background-size: cover !important;
  border-radius: 10px !important;
  overflow: hidden !important;
  box-shadow: inset 0 0 0 1px rgba(196,181,253,.2);
}

#oobe .oobe-wall {
  color: #f5f0ff !important;
}

#oobe .oobe-wall.on {
  border-color: #c4b5fd !important;
  box-shadow: 0 0 0 1px rgba(196,181,253,.35),
              0 0 18px rgba(139,92,246,.15);
}

/* Preview-only gallery: no filenames */
#oobe .oobe-wall-name {
  display: none !important;
}

#oobe input,
#oobe textarea,
#oobe select {
  color: #f5f0ff !important;
}

#oobe input::placeholder,
#oobe textarea::placeholder {
  color: #a99abd !important;
}

</style>
"""

head = s.lower().find("</head>")
if head < 0:
    sys.exit("Could not find document head.")

s = s[:head] + "\n" + css + "\n" + s[head:]

backup = file.with_name(
    file.name + ".before_oobe_preview_text_" +
    datetime.now().strftime("%Y%m%d_%H%M%S") + ".bak"
)

shutil.copy2(file, backup)
file.write_text(s)

print("Wallpaper preview URL fixed.")
print("Wizard text changed to white and lavender.")
print("Wallpaper filenames remain hidden.")
print("Backup:", backup.name)
