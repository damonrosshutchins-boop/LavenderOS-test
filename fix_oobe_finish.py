from pathlib import Path
from datetime import datetime
import re
import shutil
import subprocess
import sys

file = Path("LavenderOS.html")
s = file.read_text(errors="ignore")

if "LAVENDER_OOBE_FINISH_RECOVERY_V1" in s:
    sys.exit("Finish recovery is already installed.")

# Match the exact current wrapper, allowing whitespace differences.
pattern = re.compile(
    r"function\s+oobeFinish13\s*\(\s*\)\s*\{"
    r"\s*if\s*\(_coreOobeFinish\)\s*\{"
    r"\s*_coreOobeFinish\(\);\s*return;\s*\}"
    r"\s*S\.setupDone\s*=\s*true;"
    r"\s*S\.lastUsed\s*=\s*Date\.now\(\);"
    r"\s*save\(true\);"
    r"\s*bootDesktop\(\);"
    r"\s*\}"
    r"\s*window\.oobeFinish\s*=\s*oobeFinish13\s*;",
    re.S
)

matches = list(pattern.finditer(s))

if len(matches) != 1:
    sys.exit(
        f"STOP: Expected one original Finish wrapper; found {len(matches)}."
    )

replacement = r"""
function oobeFinish13() {
  /* LAVENDER_OOBE_FINISH_RECOVERY_V1 */
  if (window.__lavenderOobeFinishing) return;
  window.__lavenderOobeFinishing = true;

  try {
    // Prefer the original setup completion handler.
    if (typeof _coreOobeFinish === 'function') {
      try {
        _coreOobeFinish();
        return;
      } catch (err) {
        console.error('Original OOBE finish failed; recovering:', err);
      }
    }

    // Recover the user's selections if the original handler fails.
    try {
      if (typeof oobeCaptureName === 'function') oobeCaptureName();

      if (typeof S !== 'undefined' && S) {
        if (typeof oobeTempName !== 'undefined' && oobeTempName)
          S.username = oobeTempName;

        if (typeof oobeTempAvatar !== 'undefined' && oobeTempAvatar)
          S.userAvatar = oobeTempAvatar;

        if (typeof oobeTempBio !== 'undefined' && oobeTempBio)
          S.userBio = oobeTempBio;

        if (typeof oobeTempTheme !== 'undefined' && oobeTempTheme)
          S.wallpaper = oobeTempTheme;

        if (typeof oobeTempGlass !== 'undefined')
          S.glass = oobeTempGlass;

        if (typeof oobeTempCloak !== 'undefined')
          S.tabCloak = oobeTempCloak;

        if (typeof oobeTempPotato !== 'undefined')
          S.potatoMode = oobeTempPotato;

        if (typeof oobeTempCursor !== 'undefined')
          S.customCursor = oobeTempCursor;

        if (typeof oobeTempAnimations !== 'undefined')
          S.animations = oobeTempAnimations;

        if (typeof oobeTempLang !== 'undefined' && oobeTempLang)
          S.lang = oobeTempLang;

        if (typeof oobeTempFont !== 'undefined' && oobeTempFont)
          S.font = oobeTempFont;

        S.setupDone = true;
        S.lastUsed = Date.now();
      }
    } catch (err) {
      console.error('Could not restore all setup selections:', err);
    }

    // Apply each setting independently so one failure does not block startup.
    const applySteps = [
      () => typeof applyFont === 'function' && applyFont(),
      () => typeof applyAccent === 'function' && applyAccent(),
      () => typeof applyTheme === 'function' && applyTheme(),
      () => typeof applyGlass === 'function' && applyGlass(),
      () => typeof applyTabCloak === 'function' && applyTabCloak(),
      () => typeof applyWallpaper === 'function' && applyWallpaper(),
      () => typeof applyPotatoMode === 'function' && applyPotatoMode(),
      () => typeof applyCustomCursor === 'function' && applyCustomCursor(),
      () => typeof applyAnimations === 'function' && applyAnimations()
    ];

    for (const step of applySteps) {
      try {
        step();
      } catch (err) {
        console.error('A setup setting could not be applied:', err);
      }
    }

    try {
      if (typeof save === 'function') save(true);
    } catch (err) {
      console.error('Setup save failed:', err);
    }

    const host = document.getElementById('oobe');

    if (host) {
      host.classList.remove('show');
      host.style.display = 'none';
      host.innerHTML = '';
    }

    // Launch the desktop through the current 1.3 boot wrapper.
    if (typeof window.bootDesktop === 'function') {
      window.bootDesktop();
    } else if (typeof bootDesktop === 'function') {
      bootDesktop();
    }

  } finally {
    window.__lavenderOobeFinishing = false;
  }
}

window.oobeFinish = oobeFinish13;
""".strip()

updated = s[:matches[0].start()] + replacement + s[matches[0].end():]

# Check the modified script before saving.
scripts = re.findall(
    r'<script\b[^>]*>(.*?)</script\s*>',
    updated,
    re.I | re.S
)

target = [x for x in scripts if "LAVENDER_OOBE_FINISH_RECOVERY_V1" in x]

if len(target) != 1:
    sys.exit("STOP: Could not isolate the updated Finish script.")

temp = Path("/tmp/lavender-oobe-finish-check.js")
temp.write_text(target[0])

check = subprocess.run(
    ["node", "--check", str(temp)],
    capture_output=True,
    text=True
)

if check.returncode:
    sys.exit("STOP: JavaScript syntax error:\n" + check.stderr)

# Backup and write.
backup = file.with_name(
    file.name + ".before_oobe_finish_repair_" +
    datetime.now().strftime("%Y%m%d_%H%M%S") + ".bak"
)

shutil.copy2(file, backup)
file.write_text(updated)

print("LavenderOS Finish handler repaired.")
print("Original handler: retained with error recovery.")
print("Fallback: saves setup selections and launches desktop.")
print("JavaScript syntax check: passed.")
print("Previous wallpaper repairs: preserved.")
print("Backup:", backup.name)
