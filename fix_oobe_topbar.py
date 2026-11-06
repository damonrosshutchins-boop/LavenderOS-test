from pathlib import Path
from datetime import datetime
import shutil
import sys

file = Path("LavenderOS.html")
s = file.read_text(errors="ignore")

old = 'fill="#0067c0"'
p = s.find("function oobeHTML")

if p < 0:
    sys.exit("STOP: oobeHTML not found.")

end = s.find("function oobeStepHTML", p)
if end < 0:
    sys.exit("STOP: Could not locate oobeHTML boundary.")

section = s[p:end]

if 'class="oobe-mslogo"' not in section:
    sys.exit("STOP: Expected Windows-style SVG logo not found.")

if old not in section:
    sys.exit("STOP: Original blue logo fills not found.")

if "LAVENDER_OOBE_TOPBAR_FIX" in s:
    sys.exit("Top-bar fix already installed.")

backup = file.with_name(
    file.name + ".before_oobe_topbar_" +
    datetime.now().strftime("%Y%m%d_%H%M%S") + ".bak"
)
shutil.copy2(file, backup)

# Recolor only the four rectangles in the wizard's logo.
section = section.replace(old, 'fill="#c4b5fd"')
s = s[:p] + section + s[end:]

css = """
<style id="lavender-oobe-topbar-fix">
/* LAVENDER_OOBE_TOPBAR_FIX */
#oobe #oobe-card .oobe-topbar {
  background: linear-gradient(135deg,rgba(39,29,61,.98),rgba(22,16,36,.98)) !important;
  border-bottom: 1px solid rgba(167,139,250,.22) !important;
  color: #f5efff !important;
  border-radius: 19px 19px 0 0 !important;
}

#oobe #oobe-card .oobe-brand b {
  color: #f5efff !important;
}

#oobe #oobe-card .oobe-mslogo rect {
  fill: #c4b5fd !important;
}

#oobe #oobe-card .oobe-stepcount {
  color: #c4b5fd !important;
}

#oobe #oobe-card .oobe-footer,
#oobe #oobe-card .oobe-footer * {
  color: #c9bce2 !important;
}

#oobe #oobe-card .oobe-footer {
  border-top-color: rgba(167,139,250,.22) !important;
}
</style>
"""

head_end = s.lower().find("</head>")
if head_end < 0:
    sys.exit("STOP: Main document head not found.")

s = s[:head_end] + "\n" + css + "\n" + s[head_end:]
file.write_text(s)

print("Top bar recolored to dark purple.")
print("Windows logo recolored to lavender.")
print("Footer contrast improved.")
print("Backup:", backup.name)
