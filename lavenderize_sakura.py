from pathlib import Path
from datetime import datetime
import shutil
import sys

file = Path("LavenderOS.html")
html = file.read_text(encoding="utf-8")

replacements = {
    "#f8c6d0": "#d9c5ff",
    "#f8a5c2": "#b99aff",
    "#e84393": "#8960dc",
    "#5c2c34": "#35234f",
    "#fff0f5": "#f4edff",
    "rgba(248,165,194,0.4)": "rgba(185,154,255,0.4)",
}

counts = {old: html.count(old) for old in replacements}

if not any(counts.values()):
    print("No matching Sakura colors found. Nothing changed.")
    sys.exit(1)

backup = file.with_name(
    f"LavenderOS.html.before_lavender_palette_{datetime.now():%Y%m%d_%H%M%S}.bak"
)
shutil.copy2(file, backup)

for old, new in replacements.items():
    html = html.replace(old, new)

file.write_text(html, encoding="utf-8")

print("Lavender palette applied.")
print("Replacements:")
for old, count in counts.items():
    if count:
        print(f"  {old} -> {replacements[old]} ({count})")
print(f"Backup: {backup.name}")
