
from pathlib import Path
from datetime import datetime
import shutil

html = Path("LavenderOS.html")
source = html.read_text(encoding="utf-8")

start = source.index("function bgWallpaperOpts() {")
end = source.index("function bgWallpaperPages(", start)

replacement = """function bgWallpaperOpts() {
  return LOCAL_STATIC_WALLPAPERS.map((url, i) => ({
    id: 'localwp:' + i,
    name: '',
    icon: 'image',
    poster: url,
    local: true
  }));
}

"""

updated = source[:start] + replacement + source[end:]

backup = html.with_name(
    "LavenderOS.html.before_clean_gallery_"
    + datetime.now().strftime("%Y%m%d_%H%M%S")
    + ".bak"
)

shutil.copy2(html, backup)
html.write_text(updated, encoding="utf-8")

print("Wallpaper gallery cleaned.")
print("Only local static wallpapers will be listed.")
print("Built-in GIFs, ZIP wallpapers and video wallpapers excluded.")
print("Backup:", backup.name)
