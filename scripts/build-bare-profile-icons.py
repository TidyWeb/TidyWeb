"""Keep bare profile icons local; never overwrite an existing asset."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.request import urlopen
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets' / 'toolkit-bare'
COMMIT = '376c2f9b0ff0ebfcef3f9f5ca252e12c46b17057'
NAMES = ['python', 'javascript', 'html', 'css', 'flask', 'bash', 'git',
         'github', 'githubactions', 'visual_studio_code', 'docker',
         'playwright', 'sqlite', 'pandas', 'numpy', 'jupyter_notebook',
         'linux', 'fedora', 'windows', 'macos']
NS = 'http://www.w3.org/2000/svg'
ET.register_namespace('', NS)

def download(name):
    url = f'https://raw.githubusercontent.com/marwin1991/profile-technology-icons/{COMMIT}/icons/{name}.png'
    with urlopen(url, timeout=30) as response:
        data = response.read()
    with (OUT / f'{name}.png').open('xb') as handle:
        handle.write(data)
    return name

OUT.mkdir(parents=True, exist_ok=True)
for name in ThreadPoolExecutor(max_workers=6).map(download, NAMES):
    print(name)

# Reuse original, verified SVG artwork without its former tile or label.
for filename, selections in [
    ('toolkit-1.svg', {0:'claude',1:'codex',2:'openai',3:'gemini',
                       8:'scikit-learn',9:'power-bi',10:'tableau'}),
    ('toolkit-2.svg', {5:'cloud-run'}),
]:
    root = ET.parse(ROOT / 'assets' / 'toolkit' / filename).getroot()
    icons = root.findall(f'{{{NS}}}svg')
    for index, name in selections.items():
        icon = icons[index]
        icon.attrib.pop('x', None)
        icon.attrib.pop('y', None)
        icon.set('width', '36')
        icon.set('height', '36')
        with (OUT / f'{name}.svg').open('x') as handle:
            handle.write(ET.tostring(icon, encoding='unicode') + '\n')
        print(name)
