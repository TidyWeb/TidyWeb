"""Generate transparent monochrome variants for GitHub light/dark themes."""
from pathlib import Path
import re
import xml.etree.ElementTree as ET
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets' / 'toolkit-bare'
NS = 'http://www.w3.org/2000/svg'
ET.register_namespace('', NS)
icons = ET.parse(ROOT / 'assets' / 'toolkit' / 'toolkit-2.svg').getroot().findall(f'{{{NS}}}svg')
for index, name in [(3, 'flask'), (8, 'github-actions')]:
    icon = icons[index]
    icon.attrib.pop('x', None)
    icon.attrib.pop('y', None)
    with (OUT / f'{name}.svg').open('x') as handle:
        handle.write(ET.tostring(icon, encoding='unicode'))
for name in ['flask', 'codex', 'openai']:
    source = (OUT / f'{name}.svg').read_text()
    source = re.sub(r'fill="(?:#000000|#000|#111|black|currentColor)"', 'fill="#ffffff"', source)
    root = ET.fromstring(source)
    root.set('fill', '#ffffff')
    root.set('color', '#ffffff')
    with (OUT / f'{name}-dark.svg').open('x') as handle:
        handle.write(ET.tostring(root, encoding='unicode'))
