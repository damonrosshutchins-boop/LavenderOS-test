from pathlib import Path
from datetime import datetime
import shutil
import sys

file = Path("LavenderOS.html")
html = file.read_text(encoding="utf-8")

old = """function setNav(id) {
  SET.cur = id;
  const a = openWindows.find(w => w.app.id === 'settings' && !w.closed);
  if (a) renderSettings(a.body);
}"""

new = """function setNav(id) {
  SET.cur = id;
  const a = openWindows.find(w => w.app.id === 'settings' && !w.closed);
  if (!a) return;

  const nav = a.body.querySelector('#set-nav');
  const body = a.body.querySelector('#set-body');

  if (!nav || !body) {
    renderSettings(a.body);
    return;
  }

  const search = nav.querySelector('#set-search');
  const searchValue = search ? search.value : '';

  renderNav(a.body);

  const nextSearch = a.body.querySelector('#set-search');
  if (nextSearch) {
    nextSearch.value = searchValue;
    if (searchValue) setSearch(searchValue);
  }

  renderBody(a.body);
}"""

if html.count(old) != 1:
    print("STOP: Expected setNav function was not found exactly once.")
    print("No changes made.")
    sys.exit(1)

backup = file.with_name(
    f"LavenderOS.html.before_settings_nav_{datetime.now():%Y%m%d_%H%M%S}.bak"
)
shutil.copy2(file, backup)

file.write_text(html.replace(old, new, 1), encoding="utf-8")

print("Settings navigation patch applied.")
print(f"Backup: {backup.name}")
