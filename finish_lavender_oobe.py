from pathlib import Path
from datetime import datetime
import re
import shutil
import sys

file = Path("LavenderOS.html")
s = file.read_text(errors="ignore")

marker = "LAVENDER_OOBE_FINAL_PALETTE"
if marker in s:
    sys.exit("This palette patch is already installed.")

head_end = s.lower().find("</head>")
body_start = s.lower().find("<body")

if head_end < 0 or body_start < 0 or head_end > body_start:
    sys.exit("STOP: Main document head could not be verified.")

if s[:head_end].count("<html") != 1:
    sys.exit("STOP: Main document boundary is ambiguous.")

css = r"""
<style id="lavender-oobe-final-palette">
/* LAVENDER_OOBE_FINAL_PALETTE */
#oobe {
  --accent: #a78bfa !important;
  --accent-press: #8b5cf6 !important;
  --accent-glow: rgba(167,139,250,.3) !important;
  color: #f4efff !important;
}

#oobe-card {
  background: linear-gradient(145deg,#211936 0%,#151020 65%,#100d19 100%) !important;
  border-color: rgba(167,139,250,.28) !important;
}

#oobe .oobe-header,
#oobe .oobe-footer {
  background: rgba(10,8,18,.48) !important;
  border-color: rgba(167,139,250,.2) !important;
}

#oobe .oobe-brand b,
#oobe .oobe-title,
#oobe .oobe-row,
#oobe .oobe-row-main b,
#oobe .oobe-font,
#oobe .oobe-wall,
#oobe .oobe-setting,
#oobe .oobe-chip,
#oobe .oobe-summary {
  color: #f3edff !important;
}

#oobe .oobe-subtitle,
#oobe .oobe-row-main > span,
#oobe .oobe-stepcount,
#oobe .oobe-note,
#oobe .oobe-wall-name {
  color: #c5b8dc !important;
}

#oobe .oobe-note,
#oobe .oobe-list,
#oobe .oobe-row,
#oobe .oobe-font,
#oobe .oobe-wall,
#oobe .oobe-setting,
#oobe .oobe-chip,
#oobe .oobe-avatar-chip,
#oobe .oobe-summary {
  background: rgba(35,27,53,.92) !important;
  border-color: rgba(167,139,250,.19) !important;
  border-radius: 10px !important;
}

#oobe .oobe-row:hover,
#oobe .oobe-font:hover,
#oobe .oobe-wall:hover,
#oobe .oobe-chip:hover {
  background: rgba(115,82,170,.22) !important;
  border-color: rgba(196,181,253,.42) !important;
}

#oobe .oobe-row.on,
#oobe .oobe-row[aria-pressed="true"],
#oobe .oobe-font.on,
#oobe .oobe-wall.on,
#oobe .oobe-chip.on,
#oobe .oobe-avatar-chip.on {
  background: rgba(139,92,246,.24) !important;
  border-color: #a78bfa !important;
  color: #fff !important;
}

#oobe .oobe-row-check,
#oobe .oobe-font-check {
  color: #c4b5fd !important;
}

#oobe .oobe-btn-primary {
  background: linear-gradient(135deg,#a78bfa,#7041c5) !important;
  border-color: #b9a1ff !important;
  color: #fff !important;
}

#oobe .oobe-btn-primary:hover {
  background: linear-gradient(135deg,#b69cff,#8054d6) !important;
}

#oobe .oobe-progress,
#oobe .oobe-progress i {
  background-color: rgba(167,139,250,.2) !important;
}

#oobe .oobe-progress i {
  background: linear-gradient(90deg,#8b5cf6,#c4b5fd) !important;
}

#oobe .oobe-step-dot.active {
  background: #b9a1ff !important;
  box-shadow: 0 0 12px rgba(167,139,250,.5) !important;
}

#oobe .text-input {
  background: #171222 !important;
  border-color: rgba(167,139,250,.35) !important;
  color: #f7f1ff !important;
}

#oobe .text-input:focus {
  background: #1d1630 !important;
  border-color: #a78bfa !important;
  box-shadow: 0 0 0 2px rgba(167,139,250,.2) !important;
}

#oobe .switch.on,
#oobe .oobe-avatar-cam,
#oobe .oobe-wall-check {
  background: #8b5cf6 !important;
}

#oobe .oobe-logo-icon {
  background: linear-gradient(135deg,#c4b5fd,#7041c5) !important;
  box-shadow: 0 4px 22px rgba(139,92,246,.35) !important;
}

#oobe .oobe-logo-icon svg {
  color: #fff !important;
  fill: #fff !important;
  stroke: #fff !important;
}

#oobe .oobe-list::-webkit-scrollbar-thumb {
  background: #66518d !important;
  border-color: #211936 !important;
}
</style>
"""

backup = file.with_name(
    file.name + ".before_oobe_final_palette_" +
    datetime.now().strftime("%Y%m%d_%H%M%S") + ".bak"
)
shutil.copy2(file, backup)

s = s[:head_end] + "\n" + css + "\n" + s[head_end:]
file.write_text(s)

print("LavenderOS wizard palette updated.")
print("Scoped to the setup wizard; desktop accent unchanged.")
print("Backup:", backup.name)
