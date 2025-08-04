import sys
from datetime import datetime

filename = sys.argv[1]
species = sys.argv[2]

# index.html dosyasını oku
with open("index.html", "r", encoding="utf-8") as file:
    lines = file.readlines()

# Yeni satır (HTML linki)
now = datetime.now().strftime("%Y-%m-%d")
new_entry = f'    <li><a href="{filename}.html">{filename}</a> – <em>{species}</em> ({now})</li>\n'

# </ul> satırını bul ve hemen öncesine ekle
for i, line in enumerate(lines):
    if "</ul>" in line:
        lines.insert(i, new_entry)
        break

# Dosyayı tekrar yaz
with open("index.html", "w", encoding="utf-8") as file:
    file.writelines(lines)
