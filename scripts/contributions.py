#!/usr/bin/env python3
"""Render a GitHub-style contribution breakdown radar as a self-contained SVG.

Sums public contributions across every year the user has been active, then
draws the four-axis chart (commits / pull requests / code review / issues).
Reads the token from GH_TOKEN. Writes SVG to stdout.
"""
import json, os, sys, urllib.request
from datetime import datetime, timezone

USER = sys.argv[1] if len(sys.argv) > 1 else "lucaf"
TOKEN = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
FIRST_YEAR = 2023

def gql(query):
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": query}).encode(),
        headers={"Authorization": f"bearer {TOKEN}",
                 "Content-Type": "application/json",
                 "User-Agent": "profile-readme"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)

totals = {"commits": 0, "prs": 0, "reviews": 0, "issues": 0}
for year in range(FIRST_YEAR, datetime.now(timezone.utc).year + 1):
    q = f'''query {{ user(login: "{USER}") {{ contributionsCollection(
        from: "{year}-01-01T00:00:00Z", to: "{year}-12-31T23:59:59Z") {{
        totalCommitContributions
        totalPullRequestContributions
        totalPullRequestReviewContributions
        totalIssueContributions }} }} }}'''
    c = gql(q)["data"]["user"]["contributionsCollection"]
    totals["commits"] += c["totalCommitContributions"]
    totals["prs"]     += c["totalPullRequestContributions"]
    totals["reviews"] += c["totalPullRequestReviewContributions"]
    totals["issues"]  += c["totalIssueContributions"]

grand = sum(totals.values()) or 1
pct = {k: 100.0 * v / grand for k, v in totals.items()}

W, H, CX, CY, R = 560, 400, 280, 200, 132
SANS = ("-apple-system,BlinkMacSystemFont,&apos;Segoe UI&apos;,"
        "Helvetica,Arial,&apos;Liberation Sans&apos;,sans-serif")

# (key, label, unit dx, dy, label anchor, label offset)
AXES = [
    ("reviews", "Code review",  0, -1, "middle", (0, -22)),
    ("issues",  "Issues",       1,  0, "start",  (18, 5)),
    ("prs",     "Pull requests",0,  1, "middle", (0, 34)),
    ("commits", "Commits",     -1,  0, "end",    (-18, 5)),
]

axis_lines, points, dots, labels = [], [], [], []
for key, label, dx, dy, anchor, (lox, loy) in AXES:
    ex, ey = CX + dx * R, CY + dy * R
    axis_lines.append(f'<line class="ax" x1="{CX}" y1="{CY}" x2="{ex:.1f}" y2="{ey:.1f}"/>')
    r = R * (pct[key] / 100.0)
    px, py = CX + dx * r, CY + dy * r
    points.append(f"{px:.1f},{py:.1f}")
    dots.append(f'<circle class="pt" cx="{px:.1f}" cy="{py:.1f}" r="4"/>')
    labels.append(
        f'<text class="v" x="{ex+lox:.1f}" y="{ey+loy:.1f}" text-anchor="{anchor}">{pct[key]:.0f}%</text>'
        f'<text class="k" x="{ex+lox:.1f}" y="{ey+loy+19:.1f}" text-anchor="{anchor}">{label}</text>')

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Contribution breakdown: {pct['commits']:.0f}% commits, {pct['prs']:.0f}% pull requests, {pct['reviews']:.0f}% code review, {pct['issues']:.0f}% issues">
<style>
.ax{{stroke:#2f7d6f;stroke-width:1.5}}
.pt{{fill:#2f7d6f}}
.area{{fill:#2f7d6f;fill-opacity:.35;stroke:#2f7d6f;stroke-width:1.5}}
.v{{font-family:{SANS};font-size:17px;font-weight:600;fill:#1f2328}}
.k{{font-family:{SANS};font-size:14px;fill:#57606a}}
@media (prefers-color-scheme:dark){{
.ax{{stroke:#3fb950}} .pt{{fill:#3fb950}}
.area{{fill:#3fb950;fill-opacity:.3;stroke:#3fb950}}
.v{{fill:#e6edf3}} .k{{fill:#8b949e}}
}}
</style>
{"".join(axis_lines)}
<polygon class="area" points="{" ".join(points)}"/>
{"".join(dots)}
{"".join(labels)}
</svg>
'''
sys.stdout.write(svg)
