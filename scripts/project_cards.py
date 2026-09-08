#!/usr/bin/env python3
from pathlib import Path
import json, html
ROOT=Path(__file__).resolve().parents[1]
items=json.loads((ROOT/"assets"/"projects.json").read_text())
OUT=ROOT/"assets"/"projects"
def card(p,dark):
    bg="#0d1117" if dark else "#ffffff"
    border="#30363d" if dark else "#d0d7de"
    fg="#e6edf3" if dark else "#24292f"
    muted="#8b949e" if dark else "#57606a"
    accent="#ff4b2b"
    tags=" · ".join(p["stack"])
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="840" height="300">
<rect x="2" y="2" width="836" height="296" rx="24" fill="{bg}" stroke="{border}" stroke-width="3"/>
<circle cx="52" cy="52" r="10" fill="{accent}"/>
<text x="78" y="61" fill="{fg}" font-size="30" font-weight="700" font-family="Arial">{html.escape(p["title"])}</text>
<text x="44" y="112" fill="{muted}" font-size="17" font-family="Arial">{html.escape(p["repo"])}</text>
<text x="44" y="162" fill="{fg}" font-size="19" font-family="Arial">{html.escape(p["description"])}</text>
<rect x="44" y="230" width="752" height="40" rx="20" fill="{accent}" fill-opacity=".12"/>
<text x="64" y="257" fill="{accent}" font-size="17" font-weight="600" font-family="Arial">{html.escape(tags)}</text>
</svg>'''
for p in items:
    for dark in (True,False):
        (OUT/f'{p["slug"]}-{"dark" if dark else "light"}.svg').write_text(card(p,dark))
print("project cards updated")
