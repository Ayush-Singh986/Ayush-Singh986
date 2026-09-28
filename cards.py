#!/usr/bin/env python3
"""Builds the 'numbers' cards (stats + languages, dark and light) from LIVE GitHub data.
Runs in GitHub Actions with GITHUB_TOKEN (see .github/workflows/cards.yml).
Local:  GITHUB_TOKEN=<token> python3 cards.py
Only your own, non-fork public repos count toward stars and languages."""
import os, sys, json, urllib.request
from datetime import date
from html import escape

USER = os.environ.get("GH_USER", "Ayush-Singh986")
TOKEN = os.environ.get("GITHUB_TOKEN", "")
OUT = os.environ.get("OUT_DIR", os.path.dirname(os.path.abspath(__file__)))
SANS = "-apple-system,'Segoe UI',Helvetica,Arial,sans-serif"
FALLBACK_COLORS = {"HCL": "#844FBA", "Shell": "#89E051", "Python": "#3572A5", "Java": "#B07219",
                   "JavaScript": "#F1E05A", "HTML": "#E34C26", "CSS": "#563D7C", "Dockerfile": "#384D54",
                   "TypeScript": "#3178C6", "Go": "#00ADD8", "Makefile": "#427819", "Groovy": "#4298B8"}
THEMES = {
    "dark":  dict(fill="#0D1117", line="#30363D", text="#F0F6FC", mut="#8B949E", acc="#58A6FF"),
    "light": dict(fill="#FFFFFF", line="#D0D7DE", text="#1F2328", mut="#656D76", acc="#0969DA"),
}

def http(url, body=None):
    h = {"User-Agent": "profile-cards", "Accept": "application/vnd.github+json"}
    if TOKEN: h["Authorization"] = f"Bearer {TOKEN}"
    req = urllib.request.Request(url, data=json.dumps(body).encode() if body else None, headers=h)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)

def streaks(days):
    days = sorted(days)
    longest = run = 0
    for _, c in days:
        run = run + 1 if c > 0 else 0
        longest = max(longest, run)
    cur = 0
    for i, (d, c) in enumerate(reversed(days)):
        if c > 0: cur += 1
        elif i == 0 and d == date.today().isoformat(): continue  # today not counted yet
        else: break
    return cur, longest

def fetch_graphql():
    q = """query($login:String!){user(login:$login){
      followers{totalCount}
      all:repositories(ownerAffiliations:OWNER,privacy:PUBLIC){totalCount}
      own:repositories(ownerAffiliations:OWNER,privacy:PUBLIC,isFork:false,first:100){nodes{stargazerCount
        languages(first:10,orderBy:{field:SIZE,direction:DESC}){edges{size node{name color}}}}}
      contributionsCollection{contributionCalendar{totalContributions weeks{contributionDays{contributionCount date}}}}}}"""
    u = http("https://api.github.com/graphql", {"query": q, "variables": {"login": USER}})["data"]["user"]
    langs = {}
    for r in u["own"]["nodes"]:
        for e in r["languages"]["edges"]:
            n = e["node"]["name"]; b, c = langs.get(n, (0, e["node"]["color"]))
            langs[n] = (b + e["size"], c or FALLBACK_COLORS.get(n, "#8B949E"))
    cal = u["contributionsCollection"]["contributionCalendar"]
    days = [(d["date"], d["contributionCount"]) for w in cal["weeks"] for d in w["contributionDays"]]
    cur, longest = streaks(days)
    return dict(stars=sum(r["stargazerCount"] for r in u["own"]["nodes"]), repos=u["all"]["totalCount"],
                followers=u["followers"]["totalCount"], contribs=cal["totalContributions"], cur=cur,
                longest=longest, langs=sorted(((n, b, c) for n, (b, c) in langs.items()), key=lambda x: -x[1]))

def fetch_rest():  # fallback without token: no contributions / streaks
    u = http(f"https://api.github.com/users/{USER}")
    repos = [r for r in http(f"https://api.github.com/users/{USER}/repos?per_page=100&type=owner") if not r["fork"]]
    langs = {}
    for r in repos:
        for n, b in http(f"https://api.github.com/repos/{USER}/{r['name']}/languages").items():
            langs[n] = (langs.get(n, (0, ""))[0] + b, FALLBACK_COLORS.get(n, "#8B949E"))
    return dict(stars=sum(r["stargazers_count"] for r in repos), repos=u["public_repos"], followers=u["followers"],
                contribs=None, cur=None, longest=None,
                langs=sorted(((n, b, c) for n, (b, c) in langs.items()), key=lambda x: -x[1]))

