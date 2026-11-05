"""Build self-contained profile tiles from existing SVG brand artwork."""

from pathlib import Path
import json
import re
import urllib.request
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "toolkit"
NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", NS)

def fetch(url):
    with urllib.request.urlopen(url, timeout=30) as response:
        return response.read()

catalogue = json.loads(fetch(
    "https://raw.githubusercontent.com/iconify/icon-sets/master/json/logos.json"
))
TOOLS = [
    ("Claude", "claude-icon"), ("Codex", "codex"),
    ("OpenAI", "openai-icon"), ("Gemini", "google-gemini-icon"),
    ("Python", "python"), ("pandas", "pandas-icon"),
    ("NumPy", "numpy"), ("Jupyter", "jupyter"),
    ("scikit-learn", None), ("Power BI", "microsoft-power-bi"),
    ("Tableau", "tableau-icon"), ("SQLite", "sqlite"),
    ("JavaScript", "javascript"), ("HTML", "html-5"),
    ("CSS", "css-3"), ("Flask", "flask"),
    ("Docker", "docker-icon"), ("Cloud Run", "google-cloud-run"),
    ("Git", "git-icon"), ("GitHub", "github-icon"),
    ("Actions", "github-actions"), ("VS Code", "visual-studio-code"),
    ("Linux", "linux-tux"), ("Bash", "bash-icon"),
]

def artwork(slug):
    if slug is None:
        element = ET.fromstring(fetch(
            "https://raw.githubusercontent.com/simple-icons/simple-icons/develop/icons/scikitlearn.svg"
        ))
        element.set("fill", "#f7931e")
        return element
    icon = catalogue["icons"][slug]
    width = icon.get("width", catalogue.get("width", 24))
    height = icon.get("height", catalogue.get("height", 24))
    return ET.fromstring(
        f'<svg xmlns="{NS}" viewBox="0 0 {width} {height}">{icon["body"]}</svg>'
    )

OUT.mkdir(parents=True, exist_ok=True)
for row in range(2):
    tools = TOOLS[row * 12:(row + 1) * 12]
    root = ET.Element(f"{{{NS}}}svg", {
        "width": "720", "height": "76", "viewBox": "0 0 720 76",
        "role": "img", "aria-label": ", ".join(label for label, _ in tools),
    })
    ET.SubElement(root, f"{{{NS}}}title").text = ", ".join(label for label, _ in tools)
    for index, (label, slug) in enumerate(tools):
        x = index * 60
        ET.SubElement(root, f"{{{NS}}}rect", {
            "x": str(x + 2), "y": "2", "width": "56", "height": "68",
            "rx": "10", "fill": "#eeeae2",
        })
        icon = artwork(slug)
        raw = ET.tostring(icon, encoding="unicode")
        for old in re.findall(r'\bid="([^"]+)"', raw):
            new = f"r{row}i{index}-{old}"
            raw = raw.replace(f'id="{old}"', f'id="{new}"')
            raw = raw.replace(f"url(#{old})", f"url(#{new})")
            raw = raw.replace(f'="#'+old+'"', f'="#'+new+'"')
        icon = ET.fromstring(raw)
        icon.attrib.update({"x": str(x + 12), "y": "10", "width": "36", "height": "36"})
        root.append(icon)
        text = ET.SubElement(root, f"{{{NS}}}text", {
            "x": str(x + 30), "y": "60", "text-anchor": "middle",
            "font-family": "DejaVu Sans,Arial,sans-serif", "font-size": "8",
            "fill": "#252a31",
        })
        text.text = label
    destination = OUT / f"toolkit-{row + 1}.svg"
    if destination.exists():
        raise FileExistsError(f"Retain existing artwork; choose a new output name: {destination}")
    destination.write_text(ET.tostring(root, encoding="unicode") + "\n")
    print(destination)
