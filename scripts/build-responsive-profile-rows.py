"""Build equal-width transparent rows; preserve existing individual artwork."""
from pathlib import Path
import subprocess
import tempfile
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets' / 'toolkit-bare'
SCRATCH = Path(tempfile.mkdtemp(prefix='profile-icon-raster-'))
ROWS = [
    ['python.png','javascript.png','html.png','css.png','flask.svg','bash.png',
     'git.png','github.png','github-actions.svg','visual_studio_code.png',
     'docker.png','cloud-run.svg','playwright.png','sqlite.png'],
    ['claude.svg','codex.svg','openai.svg','gemini.svg','pandas.png','numpy.png',
     'jupyter_notebook.png','scikit-learn.svg','power-bi.svg','tableau.svg',
     'linux.png','fedora.png','windows.png','macos.png'],
]
for theme in ['light', 'dark']:
    for number, names in enumerate(ROWS, 1):
        canvas = Image.new('RGBA', (1568, 112))
        for index, name in enumerate(names):
            source = ASSETS / name
            if theme == 'dark' and name in ['flask.svg','codex.svg','openai.svg']:
                source = source.with_name(source.stem + '-dark.svg')
            if source.suffix == '.svg':
                raster = SCRATCH / (source.stem + '.png')
                if not raster.exists():
                    subprocess.run(['inkscape', str(source), '--export-type=png',
                                    '--export-filename=' + str(raster),
                                    '--export-width=352'], check=True, capture_output=True)
                source = raster
            icon = Image.open(source).convert('RGBA')
            icon = icon.crop(icon.getchannel('A').getbbox())
            icon.thumbnail((88, 88), Image.Resampling.LANCZOS)
            canvas.alpha_composite(icon, (index * 112 + (112-icon.width)//2,
                                          (112-icon.height)//2))
        output = ASSETS / f'profile-row-{number}-{theme}.png'
        canvas.save(output)
        print(output)
print('Raster intermediates retained:', SCRATCH)
