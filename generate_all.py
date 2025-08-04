import sys
import requests
from bs4 import BeautifulSoup
import os

if len(sys.argv) < 4:
    print("Usage: python generate_all.py <morphosource_url> <filename> <species>")
    sys.exit(1)

url = sys.argv[1]
filename = sys.argv[2]
species = sys.argv[3]

# Sayfayı çek
response = requests.get(url)
if response.status_code != 200:
    print("Failed to fetch URL.")
    sys.exit(1)

soup = BeautifulSoup(response.text, "html.parser")

# Meta verileri çek
def extract_label(label):
    el = soup.find("dt", string=label)
    if el and el.find_next_sibling("dd"):
        return el.find_next_sibling("dd").text.strip()
    return "N/A"

media_id = url.split("/")[-1].split("?")[0]
specimen_code = extract_label("Specimen")
resolution = extract_label("Scan Resolution")

# HTML oluştur
html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{filename} | Licensing</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <h1>{filename}</h1>
  <div class="meta">
    <label>Species:</label>
    <span><em>{species}</em></span>

    <label>Specimen Code:</label>
    <span>{specimen_code}</span>

    <label>Organization:</label>
    <span>Florida Museum of Natural History</span>

    <label>Collection:</label>
    <span>Herpetology</span>

    <label>Media ID:</label>
    <span>{media_id}</span>

    <label>Type:</label>
    <span>Zipped TIFF Stack (Volumetric Data)</span>

    <label>Scan Resolution:</label>
    <span>{resolution}</span>

    <label>License:</label>
    <span>CC BY-NC 4.0</span>

    <label>Original Source:</label>
    <span>
      <a href="{url}" target="_blank">
        View on MorphoSource ↗
      </a>
    </span>
  </div>

  <div class="citation">
Florida Museum of Natural History. Specimen {specimen_code}.  
{species}. Herpetology Collection.  
Media ID: {media_id}. Accessed August 4, 2025.  
{url}
  </div>

  <footer>
    <p><a href="index.html">← Back to archive</a></p>
  </footer>
</body>
</html>"""

# Kaydet
with open(f"{filename}.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"{filename}.html created.")

# index.html güncelle (otomatik)
os.system(f'python update_index.py {filename} "{species}"')