def get_data():
    if "--demo" in sys.argv:   # sample numbers, layout preview only
        return dict(stars=4, repos=12, followers=9, contribs=180, cur=2, longest=9,
                    langs=[("HCL", 90000, "#844FBA"), ("Shell", 40000, "#89E051"), ("Python", 30000, "#3572A5"),
                           ("Java", 20000, "#B07219"), ("HTML", 9000, "#E34C26"), ("Dockerfile", 2000, "#384D54")])
    for fn in ((fetch_graphql,) if TOKEN else ()) + (fetch_rest,):
        try: return fn()
        except Exception as e: print("fetch failed:", fn.__name__, e, file=sys.stderr)
    return None

def fmt_size(b):
    return f"{b/1e6:.3g} MB" if b >= 1e6 else (f"{b/1e3:.3g} kB" if b >= 1e3 else f"{b} B")

def stats_card(t, d):
    v = lambda k: "–" if not d or d[k] is None else f"{d[k]:,}"
    cells = [("stars", "Total stars"), ("repos", "Public repos"), ("followers", "Followers"),
             ("contribs", "Contributions (1y)"), ("cur", "Current streak"), ("longest", "Longest streak")]
    out = ""
    for i, (k, lab) in enumerate(cells):
        x = 28 + (i % 3) * 190; y = 98 + (i // 3) * 60
        out += (f'<text class="n" x="{x}" y="{y}">{v(k)}</text><text class="l" x="{x}" y="{y+20}">{lab}</text>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="600" height="210" viewBox="0 0 600 210" role="img" aria-label="GitHub stats at a glance">
<style>.u{{font:700 18px {SANS};fill:{t['acc']}}}.g{{font:13px {SANS};fill:{t['mut']}}}.n{{font:700 30px {SANS};fill:{t['text']}}}.l{{font:12px {SANS};fill:{t['mut']}}}</style>
<rect x=".5" y=".5" width="599" height="209" rx="14" fill="{t['fill']}" stroke="{t['line']}"/>
<text class="u" x="28" y="40">{escape(USER)}</text><text class="g" x="572" y="40" text-anchor="end">at a glance</text>
<line x1="28" y1="54" x2="572" y2="54" stroke="{t['line']}"/>{out}
</svg>
'''

def langs_card(t, d):
    langs = d["langs"] if d else []
    total = sum(b for _, b, _ in langs) or 1
    top = langs[:8]; rows = (len(top) + 1) // 2
    H = 98 + max(rows - 1, 0) * 26 + 30 if top else 110
    head = f"{len(langs)} Languages" if langs else "Languages"
    body = ""
    if top:
        x = 28; segs = ""
        for n, b, c in top:
            w = max(2, 544 * b / total); segs += f'<rect x="{x:.1f}" y="52" width="{w:.1f}" height="8" fill="{c}"/>'; x += w
        rest = 544 - (x - 28)
        if rest > 1: segs += f'<rect x="{x:.1f}" y="52" width="{rest:.1f}" height="8" fill="{t["mut"]}"/>'
        body += f'<clipPath id="bc"><rect x="28" y="52" width="544" height="8" rx="4"/></clipPath><g clip-path="url(#bc)">{segs}</g>'
        for i, (n, b, c) in enumerate(top):
            cx = 28 + (i % 2) * 288; y = 98 + (i // 2) * 26
            body += (f'<circle cx="{cx+5}" cy="{y-4}" r="5" fill="{c}"/><text class="ln" x="{cx+18}" y="{y}">{escape(n)}</text>'
                     f'<text class="ls" x="{cx+205}" y="{y}" text-anchor="end">{fmt_size(b)}</text>'
                     f'<text class="ls" x="{cx+262}" y="{y}" text-anchor="end">{100*b/total:.2f}%</text>')
    else:
        body = f'<text class="ls" x="28" y="80">Numbers appear after the daily update runs.</text>'
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="600" height="{H}" viewBox="0 0 600 {H}" role="img" aria-label="Most used languages">
<style>.h{{font:600 15px {SANS};fill:{t['acc']}}}.ln{{font:14px {SANS};fill:{t['text']}}}.ls{{font:12px {SANS};fill:{t['mut']}}}</style>
<rect x=".5" y=".5" width="599" height="{H-1}" rx="14" fill="{t['fill']}" stroke="{t['line']}"/>
<text class="h" x="28" y="34">{head}</text><text class="ls" x="572" y="34" text-anchor="end">most used, by code size</text>{body}
</svg>
'''

if __name__ == "__main__":
    d = get_data()
    for name, t in THEMES.items():
        open(os.path.join(OUT, f"card-stats-{name}.svg"), "w").write(stats_card(t, d))
        open(os.path.join(OUT, f"card-languages-{name}.svg"), "w").write(langs_card(t, d))
    print("cards written to", OUT, "| live data" if d else "| placeholder (no data)")
