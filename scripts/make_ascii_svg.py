from pathlib import Path
from PIL import Image
from xml.sax.saxutils import escape

INPUT = Path("profile-prepped.png")
OUTPUT = Path("mallikarjuna-ascii.svg")

CHARS = " .,:;irsXA253hMHGS#9B&@"

COLS = 58
ROWS = 48

WIDTH = 370
HEIGHT = 370

img = Image.open(INPUT).convert("L")
img = img.resize((COLS, ROWS))

pixels = img.load()

lines = []

for y in range(ROWS):

    line = ""

    for x in range(COLS):

        brightness = pixels[x, y]

        position = int(
            (255 - brightness)
            / 255
            * (len(CHARS) - 1)
        )

        line += CHARS[position]

    lines.append(line.rstrip())

svg = f'''<svg xmlns="http://www.w3.org/2000/svg"
width="{WIDTH}" height="{HEIGHT}"
viewBox="0 0 {WIDTH} {HEIGHT}">

<style>

.row {{
    opacity: 0;
    animation: printRow 0.25s linear forwards;
}}

@keyframes printRow {{
    from {{
        opacity: 0;
        transform: translateX(-5px);
    }}

    to {{
        opacity: 1;
        transform: translateX(0);
    }}
}}

</style>

<rect width="100%" height="100%" rx="14" fill="#0d1117"/>

<rect
x="1"
y="1"
width="{WIDTH-2}"
height="{HEIGHT-2}"
rx="14"
fill="none"
stroke="#30363d"/>

<circle cx="22" cy="20" r="5" fill="#ff5f56"/>
<circle cx="40" cy="20" r="5" fill="#ffbd2e"/>
<circle cx="58" cy="20" r="5" fill="#27c93f"/>

<text
x="78"
y="25"
font-family="monospace"
font-size="12"
fill="#8b949e">
ASCII://mallikarjuna
</text>

'''

start_y = 49

for i, line in enumerate(lines):

    delay = i * 0.035

    svg += f'''
<text
class="row"
x="18"
y="{start_y + i * 6.3}"
font-family="monospace"
font-size="5.6"
fill="#c9d1d9"
xml:space="preserve"
style="animation-delay:{delay:.3f}s">
{escape(line)}
</text>
'''

svg += "</svg>"

OUTPUT.write_text(svg, encoding="utf-8")

print(f"Created {OUTPUT}")