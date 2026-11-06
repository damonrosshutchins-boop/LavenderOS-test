from pathlib import Path
from datetime import datetime
import shutil
import sys

file = Path("LavenderOS.html")
html = file.read_text(encoding="utf-8")

old_theme = """  --accent: #ff9ec7;
  --accent-press: #f88bb0;
  --accent-glow: rgba(255, 158, 199, 0.38);"""

new_theme = """  --accent: #a78bfa;
  --accent-press: #8b5cf6;
  --accent-glow: rgba(167, 139, 250, 0.35);"""

old_button = "background: linear-gradient(135deg, var(--accent), #f8a5c2);"
new_button = "background: linear-gradient(135deg, #a78bfa, #8b5cf6);"

if html.count(old_theme) != 1:
    sys.exit("STOP: Expected theme block was not found exactly once.")

if html.count(old_button) != 1:
    sys.exit("STOP: Expected primary button gradient was not found exactly once.")

backup = file.with_name(
    f"LavenderOS.html.before_purple_buttons_{datetime.now():%Y%m%d_%H%M%S}.bak"
)
shutil.copy2(file, backup)

html = html.replace(old_theme, new_theme, 1)
html = html.replace(old_button, new_button, 1)

file.write_text(html, encoding="utf-8")

print("LavenderOS purple accents applied.")
print(f"Backup: {backup.name}")
