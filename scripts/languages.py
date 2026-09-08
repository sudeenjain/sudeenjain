#!/usr/bin/env python3
from pathlib import Path
import os, json, urllib.request, math, html
from collections import Counter
USER="sudeenjain"
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"assets"/"radar"
TOKEN=os.getenv("GITHUB_TOKEN","")
EXCLUDE={"HTML","CSS","Shell","Jupyter Notebook"}

def get(url):
    headers={"Accept":"application/vnd.github+json","User-Agent":"profile-readme"}
    if TOKEN:
        headers["Authorization"]=f"Bearer {TOKEN}"
    req=urllib.request.Request(url,headers=headers)
    with urllib.request.urlopen(req,timeout=30) as r:
        return json.load(r)

repos=get(f"https://api.github.com/users/{USER}/repos?per_page=100&type=owner")
totals=Counter()
for repo in repos:
    if repo.get("fork"): continue
    try:
        for lang,size in get(repo["languages_url"]).items():
            if lang not in EXCLUDE:
                totals[lang]+=size
    except Exception:
        pass
top=totals.most_common(6) or [("Python",1),("JavaScript",1),("PHP",1),("Java",1)]
mx=max(v for _,v in top)
labels=[k for k,_ in top]
values=[max(20,round(100*((v/mx)**0.5))) for _,v in top]

def render(dark):
    W=H=520; cx,cy,R=260,275,165
    bg="#0d1117" if dark else "#ffffff"
    fg="#e6edf3" if dark else "#24292f"
    grid="#30363d" if dark else "#d0d7de"
    accent="#ff4b2b"; n=len(labels)
    parts=[]; pts=[]; labs=[]
    for level in [.25,.5,.75,1]:
        ring=[]
        for i in range(n):
            a=-math.pi/2+2*math.pi*i/n
            ring.append(f"{cx+R*level*math.cos(a):.1f},{cy+R*level*math.sin(a):.1f}")
        parts.append(f'<polygon points="{" ".join(ring)}" fill="none" stroke="{grid}"/>')
    for i,(name,val) in enumerate(zip(labels,values)):
        a=-math.pi/2+2*math.pi*i/n
        x2,y2=cx+R*math.cos(a),cy+R*math.sin(a)
        parts.append(f'<line x1="{cx}" y1="{cy}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{grid}"/>')
        rr=R*val/100; pts.append((cx+rr*math.cos(a),cy+rr*math.sin(a)))
        lr=R+38; x,y=cx+lr*math.cos(a),cy+lr*math.sin(a)
        anchor="start" if math.cos(a)>.3 else ("end" if math.cos(a)<-.3 else "middle")
        labs.append(f'<text x="{x:.1f}" y="{y:.1f}" fill="{fg}" font-size="15" font-family="Arial" text-anchor="{anchor}" dominant-baseline="middle">{html.escape(name)}</text>')
    poly=" ".join(f"{x:.1f},{y:.1f}" for x,y in pts)
    dots="".join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="{accent}"/>' for x,y in pts)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}">
<rect width="100%" height="100%" rx="18" fill="{bg}"/>
<text x="260" y="38" fill="{fg}" font-size="22" font-weight="700" font-family="Arial" text-anchor="middle">GitHub Languages</text>
{''.join(parts)}
<polygon points="{poly}" fill="{accent}" fill-opacity=".18" stroke="{accent}" stroke-width="3"/>
{dots}{''.join(labs)}
</svg>'''
for dark in (True,False):
    (OUT/f"radar-langs-{'dark' if dark else 'light'}.svg").write_text(render(dark))
print("language radar updated")
