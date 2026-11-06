
from pathlib import Path
from datetime import datetime

html = Path("LavenderOS.html")

if not html.exists():
    raise SystemExit("LavenderOS.html was not found.")

content = html.read_text(encoding="utf-8")
original = content

# Visible branding only. Internal code identifiers remain untouched.
replacements = {
    "SakuraVault": "LavenderOS",
    "Sakura OS": "LavenderOS",
    "SakuraOS": "LavenderOS",

    "sakura@sakuraos:~$": "lavender@lavenderos:~$",

    "Sakura petals, starry night, custom GIFs":
        "Ambient effects, starry night, custom GIFs",

    "Spinning Sakura": "Lavender Orbit",
    "Sakura Bloom": "Lavender Bloom",
    "Flor de Sakura": "Flor de Lavanda",
    "Floraison Sakura": "Floraison Lavande",
    "Fioritura Sakura": "Fioritura Lavanda",
    "Sakura-Blüte": "Lavendelblüte",
    "Sakura-bloesem": "Lavendelbloesem",
    "Kwiat wiśni": "Kwiat lawendy",
    "Sakura çiçeği": "Lavanta çiçeği",
    "桜の花": "ラベンダーの花",
    "樱花绽放": "薰衣草绽放",
    "زهر الساكورا": "زهرة اللافندر",

    'Default (Sakura OS)': 'Default (LavenderOS)',
    'cherry blossom favicon': 'LavenderOS favicon',
}

for old, new in replacements.items():
    content = content.replace(old, new)

if content == original:
    print("No visible branding changes were necessary.")
else:
    backup = html.with_name(
        f"LavenderOS.html.before_rebrand_{datetime.now():%Y%m%d_%H%M%S}.bak"
    )

    backup.write_text(original, encoding="utf-8")
    html.write_text(content, encoding="utf-8")

    print("LavenderOS branding pass completed.")
    print(f"Backup: {backup}")
    print(f"Replacements applied: {sum(original.count(k) for k in replacements)}")
