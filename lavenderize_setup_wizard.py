from pathlib import Path
from datetime import datetime
import shutil
import sys

file = Path("LavenderOS.html")
s = file.read_text(errors="ignore")

marker = 'id="lavender-oobe-theme"'
if marker in s:
    sys.exit("Theme patch already exists. No changes made.")

css = r"""
<style id="lavender-oobe-theme">
/* LavenderOS — Dark Setup Wizard */
#oobe {
  background:
    radial-gradient(ellipse at 50% 0%, rgba(109, 72, 190, .20), transparent 55%),
    radial-gradient(ellipse at 10% 90%, rgba(76, 40, 130, .13), transparent 45%),
    #07060d !important;
  color: #f1edff !important;
}

#oobe-card {
  background: linear-gradient(145deg,
    rgba(26, 20, 43, .98),
    rgba(13, 11, 23, .99) 65%,
    rgba(17, 13, 29, .99)) !important;
  border: 1px solid rgba(167, 139, 250, .22) !important;
  box-shadow:
    0 30px 100px rgba(0, 0, 0, .75),
    0 0 55px rgba(124, 83, 210, .10),
    inset 0 1px rgba(255, 255, 255, .035) !important;
  color: #f4efff !important;
  backdrop-filter: blur(30px) saturate(125%) !important;
  -webkit-backdrop-filter: blur(30px) saturate(125%) !important;
}

#oobe .oobe-header,
#oobe .oobe-footer {
  border-color: rgba(167, 139, 250, .15) !important;
}

#oobe .oobe-logo-icon {
  background: linear-gradient(135deg, #a78bfa, #7041c5) !important;
  box-shadow: 0 4px 22px rgba(139, 92, 246, .28) !important;
}

#oobe .oobe-brand span {
  background: rgba(139, 92, 246, .15) !important;
  color: #c4b5fd !important;
}

#oobe .oobe-title,
#oobe .oobe-brand b {
  color: #f5f0ff !important;
}

#oobe .oobe-subtitle {
  color: #aaa0c2 !important;
}

#oobe .oobe-step-dot {
  background: rgba(196, 181, 253, .17) !important;
}

#oobe .oobe-step-dot.active {
  background: #a78bfa !important;
  box-shadow: 0 0 15px rgba(167, 139, 250, .45) !important;
}

#oobe .oobe-step-dot.done {
  background: #8b72d6 !important;
}

/* Wizard controls */
#oobe button:not(.btn-danger) {
  border-color: rgba(167, 139, 250, .22);
}

#oobe button:not(.btn-danger):hover {
  border-color: rgba(167, 139, 250, .55) !important;
}

#oobe input:not([type="checkbox"]):not([type="radio"]),
#oobe select,
#oobe textarea {
  background: #100d1b !important;
  color: #eee7ff !important;
  border-color: rgba(167, 139, 250, .25) !important;
}

#oobe input::placeholder,
#oobe textarea::placeholder {
  color: #817794 !important;
}

#oobe input:focus,
#oobe select:focus,
#oobe textarea:focus {
  border-color: #a78bfa !important;
  outline-color: rgba(167, 139, 250, .25) !important;
}

#oobe input[type="checkbox"],
#oobe input[type="radio"] {
  accent-color: #a78bfa !important;
}

/* Selected options and cards */
#oobe .selected,
#oobe .active,
#oobe [aria-selected="true"] {
  border-color: #a78bfa !important;
}

#oobe ::selection {
  background: rgba(139, 92, 246, .4);
  color: white;
}

#oobe ::-webkit-scrollbar-thumb {
  background: rgba(167, 139, 250, .35);
  border-radius: 10px;
}

@media (prefers-reduced-motion: reduce) {
  #oobe-card {
    animation: none !important;
  }
}
</style>
"""

if "</head>" not in s.lower():
    sys.exit("STOP: Could not find the document head.")

import re
updated, count = re.subn(
    r"</head>",
    lambda m: css + "\n" + m.group(0),
    s,
    count=1,
    flags=re.I
)

if count != 1:
    sys.exit("STOP: Could not safely insert the theme.")

backup = file.with_name(
    file.name + ".before_oobe_lavender_" +
    datetime.now().strftime("%Y%m%d_%H%M%S") + ".bak"
)

shutil.copy2(file, backup)
file.write_text(updated)

print("Dark Lavender Setup Wizard theme installed.")
print("Only the setup wizard is targeted.")
print("Backup:", backup.name)
