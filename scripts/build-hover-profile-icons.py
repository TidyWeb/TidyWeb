"""Split approved rows into identical-size individual hover targets."""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets' / 'toolkit-bare'
OUT = ASSETS / 'responsive'
OUT.mkdir(exist_ok=True)
ROWS = [
    ['python','javascript','html','css','flask','bash','git','github',
     'github-actions','vscode','docker','cloud-run','playwright','sqlite'],
    ['claude','codex','openai','gemini','pandas','numpy','jupyter','scikit-learn',
     'power-bi','tableau','linux','fedora','windows','macos'],
]
for row, names in enumerate(ROWS, 1):
    light = Image.open(ASSETS / f'profile-row-{row}-light.png').convert('RGBA')
    dark = Image.open(ASSETS / f'profile-row-{row}-dark.png').convert('RGBA')
    assert light.size == dark.size == (1568, 112)
    for index, name in enumerate(names):
        box = (index * 112, 0, (index+1)*112, 112)
        with (OUT / f'{name}.png').open('xb') as handle:
            light.crop(box).save(handle, format='PNG')
        if name in ['flask', 'codex', 'openai']:
            with (OUT / f'{name}-dark.png').open('xb') as handle:
                dark.crop(box).save(handle, format='PNG')
