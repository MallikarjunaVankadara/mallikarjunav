import json
from datetime import datetime
from pathlib import Path
from xml.sax.saxutils import escape

INPUT = Path("data/contributions.json")
OUTPUT = Path("contrib-heatmap.svg")

WIDTH = 860
HEIGHT = 220

CELL = 10
GAP = 3

COLORS = [
    "#161b22",
    "#0e4429",
    "#006d32",
    "#26a641",
    "#39d353",
]

data = json.loads(INPUT.read_text(encoding="utf-8"))
days = data.get("days", [])
username = data.get("username", "mallikarjunav")
total = data.get("total", 0)

svg = []

svg.append(
    f'''<svg xmlns="http://www.w3.org/2000/svg"
width="{WIDTH}" height="{HEIGHT}"
viewBox="0 0 {WIDTH} {HEIGHT}">

<style>
    .terminal {{
        font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
    }}

    .cell {{
        opacity: 0;
        animation: reveal 0.35s ease forwards;
    }}

    @keyframes reveal {{
        from {{
            opacity: 0;
            transform: translateY(6px);
        }}

        to {{
            opacity: 1;
            transform: translateY(0);
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
<rect x="1" y="1" width="{WIDTH-2}" height="{HEIGHT-2}"
      rx="14" fill="none" stroke="#30363d"/>

<circle cx="22" cy="20" r="5" fill="#ff5f56"/>
<circle cx="40" cy="20" r="5" fill="#ffbd2e"/>
<circle cx="58" cy="20" r="5" fill="#27c93f"/>

<text x="78" y="25"
      class="terminal"
      font-size="13"
      fill="#8b949e">
      {escape(username)}@github: ~/contributions
</text>

<text x="24" y="53"
      class="terminal"
      font-size="14"
      fill="#39d353">
      $ ./contributions.sh
</text>
'''
)

start_x = 45
start_y = 75

for index, day in enumerate(days[-371:]):
    week = index // 7
    weekday = index % 7

    x = start_x + week * (CELL + GAP)
    y = start_y + weekday * (CELL + GAP)

    level = max(0, min(int(day.get("level", 0)), 4))
    color = COLORS[level]

    delay = (week + weekday) * 0.015

    date = escape(str(day.get("date", "")))
    count = int(day.get("count", 0))

    svg.append(
        f'''
<rect
    class="cell"
    x="{x}"
    y="{y}"
    width="{CELL}"
    height="{CELL}"
    rx="2"
    fill="{color}"
    style="animation-delay:{delay:.3f}s">
    <title>{date}: {count} contributions</title>
</rect>
'''
    )

svg.append(
    f'''
<text x="45" y="190"
      class="terminal"
      font-size="12"
      fill="#8b949e">
      Contributions in displayed period:
</text>

<text x="275" y="190"
      class="terminal"
      font-size="12"
      fill="#39d353">
      {total}
</text>

<text x="45" y="211"
      class="terminal cursor"
      font-size="13"
      fill="#58a6ff">
      █
</text>

</svg>
'''
)

OUTPUT.write_text("".join(svg), encoding="utf-8")

print(f"Created {OUTPUT}")