#!/usr/bin/env python3
"""Generates the skill radar (dark/light) SVGs. Banner: see generate_banner.py.
Edit assets/skills.json, then run:  python3 scripts/generate_assets.py"""
import json, math, os
from html import escape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = os.path.join(ROOT, "assets")
MONO = "SFMono-Regular,Consolas,'Liberation Mono',Menlo,monospace"
SANS = "-apple-system,'Segoe UI',Helvetica,Arial,sans-serif"

THEMES = {
    "dark":  dict(bg="#0D1117", win="#161B22", line="#30363D", text="#E6EDF3", mut="#8B949E",
                  green="#3FB950", blue="#58A6FF", dot="#58A6FF", dota=0.16, grid="#30363D"),
    "light": dict(bg="#F6F8FA", win="#FFFFFF", line="#D0D7DE", text="#1F2328", mut="#656D76",
                  green="#1A7F37", blue="#0969DA", dot="#0969DA", dota=0.14, grid="#D0D7DE"),
}

# ---------- radar ----------
def radar(name, t, axes):
    W, H, cx, cy, R = 620, 470, 310, 235, 150
    n = len(axes)
    ang = lambda i: -math.pi / 2 + i * 2 * math.pi / n
    pt = lambda i, r: (cx + r * math.cos(ang(i)), cy + r * math.sin(ang(i)))
    rings = ""
    for lv in range(1, 6):
        pts = " ".join(f"{pt(i, R*lv/5)[0]:.1f},{pt(i, R*lv/5)[1]:.1f}" for i in range(n))
        rings += f'<polygon points="{pts}" fill="none" stroke="{t["grid"]}" stroke-width="1"/>'
    spokes = "".join(f'<line x1="{cx}" y1="{cy}" x2="{pt(i,R)[0]:.1f}" y2="{pt(i,R)[1]:.1f}" stroke="{t["grid"]}"/>' for i in range(n))
    vals = [a["value"] for a in axes]
    poly = " ".join(f"{pt(i, R*v/5)[0]:.1f},{pt(i, R*v/5)[1]:.1f}" for i, v in enumerate(vals))
    dots = "".join(f'<circle cx="{pt(i,R*v/5)[0]:.1f}" cy="{pt(i,R*v/5)[1]:.1f}" r="4" fill="{t["blue"]}"/>' for i, v in enumerate(vals))
    labels = ""
    for i, a in enumerate(axes):
        x, y = pt(i, R + 26)
        c = math.cos(ang(i))
        anchor = "middle" if abs(c) < 0.3 else ("start" if c > 0 else "end")
        labels += f'<text class="lb" x="{x:.1f}" y="{y+5:.1f}" text-anchor="{anchor}">{escape(a["name"])}</text>'
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Self-rated skill radar chart">
<defs><style>
.lb{{font-family:{SANS};font-size:14px;font-weight:600;fill:{t['text']}}}
.sh{{transform-origin:{cx}px {cy}px;animation:grow 1.4s cubic-bezier(.2,.8,.2,1) both}}
@keyframes grow{{from{{transform:scale(0);opacity:0}}to{{transform:scale(1);opacity:1}}}}
</style></defs>
{rings}{spokes}
<g class="sh"><polygon points="{poly}" fill="{t['blue']}" fill-opacity="0.25" stroke="{t['blue']}" stroke-width="2.5" stroke-linejoin="round"/>{dots}</g>
{labels}
</svg>
'''

if __name__ == "__main__":
    axes = json.load(open(os.path.join(A, "skills.json")))["axes"]
    for name, t in THEMES.items():
        open(os.path.join(A, f"radar-{name}.svg"), "w").write(radar(name, t, axes))
    print("generated in", A)
