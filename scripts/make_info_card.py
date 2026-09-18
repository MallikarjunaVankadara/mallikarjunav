from pathlib import Path
from xml.sax.saxutils import escape

OUTPUT = Path("info-card.svg")

WIDTH = 490
HEIGHT = 370

rows = [
    ("NAME", "Mallikarjuna Vankadara"),
    ("ROLE", "Service Engineer"),
    ("FOCUS", "Product Thinking + AI"),
    ("DOMAIN", "Enterprise AI / Healthcare"),
    ("STRENGTH", "Customer Problems → Product Ideas"),
    ("DELIVERY", "Cross-functional Execution"),
    ("CLOUD", "Azure Region Delivery"),
    ("BACKGROUND", "Linux / Data Center Migration"),
]

svg = f'''<svg xmlns="http://www.w3.org/2000/svg"
width="{WIDTH}" height="{HEIGHT}"
viewBox="0 0 {WIDTH} {HEIGHT}">

<style>

text {{
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
}}

.line {{
    opacity: 0;
    animation: show 0.40s ease forwards;
}}

@keyframes show {{
    from {{
        opacity: 0;
        transform: translateX(-8px);
    }}

    to {{
        opacity: 1;
        transform: translateX(0);
    }}
}}

.cursor {{
    animation: blink 1s steps(2,start) infinite;
}}

@keyframes blink {{
    50% {{ opacity: 0; }}
}}

</style>

<rect width="100%" height="100%" rx="14" fill="#0d1117"/>

<rect x="1" y="1"
width="{WIDTH-2}"
height="{HEIGHT-2}"
rx="14"
fill="none"
stroke="#30363d"/>

<circle cx="22" cy="20" r="5" fill="#ff5f56"/>
<circle cx="40" cy="20" r="5" fill="#ffbd2e"/>
<circle cx="58" cy="20" r="5" fill="#27c93f"/>

<text x="78" y="25"
font-size="13"
fill="#8b949e">
mallikarjunav@github: ~
</text>

<text x="25" y="58"
font-size="14"
fill="#39d353">
$ neofetch
</text>

'''

y = 92

for i, (key, value) in enumerate(rows):

    delay = 0.15 + i * 0.16

    svg += f'''
<g class="line"
style="animation-delay:{delay}s">

<text x="25" y="{y}"
font-size="13"
fill="#58a6ff">
{escape(key)}
</text>

<text x="135" y="{y}"
font-size="13"
fill="#c9d1d9">
{escape(value)}
</text>

</g>
'''

    y += 31

svg += f'''

<text x="25" y="{HEIGHT-25}"
font-size="13"
fill="#39d353"
class="cursor">
█
</text>

</svg>
'''

OUTPUT.write_text(svg, encoding="utf-8")

print(f"Created {OUTPUT}")