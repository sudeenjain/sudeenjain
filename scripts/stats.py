#!/usr/bin/env python3
from pathlib import Path
import os, json, urllib.request, html
from collections import Counter
USER="sudeenjain"
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"assets"/"stats"
TOKEN=os.getenv("GITHUB_TOKEN","")
def get(url):
    headers={"Accept":"application/vnd.github+json","User-Agent":"profile-readme"}
    if TOKEN: headers["Authorization"]=f"Bearer {TOKEN}"
    req=urllib.request.Request(url,headers=headers)
    with urllib.request.urlopen(req,timeout=30) as r:
        return json.load(r)
profile=get(f"https://api.github.com/users/{USER}")
repos=get(f"https://api.github.com/users/{USER}/repos?per_page=100&type=owner")
repos=[r for r in repos if not r.get("fork")]
stars=sum(r.get("stargazers_count",0) for r in repos)
forks=sum(r.get("forks_count",0) for r in repos)
langs=Counter(r.get("language") for r in repos if r.get("language"))
top=langs.most_common(1)[0][0] if langs else "-"
vals=[("Public repos",str(profile.get("public_repos",len(repos)))),("Total stars",str(stars)),("Total forks",str(forks)),("Top language",top)]
def render(dark):
    bg="#0d1117" if dark else "#ffffff"
    border="#30363d" if dark else "#d0d7de"
    fg="#e6edf3" if dark else "#24292f"
    muted="#8b949e" if dark else "#57606a"
    accent="#ff4b2b"
    cells=[]
    for i,(lab,val) in enumerate(vals):
        x=40+i*190
        cells.append(f'<text x="{x}" y="112" fill="{accent}" font-size="31" font-weight="700" font-family="Arial">{html.escape(val)}</text>')
        cells.append(f'<text x="{x}" y="143" fill="{muted}" font-size="15" font-family="Arial">{html.escape(lab)}</text>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="820" height="210">
<rect x="2" y="2" width="816" height="206" rx="22" fill="{bg}" stroke="{border}" stroke-width="3"/>
<text x="40" y="55" fill="{fg}" font-size="25" font-weight="700" font-family="Arial">GitHub Snapshot</text>
<text x="40" y="78" fill="{muted}" font-size="14" font-family="Arial">sudeenjain - auto-refreshed by GitHub Actions</text>
{''.join(cells)}
</svg>'''
for dark in (True,False):
    (OUT/f"github-snapshot-{'dark' if dark else 'light'}.svg").write_text(render(dark))
print("stats updated")
