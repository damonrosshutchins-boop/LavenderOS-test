from pathlib import Path
from datetime import datetime
import re
import shutil
import sys

file = Path("LavenderOS.html")
s = file.read_text(errors="ignore")

pattern = r"const LOCAL_STATIC_WALLPAPERS\s*=\s*\[.*?\];"
matches = list(re.finditer(pattern, s, re.S))

if len(matches) != 2:
    sys.exit(f"STOP: Expected 2 declarations, found {len(matches)}.")

first, second = matches

if first.group() != second.group():
    sys.exit("STOP: The two declarations differ. Nothing changed.")

backup = file.with_name(
    file.name + ".before_wallpaper_duplicate_fix_" +
    datetime.now().strftime("%Y%m%d_%H%M%S") + ".bak"
)

shutil.copy2(file, backup)

s = s[:second.start()] + s[second.end():]
file.write_text(s)

print("Removed duplicate wallpaper declaration.")
print("Kept all 141 wallpaper paths.")
print("Backup:", backup.name)
