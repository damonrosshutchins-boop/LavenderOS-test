
from pathlib import Path
from urllib.parse import quote
from datetime import datetime
import shutil
import sys

root = Path(__file__).resolve().parent
html = root / "LavenderOS.html"
wallpapers = root / "wallpapers"

if not html.exists() or not wallpapers.is_dir():
    sys.exit("Missing LavenderOS.html or wallpapers folder.")

source = html.read_text(encoding="utf-8")

images = sorted(
    p for p in wallpapers.iterdir()
    if p.is_file() and p.suffix.lower() in {
        ".jpg", ".jpeg", ".png", ".webp"
    }
)

if not images:
    sys.exit("No static wallpaper images found.")

urls = [
    "wallpapers/" + quote(p.name, safe="-._~")
    for p in images
]

# Add the local wallpaper list before bgWallpaperOpts().
manifest = (
    "const LOCAL_STATIC_WALLPAPERS = "
    + repr(urls)
    + ";\n\n"
)

anchor = "function bgWallpaperOpts()"
source = source.replace(anchor, manifest + anchor, 1)

# Add local images to the actual gallery array.
anchor = """    .concat((window.EXTRA_WP_LIST || []).map(z => ({ id: z.id, name: z.name, icon: 'image', poster: z.poster || '', file: z.file, kind: z.kind || 'video' })))"""

replacement = anchor + """
    .concat(LOCAL_STATIC_WALLPAPERS.map((url, i) => ({
      id: 'localwp:' + i,
      name: '',
      icon: 'image',
      poster: url,
      local: true
    })))"""

source = source.replace(anchor, replacement, 1)

# Hide names on both card templates.
old_label = '<b style="font-size:13px;text-align:center;display:block">${escapeHtml(o.name)}</b>'
new_label = '${o.local ? "" : `<b style="font-size:13px;text-align:center;display:block">${escapeHtml(o.name)}</b>`}'
source = source.replace(old_label, new_label)

# Show the selection marker for the currently active local image.
source = source.replace(
    "checkBadge(S.wallpaper === o.id)",
    "checkBadge(S.wallpaper === o.id || (o.local && S.wallpaper === 'custom' && S.customBg === o.poster))"
)

source = source.replace(
    "S.wallpaper === o.id ? 'var(--accent)' : 'var(--card-border)'",
    "(S.wallpaper === o.id || (o.local && S.wallpaper === 'custom' && S.customBg === o.poster)) ? 'var(--accent)' : 'var(--card-border)'"
)

# Apply a selected local image.
old_click = """      const wp = it.dataset.wp;
      if (wp === 'spinningSakura')"""

new_click = """      const wp = it.dataset.wp;
      if (wp && wp.startsWith('localwp:')) {
        const item = bgWallpaperOpts().find(o => o.id === wp);
        if (item) setCustomWallpaper(item.poster, {
          onDone: () => renderSettings(root)
        });
        return;
      }
      if (wp === 'spinningSakura')"""

source = source.replace(old_click, new_click, 1)

# Backup and write.
backup = html.with_name(
    "LavenderOS.html.before_local_wallpapers_"
    + datetime.now().strftime("%Y%m%d_%H%M%S")
    + ".bak"
)

shutil.copy2(html, backup)
html.write_text(source, encoding="utf-8")

print("Local wallpaper patch applied.")
print("Static images added:", len(images))
print("GIF files excluded.")
print("Backup:", backup.name)
