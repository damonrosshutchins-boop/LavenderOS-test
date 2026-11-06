
from pathlib import Path
from datetime import datetime
import shutil
import sys

html = Path("LavenderOS.html")
source = html.read_text(encoding="utf-8")

anchor = "function removeCustomWallpaper()"

if "function setLocalWallpaper(" in source:
    sys.exit("Local wallpaper loader already exists.")

local_function = r'''
/* Local static wallpaper loader - bypasses external URL validation. */
function setLocalWallpaper(url, opts) {
  opts = opts || {};

  if (!/^wallpapers\/[^?#]+$/i.test(String(url || ''))) {
    toast('Invalid local wallpaper path.');
    return Promise.resolve(false);
  }

  const image = new Image();

  image.onload = function () {
    if (!image.naturalWidth || !image.naturalHeight) {
      toast('Local wallpaper could not be decoded.');
      if (opts.onDone) opts.onDone(false);
      return;
    }

    S.customBg = url;
    S.customBgType = 'image';
    S.wallpaper = 'custom';

    save(true);
    applyWallpaper();

    if (opts.onDone) opts.onDone(true);
    toast('Wallpaper applied');
  };

  image.onerror = function () {
    toast('Local wallpaper file could not be loaded.');
    if (opts.onDone) opts.onDone(false);
  };

  image.src = url;

  return new Promise(resolve => {
    const done = opts.onDone;
    opts.onDone = function (ok) {
      if (done) done(ok);
      resolve(ok);
    };
  });
}

'''

if source.count(anchor) != 1:
    sys.exit("Could not locate removeCustomWallpaper().")

source = source.replace(anchor, local_function + anchor, 1)

# Switch gallery clicks to the new local loader.
old = """        if (item) setCustomWallpaper(item.poster, {
          onDone: () => renderSettings(root)
        });"""

new = """        if (item) setLocalWallpaper(item.poster, {
          onDone: () => renderSettings(root)
        });"""

if old not in source:
    sys.exit("Could not locate the local wallpaper gallery click handler.")

source = source.replace(old, new, 1)

backup = html.with_name(
    "LavenderOS.html.before_local_loader_"
    + datetime.now().strftime("%Y%m%d_%H%M%S")
    + ".bak"
)

shutil.copy2(html, backup)

try:
    html.write_text(source, encoding="utf-8")
except Exception:
    shutil.copy2(backup, html)
    raise

print("Local wallpaper loader installed.")
print("Gallery now uses direct local image loading.")
print("External custom wallpaper links remain unchanged.")
print("Backup:", backup.name)
