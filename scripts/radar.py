#!/usr/bin/env python3
from pathlib import Path
import json, math, html
ROOT=Path(__file__).resolve().parents[1]
data=json.loads((ROOT/"assets"/"skills.json").read_text())
labels=list(data["skills"])
values=list(data["skills"].values())
OUT=ROOT/"assets"/"radar"

def render(dark):
    W=H=520; cx,cy,R=260,275,165
    bg="#0d1117" if dark else "#ffffff"
    fg="#e6edf3" if dark else "#24292f"
    grid="#30363d" if dark else "#d0d7de"
    accent="#ff4b2b"; n=len(labels)
    parts=[]
    for level in [.25,.5,.75,1]:
        pts=[]
        for i in range(n):
            a=-math.pi/2+2*math.pi*i/n
            pts.append(f"{cx+R*level*math.cos(a):.1f},{cy+R*level*math.sin(a):.1f}")
        parts.append(f'<polygon points="{" ".join(pts)}" fill="none" stroke="{grid}"/>')
    data_pts=[]; lab=[]
    for i,(name,val) in enumerate(zip(labels,values)):
        a=-math.pi/2+2*math.pi*i/n
        x2,y2=cx+R*math.cos(a),cy+R*math.sin(a)
        parts.append(f'<line x1="{cx}" y1="{cy}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{grid}"/>')
        rr=R*val/100
        data_pts.append((cx+rr*math.cos(a),cy+rr*math.sin(a)))
        lr=R+38; x,y=cx+lr*math.cos(a),cy+lr*math.sin(a)
        anchor="start" if math.cos(a)>.3 else ("end" if math.cos(a)<-.3 else "middle")
        lab.append(f'<text x="{x:.1f}" y="{y:.1f}" fill="{fg}" font-size="15" font-family="Arial" text-anchor="{anchor}" dominant-baseline="middle">{html.escape(name)}</text>')
    poly=" ".join(f"{x:.1f},{y:.1f}" for x,y in data_pts)
    dots="".join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="{accent}"/>' for x,y in data_pts)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}">
<rect width="100%" height="100%" rx="18" fill="{bg}"/>
<text x="260" y="38" fill="{fg}" font-size="22" font-weight="700" font-family="Arial" text-anchor="middle">Self-rated Skills</text>
{''.join(parts)}
<polygon points="{poly}" fill="{accent}" fill-opacity=".18" stroke="{accent}" stroke-width="3"/>
{dots}{''.join(lab)}
</svg>'''

for dark in (True,False):
    (OUT/f"radar-self-{'dark' if dark else 'light'}.svg").write_text(render(dark))
print("radar updated")
