#!/usr/bin/env python3
"""Render a GitHub statistics card as a self-contained SVG.

Stars, forks, all-time contributions, lines of code changed, repository views
over the past two weeks, and repositories with contributions.
Reads GH_TOKEN. Writes SVG to stdout.
"""
import json, os, sys, time, urllib.request, urllib.error
from datetime import datetime, timezone

USER  = sys.argv[1] if len(sys.argv) > 1 else "lucaf"
TOKEN = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
HDRS  = {"Authorization": f"bearer {TOKEN}",
         "Accept": "application/vnd.github+json",
         "User-Agent": "profile-readme"}

def rest(path, retries=12):
    """GET with 202 handling: GitHub computes contributor stats asynchronously."""
    for attempt in range(retries):
        req = urllib.request.Request("https://api.github.com" + path, headers=HDRS)
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                if r.status == 202:
                    time.sleep(min(2 + attempt * 2, 15))
                    continue
                return r.status, json.load(r)
        except urllib.error.HTTPError as e:
            return e.code, None
    return 202, None

def gql(query):
    req = urllib.request.Request("https://api.github.com/graphql",
        data=json.dumps({"query": query}).encode(),
        headers={**HDRS, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)

# --- repositories: stars, forks -------------------------------------------
_, repos = rest(f"/users/{USER}/repos?per_page=100")
repos = repos or []
stars = sum(r["stargazers_count"] for r in repos)
forks = sum(r["forks_count"] for r in repos)

# --- lines changed + repos actually contributed to -------------------------
lines, contributed = 0, 0
for r in repos:
    code, data = rest(f"/repos/{USER}/{r['name']}/stats/contributors")
    if code != 200 or not data:
        continue
    mine = [c for c in data if (c.get("author") or {}).get("login", "").lower() == USER.lower()]
    if not mine:
        continue
    contributed += 1
    for c in mine:
        for w in c["weeks"]:
            lines += w["a"] + w["d"]

# --- repository views, past two weeks --------------------------------------
views, views_ok = 0, False
for r in repos:
    code, data = rest(f"/repos/{USER}/{r['name']}/traffic/views", retries=1)
    if code == 200 and data:
        views += data.get("count", 0)
        views_ok = True

# --- all-time contributions -------------------------------------------------
created = min((r["created_at"][:4] for r in repos), default="2016")
total_contrib = 0
for year in range(int(created), datetime.now(timezone.utc).year + 1):
    q = (f'query {{ user(login: "{USER}") {{ contributionsCollection('
         f'from: "{year}-01-01T00:00:00Z", to: "{year}-12-31T23:59:59Z") {{'
         f' contributionCalendar {{ totalContributions }} }} }} }}')
    try:
        total_contrib += gql(q)["data"]["user"]["contributionsCollection"]["contributionCalendar"]["totalContributions"]
    except Exception:
        pass

def n(v):
    return f"{v:,}"

ROWS = [
    ("star",   "Stars",           n(stars)),
    ("fork",   "Forks",           n(forks)),
    ("commit", "Contributions",   n(total_contrib)),
    ("diff",   "Lines changed",   n(lines)),
    ("eye",    "Views (14 days)", n(views) if views_ok else "n/a"),
    ("repo",   "Repos active in", n(contributed)),
]

# --- icons (16x16 viewport, drawn at each row) ------------------------------
ICONS = {
 "star":  '<path d="M8 .25l2.06 4.18 4.61.67-3.34 3.25.79 4.59L8 10.78l-4.12 2.16.79-4.59L1.33 5.1l4.61-.67z"/>',
 "fork":  '<path d="M5 3.25a1.75 1.75 0 11-3.5 0 1.75 1.75 0 013.5 0zm9.5 0a1.75 1.75 0 11-3.5 0 1.75 1.75 0 013.5 0zM8 14.5a1.75 1.75 0 110-3.5 1.75 1.75 0 010 3.5z"/><path d="M3.25 5v1.5c0 1 .75 1.75 1.75 1.75h6c1 0 1.75-.75 1.75-1.75V5M8 8.25v3.25" stroke-width="1.4" fill="none"/>',
 "commit":'<path d="M8 1.5a6.5 6.5 0 100 13 6.5 6.5 0 000-13zm0 1.5a5 5 0 110 10 5 5 0 010-10z"/><path d="M8 5.25v3.5M8 8.75h2.5" stroke-width="1.4" fill="none"/>',
 "diff":  '<path d="M7.25 2h1.5v3.25H12v1.5H8.75V10h-1.5V6.75H4v-1.5h3.25z"/><path d="M4 12.5h8v1.4H4z"/>',
 "eye":   '<path d="M8 3C4.5 3 1.7 5.4.8 7.6a1 1 0 000 .8C1.7 10.6 4.5 13 8 13s6.3-2.4 7.2-4.6a1 1 0 000-.8C14.3 5.4 11.5 3 8 3zm0 8.5A3.5 3.5 0 118 4.5a3.5 3.5 0 010 7zm0-1.8a1.7 1.7 0 100-3.4 1.7 1.7 0 000 3.4z"/>',
 "repo":  '<path d="M2.5 2.25A1.75 1.75 0 014.25 .5h8.25a1 1 0 011 1v10.25a1 1 0 01-1 1H4.5a.75.75 0 000 1.5h8a.75.75 0 010 1.5h-8A2 2 0 012.5 13.5z"/>',
}

SANS = ("-apple-system,BlinkMacSystemFont,&apos;Segoe UI&apos;,"
        "Helvetica,Arial,&apos;Liberation Sans&apos;,sans-serif")
W, PAD, TOP, RH = 300, 4, 54, 30
H = TOP + (len(ROWS) - 1) * RH + 22

body = []
y = TOP
for icon, label, value in ROWS:
    body.append(f'<g class="ic" transform="translate({PAD},{y-12}) scale(0.95)">{ICONS[icon]}</g>')
    body.append(f'<text class="l" x="{PAD+27}" y="{y}">{label}</text>')
    body.append(f'<text class="v" x="{W-PAD}" y="{y}" text-anchor="end">{value}</text>')
    y += RH

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="GitHub statistics for {USER}">
<style>
.t{{font-family:{SANS};font-size:17px;font-weight:700;fill:#2f81f7}}
.l{{font-family:{SANS};font-size:15px;font-weight:600;fill:#1f2328}}
.v{{font-family:{SANS};font-size:15px;fill:#57606a}}
.ic{{fill:#57606a;stroke:#57606a}}
@media (prefers-color-scheme:dark){{
.t{{fill:#58a6ff}} .l{{fill:#e6edf3}} .v{{fill:#8b949e}}
.ic{{fill:#8b949e;stroke:#8b949e}}
}}
</style>
<text class="t" x="{PAD}" y="28">GitHub Statistics</text>
{"".join(body)}
</svg>
'''
sys.stdout.write(svg)
