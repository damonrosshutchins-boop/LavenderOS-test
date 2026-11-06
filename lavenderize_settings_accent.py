from pathlib import Path
from datetime import datetime
import shutil
import re
import sys

file = Path("LavenderOS.html")
content = file.read_text(errors="ignore")

start = content.find("function applyTheme20()")
if start < 0:
    sys.exit("ERROR: applyTheme20 not found.")

end = content.find("</script>", start)
if end < 0:
    sys.exit("ERROR: Could not isolate the script.")

before = content[:start]
function = content[start:end]
after = content[end:]

replacements = [
    (r"let h\s*=\s*335,\s*l\s*=\s*70;", "let h = 255, l = 70;"),
    (r"\(\(dom\.h\s*-\s*335\)\s*%", "((dom.h - 255) %"),
    (r"const domH\s*=\s*335\s*\+\s*dist;", "const domH = 255 + dist;"),
    (r"lerp\(domH,\s*335,", "lerp(domH, 255,")
]

for pattern, replacement in replacements:
    function, count = re.subn(pattern, replacement, function, count=1)
    if count != 1:
        sys.exit(f"STOP: Expected one match for {pattern}, found {count}.")

function = function.replace(
    "signature sakura pink",
    "signature lavender"
).replace(
    "shortest angular distance to sakura pink",
    "shortest angular distance to lavender"
)

backup = file.with_name(
    file.name + ".before_lavender_accent_" +
    datetime.now().strftime("%Y%m%d_%H%M%S") + ".bak"
)

shutil.copy2(file, backup)
file.write_text(before + function + after)

print("Lavender accent patch applied!")
print("Pink hue anchor: 335° -> 255°")
print("Wallpaper adaptation preserved.")
print("Backup:", backup.name)
