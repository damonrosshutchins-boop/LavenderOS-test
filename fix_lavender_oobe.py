from pathlib import Path
from datetime import datetime
import shutil
import sys

file = Path("LavenderOS.html")
s = file.read_text(errors="ignore")

marker = "LAVENDER_OOBE_COMPLETE_THEME_V2"

if marker in s:
    sys.exit("This patch is already installed. Nothing changed.")

css = r"""
<style id="lavender-oobe-complete-theme">
/* LAVENDER_OOBE_COMPLETE_THEME_V2 */

/* Main wizard backdrop */
#oobe {
  background:
    radial-gradient(ellipse at 50% 0%, rgba(109, 65, 190, .22), transparent 58%),
    radial-gradient(ellipse at 50% 100%, rgba(74, 38, 130, .16), transparent 60%),
    #08070e !important;
  align-items: center !important;
  justify-content: center !important;
  padding: 24px !important;
}

/* Wide desktop setup window */
@media (min-width: 700px) {
  #oobe #oobe-card {
    width: min(1000px, 94vw) !important;
    max-width: 1000px !important;
    min-height: 590px !important;
    max-height: 90vh !important;
    height: auto !important;
    margin: auto !important;
    border-radius: 22px !important;
    border: 1px solid rgba(183, 148, 255, .25) !important;
    background: linear-gradient(145deg, #171321, #0d0b14 65%, #130e20) !important;
    box-shadow: 0 30px 100px rgba(0,0,0,.75),
                0 0 55px rgba(139,92,246,.10) !important;
    padding: 34px 42px 30px !important;
    color: #f5f0ff !important;
  }
}

/* Also defeat accidental phone sizing on larger screens */
@media (min-width: 700px) {
  html[data-device="phone"] #oobe {
    align-items: center !important;
    padding: 24px !important;
  }

  html[data-device="phone"] #oobe #oobe-card {
    width: min(1000px, 94vw) !important;
    max-width: 1000px !important;
    min-height: 590px !important;
    max-height: 90vh !important;
    height: auto !important;
    border-radius: 22px !important;
    padding: 34px 42px 30px !important;
    border: 1px solid rgba(183,148,255,.25) !important;
  }
}

/* Wizard interior */
#oobe #oobe-body-content,
#oobe #oobe-step-wrap {
  background: transparent !important;
  color: #f5f0ff !important;
}

#oobe .oobe-body,
#oobe .oobe-step-content {
  color: #f5f0ff !important;
}

/* Header and footer */
#oobe .oobe-header,
#oobe .oobe-footer {
  border-color: rgba(183,148,255,.20) !important;
  color: #e9ddff !important;
}

#oobe .oobe-brand b,
#oobe .oobe-title {
  color: #f7f1ff !important;
}

#oobe .oobe-subtitle,
#oobe .oobe-brand span {
  color: #b9accd !important;
}

/* Purple logo and progress */
#oobe .oobe-logo-icon {
  background: linear-gradient(135deg, #c4a5ff, #7744d1) !important;
  color: white !important;
  box-shadow: 0 4px 22px rgba(139,92,246,.3) !important;
}

#oobe .oobe-step-dot {
  background: rgba(196,181,253,.18) !important;
}

#oobe .oobe-step-dot.active,
#oobe .oobe-progress i {
  background: #a78bfa !important;
  box-shadow: 0 0 14px rgba(167,139,250,.4) !important;
}

#oobe .oobe-progress {
  background: #30263e !important;
}

/* Replace Windows blue and pale-blue selections */
#oobe .oobe-row.on,
#oobe .oobe-row[aria-pressed="true"],
#oobe .oobe-avatar-chip.on,
#oobe .oobe-font.on,
#oobe .oobe-wall.on,
#oobe .oobe-chip.on {
  background: rgba(139,92,246,.19) !important;
  border-color: #a78bfa !important;
  color: #f5edff !important;
}

#oobe .oobe-row-check,
#oobe .oobe-font-check {
  color: #c4a5ff !important;
}

/* Dark option cards and panels */
#oobe .oobe-row,
#oobe .oobe-avatar-chip,
#oobe .oobe-font,
#oobe .oobe-wall,
#oobe .oobe-chip,
#oobe .oobe-list,
#oobe .oobe-sum-cell,
#oobe .oobe-note,
#oobe .oobe-note-ok {
  background-color: #1b1725 !important;
  border-color: #393047 !important;
  color: #eee6fa !important;
}

#oobe .oobe-row:hover,
#oobe .oobe-avatar-chip:hover,
#oobe .oobe-font:hover,
#oobe .oobe-wall:hover,
#oobe .oobe-chip:hover {
  background-color: #292137 !important;
  border-color: #8061b4 !important;
}

/* Inputs */
#oobe .text-input,
#oobe input,
#oobe select,
#oobe textarea {
  background: #171320 !important;
  color: #f5efff !important;
  border-color: #49385f !important;
}

#oobe .text-input:focus,
#oobe input:focus,
#oobe select:focus,
#oobe textarea:focus {
  border-color: #a78bfa !important;
  box-shadow: 0 0 0 2px rgba(167,139,250,.18) !important;
}

#oobe input::placeholder,
#oobe textarea::placeholder {
  color: #8f829f !important;
}

/* Buttons */
#oobe .oobe-btn {
  background: #211b2d !important;
  border-color: #49385f !important;
  color: #eee6fa !important;
}

#oobe .oobe-btn:hover {
  background: #302440 !important;
  border-color: #8b6bc1 !important;
}

#oobe .oobe-btn-primary {
  background: linear-gradient(135deg, #9b72ed, #7041c5) !important;
  border-color: #a78bfa !important;
  color: #fff !important;
}

#oobe .oobe-btn-primary:hover {
  background: linear-gradient(135deg, #ad8afa, #8050d7) !important;
}

/* Switches */
#oobe .switch {
  background: #51475f !important;
}

#oobe .switch.on {
  background: #9569e8 !important;
}

/* Replace blue SVG/icon accents inside the wizard */
#oobe svg[fill="#0067c0"],
#oobe svg[fill="#0078d4"],
#oobe svg[style*="#0067c0"],
#oobe svg[style*="#0078d4"] {
  fill: #b99aff !important;
}

#oobe [style*="#0067c0"],
#oobe [style*="#0078d4"] {
  color: #b99aff !important;
  border-color: #a78bfa !important;
}

/* Keep the mobile wizard usable on actual narrow screens */
@media (max-width: 699px) {
  #oobe {
    padding: 0 !important;
  }

  #oobe #oobe-card {
    width: 100% !important;
    max-width: 100% !important;
    min-height: 100dvh !important;
    max-height: 100dvh !important;
    border-radius: 0 !important;
    padding: 18px 16px !important;
    background: #100d18 !important;
    color: #f5f0ff !important;
  }
}
</style>
"""

if "</head>" not in s.lower():
    sys.exit("STOP: Could not find </head>. Nothing changed.")

backup = file.with_name(
    file.name + ".before_oobe_complete_theme_" +
    datetime.now().strftime("%Y%m%d_%H%M%S") + ".bak"
)

shutil.copy2(file, backup)

pos = s.lower().rfind("</head>")
s = s[:pos] + css + "\n" + s[pos:]

file.write_text(s)

print("LavenderOS setup wizard theme installed.")
print("Desktop wizard: wider, centered, dark purple.")
print("White panels and blue accents: overridden.")
print("Mobile layout: preserved on narrow screens.")
print("Backup:", backup.name)	
