from pathlib import Path
from datetime import datetime
import re
import shutil
import sys

file = Path("LavenderOS.html")
s = file.read_text(errors="ignore")

pattern = r'<style id="lavender-oobe-complete-theme">.*?</style>'
matches = list(re.finditer(pattern, s, re.S))

if len(matches) != 1:
    sys.exit(f"STOP: Expected exactly 1 misplaced theme, found {len(matches)}.")

theme = matches[0].group()

# Remove the misplaced stylesheet.
clean = s[:matches[0].start()] + s[matches[0].end():]

# Locate the real document's closing head.
head_end = clean.lower().find("</head>")
body_start = clean.lower().find("<body")

if head_end < 0 or body_start < 0 or head_end > body_start:
    sys.exit("STOP: Could not safely identify the real document head.")

# Verify this is the main document, not an embedded template.
if clean[:head_end].count("<html") != 1:
    sys.exit("STOP: Main document boundary is ambiguous.")

backup = file.with_name(
    file.name + ".before_oobe_theme_relocation_" +
    datetime.now().strftime("%Y%m%d_%H%M%S") + ".bak"
)
shutil.copy2(file, backup)

clean = clean[:head_end] + "\n" + theme + "\n" + clean[head_end:]
file.write_text(clean)

print("Moved the existing purple wizard stylesheet.")
print("Destination: real LavenderOS document head.")
print("Embedded iframe template: cleaned.")
print("Backup:", backup.name)
