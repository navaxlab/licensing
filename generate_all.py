import os
import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

def get_rendered_html(url):
    options = Options()
    options.headless = True
    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(url)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )
    time.sleep(2)
    html = driver.page_source
    driver.quit()
    return html

def extract_species(html):
    soup = BeautifulSoup(html, 'html.parser')
    tag = soup.find(string=lambda text: text and "Object taxonomy" in text)
    if tag and tag.parent and tag.parent.find_next_sibling():
        return tag.parent.find_next_sibling().text.strip()
    return "UnknownSpecies"

def extract_metadata_from_html(html):
    soup = BeautifulSoup(html, 'html.parser')

    lookup = [
        ("Media ID", "Media ID"),
        ("Media type", "Media type"),
        ("Object element or part", "Object element or part"),
        ("Object represented", "Object represented"),
        ("Object taxonomy", "Object taxonomy"),
        ("Object organization", "Object organization"),
        ("Creator", "Creator"),
        ("Date created", "Date created"),
        ("Date uploaded", "Date uploaded"),
        ("File name", "File name"),
        ("File format(s)", "File format(s)"),
        ("File size", "File size"),
        ("Image width", "Image width"),
        ("Image height", "Image height"),
        ("Color space", "Color space"),
        ("Color depth", "Color depth"),
        ("Compression", "Compression"),
        ("Series type", "Series type"),
        ("X pixel spacing", "X Spacing"),
        ("Y pixel spacing", "Y Spacing"),
        ("Z pixel spacing", "Z Spacing"),
        ("Pixel spacing units", "Spacing Unit"),
        ("Modality", "Modality"),
        ("Device", "Device"),
        ("IP holder", "IP holder"),
        ("Permits commercial use", "Permits commercial use"),
        ("Permits 3D use", "Permits 3D use"),
        ("Funding attribution", "Funding attribution"),
        ("Cite as", "Cite as")
    ]

    metadata = {}
    for label, key in lookup:
        tag = soup.find(string=lambda text: text and label in text)
        if tag and tag.parent and tag.parent.find_next_sibling():
            value = tag.parent.find_next_sibling().text.strip()
            metadata[key] = value

    return metadata

def generate_html(metadata, nvx_code, species):
    spacing_html = f"""
    <div style='font-size:16px; margin-bottom:20px;'>
        <strong style='color:#990000;'>X Spacing:</strong> {metadata.get("X Spacing", "--")} {metadata.get("Spacing Unit", "--")}<br>
        <strong style='color:#990000;'>Y Spacing:</strong> {metadata.get("Y Spacing", "--")} {metadata.get("Spacing Unit", "--")}<br>
        <strong style='color:#990000;'>Z Spacing:</strong> {metadata.get("Z Spacing", "--")} {metadata.get("Spacing Unit", "--")}<br>
    </div>
    """

    source_link = f"<a href='https://www.morphosource.org/concern/media/{metadata.get('Media ID', '#')}' target='_blank'><button>View Original Source</button></a>"

    rows_html = ""
    for key, value in metadata.items():
        if value:
            rows_html += f"<tr><td style='padding: 8px; border: 1px solid #ccc; background-color: #f9f9f9;'><strong>{key}</strong></td><td style='padding: 8px; border: 1px solid #ccc;'>{value}</td></tr>"

    html_content = f"""
    <html>
    <head>
        <meta charset='UTF-8'>
        <title>{nvx_code} - {species}</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; }}
            table {{ border-collapse: collapse; width: 100%; margin-top: 20px; }}
            h1 {{ color: #333; }}
            button {{ padding: 8px 12px; background-color: #0066cc; color: white; border: none; border-radius: 4px; cursor: pointer; }}
        </style>
    </head>
    <body>
        <h1>{nvx_code} - {species}</h1>
        {source_link}
        {spacing_html}
        <table>{rows_html}</table>
    </body>
    </html>
    """

    with open(f"{nvx_code}.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"✔ HTML generated and saved as: {nvx_code}.html")

def main():
    if len(sys.argv) < 3:
        print("Usage: <url> <nvx_code>")
        return

    url = sys.argv[1]
    nvx_code = sys.argv[2]

    html = get_rendered_html(url)
    species = extract_species(html)
    metadata = extract_metadata_from_html(html)
    generate_html(metadata, nvx_code, species)

if __name__ == "__main__":
    main()
