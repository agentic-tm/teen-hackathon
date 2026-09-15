#!/usr/bin/env python3
"""Build the Nokia sponsorship proposal: a six-page A4 PDF plus a self-contained HTML.

Every number lives in the BUDGET section. Fonts and logos in assets/ are embedded
as data URIs, so the HTML has no external dependencies. Run:

    python3 build.py            # writes ../nokia-sponsorship-map.html and .pdf

The PDF is printed with headless Chrome. Set CHROME_BIN to override the binary.
"""
import base64
import html
import os
import shutil
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
ASSETS = HERE / "assets"
OUT_HTML = HERE.parent / "nokia-sponsorship-map.html"
OUT_PDF = HERE.parent / "nokia-sponsorship-map.pdf"

# ---------------------------------------------------------------- BUDGET ----
USD_EUR = 0.86  # 1 USD in EUR, mid-September 2026

HIGH_SCHOOL = 140
UNIVERSITY = 60
PARTICIPANTS = HIGH_SCHOOL + UNIVERSITY
TEAM_SIZE = 2
TEAMS = PARTICIPANTS // TEAM_SIZE
MENTORS = 10
JUDGES = 6
STAFF = 14
PEOPLE_FED = PARTICIPANTS + MENTORS + JUDGES + STAFF

# Credits, USD per participant
CREDITS = [
    ("Cursor seat, one month", 40,
     "One workspace owned by the organizers. Central billing, spend limit per seat, "
     "no card from any student."),
    ("Frontier model usage", 50,
     "Claude, GPT and Gemini calls through Cursor or a team API key behind a gateway. "
     "This is the pool that empties on a hackathon weekend."),
    ("Sunday reserve", 10,
     "Released on Sunday morning to teams close to their cap. Unused reserve is not spent."),
]
CREDITS_PER_PERSON_USD = sum(v for _, v, _ in CREDITS)
CREDITS_TOTAL_USD = CREDITS_PER_PERSON_USD * PARTICIPANTS
CREDITS_TOTAL_EUR = round(CREDITS_TOTAL_USD * USD_EUR)

# Food, EUR per person, Friday evening to Sunday afternoon
MEALS = [
    ("Breakfast ×2", 2, 6),
    ("Lunch ×2", 2, 11),
    ("Dinner ×2", 2, 9),
    ("Coffee, water, snacks", 1, 12),
]
FOOD_PER_PERSON = sum(n * p for _, n, p in MEALS)
FOOD_TOTAL = FOOD_PER_PERSON * PEOPLE_FED

# Prizes, EUR, per team of two
PRIZES = [
    ("High school track", [("1st", 1500), ("2nd", 1000), ("3rd", 500)]),
    ("University track", [("1st", 1500), ("2nd", 1000), ("3rd", 500)]),
    ("Special awards", [("Nokia Challenge Award", 1000),
                        ("Best human-in-the-loop design", 400),
                        ("Community choice", 400)]),
]
PRIZES_TOTAL = sum(v for _, items in PRIZES for _, v in items)

SWAG_ITEMS = [
    ("T-shirts", PEOPLE_FED + 10, 7),
    ("Lanyards and badges", PEOPLE_FED + 10, 1.5),
    ("Stickers", 1, 160),
]
SWAG_TOTAL = round(sum(n * p for _, n, p in SWAG_ITEMS))

OTHER = [
    ("Print and signage", 700, "Four roll-ups, stage banner, posters, room signs"),
    ("Photo and video", 1000, "Photographer both days, one edited recap video"),
    ("Mentor and judge costs", 600, "Travel for out-of-town mentors, thank-you gifts"),
    ("Safety and first aid", 500, "Medical assistance on site, consent forms for minors"),
    ("Website and registration", 150, "Domain, hosting, registration and submissions"),
]

CONTINGENCY_RATE = 0.08

CASH_LINES = [
    ("Developer tooling credits", CREDITS_TOTAL_EUR, f"{'${:,}'.format(CREDITS_TOTAL_USD)} at {USD_EUR} EUR/USD, page 4"),
    ("Food and drinks", FOOD_TOTAL, f"{PEOPLE_FED} people × €{FOOD_PER_PERSON}: six meals plus coffee, water, snacks"),
    ("Prize pool", PRIZES_TOTAL, "Two tracks plus three special awards"),
    ("Swag", SWAG_TOTAL, f"T-shirts {PEOPLE_FED + 10} × €7, lanyards and badges, stickers"),
] + [(l, v, n) for l, v, n in OTHER]
CASH_SUBTOTAL = sum(v for _, v, _ in CASH_LINES)
CONTINGENCY = round(CASH_SUBTOTAL * CONTINGENCY_RATE)
CASH_TOTAL = CASH_SUBTOTAL + CONTINGENCY

IN_KIND = [
    ("Venue: amphitheatre, labs, network", "UPT / UVT", 4500),
    ("Dorm rooms for out-of-town participants", "UPT / UVT", 3600),
    ("Identity, site, media graphics", "agentic.tm", 2500),
    ("Mentoring, 10 mentors, two days", "agentic.tm, UPT, UVT", 10000),
]
IN_KIND_TOTAL = sum(v for _, _, v in IN_KIND)

TITLE_TIER = 25000
GOLD_TIER = 10000
SILVER_TIER = 5000
assert TITLE_TIER == CREDITS_TOTAL_EUR + PRIZES_TOTAL, "Title tier must equal credits + prizes"

# Credit funding scenarios, USD
SCENARIOS = [
    ("A. No provider help", [("Sponsor cash", 20000)]),
    ("B. Cursor credits", [("Sponsor cash", 10000), ("Cursor credits", 10000)]),
    ("C. Cursor + providers", [("Sponsor cash", 4000), ("Cursor credits", 10000),
                                        ("Model provider programs", 6000)]),
]

DATES = "Friday 27 to Sunday 29 November 2026"
VENUE = "UPT, Faculty of Automation and Computers, Bd. Vasile Parvan 2, Timisoara"
DECISION_BY = "15 October 2026"

# ---------------------------------------------------------------- STYLE -----
NAVY = "#0a1f44"      # agentic.tm mark background
BLUE = "#005aff"      # accent, Nokia blue
CYAN = "#00c2ff"      # agentic.tm robot
AMBER = "#e08a00"
GREEN = "#0f9d6e"
INK = "#0b1220"
INK2 = "#4b5565"
MUTED = "#8a93a3"
GRID = "#e3e7ee"
WASH = "#f3f6fb"


def eur(v):
    return f"€{round(v):,}"


def usd(v):
    return f"${round(v):,}"


def esc(s):
    return html.escape(str(s))


def data_uri(path, mime):
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode()


LOGOS = {
    "agentic": data_uri(ASSETS / "agentic-logo.png", "image/png"),
    "upt": data_uri(ASSETS / "upt-logo.svg", "image/svg+xml"),
    "uvt": data_uri(ASSETS / "uvt-logo.svg", "image/svg+xml"),
    "nokia": data_uri(ASSETS / "nokia-logo.svg", "image/svg+xml"),
}
FONTS = {
    "inter": data_uri(ASSETS / "fonts" / "Inter.woff2", "font/woff2"),
    "mono": data_uri(ASSETS / "fonts" / "JetBrainsMono.woff2", "font/woff2"),
}

MONO = "'JetBrains Mono', ui-monospace, Menlo, monospace"
SANS = "'Inter', system-ui, -apple-system, 'Segoe UI', sans-serif"


# ---------------------------------------------------------------- CHARTS ----
def hbar_chart(rows, width=560, bar_h=14, gap=7, label_w=200, value_fmt=eur, color=BLUE):
    max_value = max(v for _, v in rows)
    h = len(rows) * (bar_h + gap) + gap
    plot_w = width - label_w - 70
    out = [f'<svg viewBox="0 0 {width} {h}" width="{width}" height="{h}" font-family="{SANS}" font-size="9.5">']
    y = gap
    for label, v in rows:
        w = max(2, plot_w * v / max_value)
        out.append(f'<text x="{label_w - 8}" y="{y + bar_h * 0.72:.1f}" text-anchor="end" fill="{INK2}">{esc(label)}</text>')
        out.append(f'<rect x="{label_w}" y="{y}" width="{w:.1f}" height="{bar_h}" fill="{color}"/>')
        out.append(f'<rect x="{label_w + w - 3:.1f}" y="{y}" width="3" height="{bar_h}" fill="{color}" rx="2"/>')
        out.append(f'<text x="{label_w + w + 6:.1f}" y="{y + bar_h * 0.72:.1f}" fill="{INK}" font-family="{MONO}" font-size="9">{esc(value_fmt(v))}</text>')
        y += bar_h + gap
    out.append(f'<line x1="{label_w}" y1="{gap - 3}" x2="{label_w}" y2="{h - gap + 3}" stroke="#c9d0dc" stroke-width="1"/>')
    out.append("</svg>")
    return "\n".join(out)


def stacked_hbar_chart(rows, series_colors, width=560, bar_h=18, gap=9, label_w=170, value_fmt=usd):
    series = []
    for _, segs in rows:
        for s, _ in segs:
            if s not in series:
                series.append(s)
    max_total = max(sum(v for _, v in segs) for _, segs in rows)
    plot_w = width - label_w - 62
    h = len(rows) * (bar_h + gap) + gap + 20
    out = [f'<svg viewBox="0 0 {width} {h}" width="{width}" height="{h}" font-family="{SANS}" font-size="9.5">']
    y = gap
    for label, segs in rows:
        out.append(f'<text x="{label_w - 8}" y="{y + bar_h * 0.7:.1f}" text-anchor="end" fill="{INK2}">{esc(label)}</text>')
        x = label_w
        for s, v in segs:
            w = plot_w * v / max_total
            c = series_colors[series.index(s)]
            out.append(f'<rect x="{x:.1f}" y="{y}" width="{max(0, w - 2):.1f}" height="{bar_h}" fill="{c}"/>')
            if w > 56:
                out.append(f'<text x="{x + 5:.1f}" y="{y + bar_h * 0.7:.1f}" fill="#fff" font-family="{MONO}" font-size="8.5" font-weight="600">{esc(value_fmt(v))}</text>')
            x += w
        out.append(f'<text x="{x + 6:.1f}" y="{y + bar_h * 0.7:.1f}" fill="{INK}" font-family="{MONO}" font-size="9">{esc(value_fmt(sum(v for _, v in segs)))}</text>')
        y += bar_h + gap
    lx = label_w
    ly = y + 2
    for s in series:
        c = series_colors[series.index(s)]
        item_w = 13 + 5.2 * len(s) + 16
        if lx + item_w > width and lx > label_w:
            lx = label_w
            ly += 14
        out.append(f'<rect x="{lx:.1f}" y="{ly}" width="9" height="9" fill="{c}" rx="2"/>')
        out.append(f'<text x="{lx + 13:.1f}" y="{ly + 8}" fill="{INK2}" font-size="8.5">{esc(s)}</text>')
        lx += item_w
    out[0] = out[0].replace(f'viewBox="0 0 {width} {h}" width="{width}" height="{h}"',
                            f'viewBox="0 0 {width} {ly + 14}" width="{width}" height="{ly + 14}"')
    out.append("</svg>")
    return "\n".join(out)


def timeline_chart(phases, months, width=560, label_w=190, row_h=15, gap=5):
    plot_w = width - label_w - 10
    top = 18
    h = top + len(phases) * (row_h + gap) + 4
    out = [f'<svg viewBox="0 0 {width} {h}" width="{width}" height="{h}" font-family="{SANS}" font-size="9">']
    mw = plot_w / len(months)
    for i, m in enumerate(months):
        x = label_w + i * mw
        out.append(f'<text x="{x + mw / 2:.1f}" y="10" text-anchor="middle" fill="{MUTED}" font-family="{MONO}" font-size="8">{esc(m)}</text>')
        out.append(f'<line x1="{x:.1f}" y1="{top - 4}" x2="{x:.1f}" y2="{h - 2}" stroke="{GRID}" stroke-width="1"/>')
    y = top
    for label, s, e, c in phases:
        out.append(f'<text x="{label_w - 8}" y="{y + row_h * 0.72:.1f}" text-anchor="end" fill="{INK2}">{esc(label)}</text>')
        x1 = label_w + s * mw
        x2 = label_w + e * mw
        out.append(f'<rect x="{x1:.1f}" y="{y + 3}" width="{x2 - x1:.1f}" height="{row_h - 6}" fill="{c}" rx="2"/>')
        y += row_h + gap
    out.append("</svg>")
    return "\n".join(out)


def loop_diagram(size=270):
    """Human-in-the-loop ring: agent proposes, human decides, agent acts."""
    import math
    c = size / 2
    r = size * 0.28
    def pt(deg):
        a = math.radians(deg)
        return c + r * math.cos(a), c + r * math.sin(a)
    def arc(a1, a2, color):
        x1, y1 = pt(a1 + 14)
        x2, y2 = pt(a2 - 14)
        return (f'<path d="M {x1:.1f},{y1:.1f} A {r:.1f},{r:.1f} 0 0 1 {x2:.1f},{y2:.1f}" fill="none" '
                f'stroke="{color}" stroke-width="5" stroke-linecap="round" marker-end="url(#arr)"/>')
    top, right, left = pt(-90), pt(30), pt(150)
    out = [f'<svg viewBox="0 0 {size} {size}" width="{size}" height="{size}" font-family="{MONO}" font-size="9">',
           f'<defs><marker id="arr" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="3.2" markerHeight="3.2" orient="auto">'
           f'<path d="M0,0 L10,5 L0,10 z" fill="context-stroke"/></marker></defs>',
           f'<circle cx="{c}" cy="{c}" r="{r}" fill="none" stroke="{GRID}" stroke-width="5"/>',
           arc(-90, 30, BLUE), arc(30, 150, NAVY), arc(150, 270, NAVY)]
    for (x, y), col in ((top, CYAN), (right, BLUE), (left, NAVY)):
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="13" fill="{col}" stroke="#fff" stroke-width="3"/>')
    out.append(f'<text x="{top[0]:.1f}" y="{top[1] - 22:.1f}" text-anchor="middle" fill="{INK}" font-weight="600">agent proposes</text>')
    out.append(f'<text x="{right[0]:.1f}" y="{c + r + 16:.1f}" text-anchor="middle" fill="{INK}" font-weight="600">human decides</text>')
    out.append(f'<text x="{left[0]:.1f}" y="{c + r + 16:.1f}" text-anchor="middle" fill="{INK}" font-weight="600">agent acts</text>')
    out.append(f'<text x="{c}" y="{c - 3}" text-anchor="middle" fill="{INK2}" font-size="8">HUMAN IN</text>')
    out.append(f'<text x="{c}" y="{c + 9}" text-anchor="middle" fill="{INK2}" font-size="8">THE LOOP</text>')
    out.append('</svg>')
    return "\n".join(out)


# ---------------------------------------------------------------- STYLE -----
CSS = """
@font-face { font-family: 'Inter'; src: url(__INTER__) format('woff2'); font-weight: 100 900; font-style: normal; }
@font-face { font-family: 'JetBrains Mono'; src: url(__MONO__) format('woff2'); font-weight: 100 800; font-style: normal; }
@page { size: A4; margin: 0; }
* { box-sizing: border-box; }
html, body { margin: 0; padding: 0; background: #fff; color: __INK__;
  font-family: __SANS__; font-size: 9.6pt; line-height: 1.42;
  -webkit-print-color-adjust: exact; print-color-adjust: exact; }
.page { width: 210mm; height: 297mm; padding: 14mm 15mm 14mm 15mm; position: relative;
  page-break-after: always; overflow: hidden; background: #fff; }
.page:last-child { page-break-after: auto; }
.mono { font-family: __MONOF__; }
.kicker { font-family: __MONOF__; font-size: 7.5pt; letter-spacing: 0.14em; text-transform: uppercase;
  color: __BLUE__; font-weight: 600; margin: 0 0 2.5mm 0; }
h1 { font-size: 20pt; line-height: 1.12; margin: 0 0 4mm 0; font-weight: 800; letter-spacing: -0.02em; }
h2 { font-size: 10.5pt; margin: 0 0 2mm 0; font-weight: 700; letter-spacing: -0.005em; }
h2 .n { font-family: __MONOF__; font-weight: 500; color: __BLUE__; font-size: 9pt; margin-left: 2mm; }
h3 { font-size: 9.6pt; margin: 3.5mm 0 1.5mm 0; font-weight: 700; }
p { margin: 0 0 2.2mm 0; }
.lead { font-size: 10.6pt; color: __INK2__; line-height: 1.4; }
.small { font-size: 8pt; color: __INK2__; line-height: 1.38; }
table { border-collapse: collapse; width: 100%; font-size: 8.6pt; margin: 0 0 3mm 0; }
th, td { text-align: left; padding: 1.4mm 1.8mm; border-bottom: 1px solid __GRID__; vertical-align: top; }
th { font-family: __MONOF__; font-size: 6.8pt; text-transform: uppercase; letter-spacing: 0.08em; color: __MUTED__; font-weight: 500; }
td.num, th.num { text-align: right; font-family: __MONOF__; font-size: 8.4pt; white-space: nowrap; }
tr.total td { font-weight: 700; border-top: 1.5px solid __INK__; border-bottom: none; }
tr.sub td { color: __INK2__; }
td.note { color: __INK2__; font-size: 7.8pt; }
.cols { display: grid; grid-template-columns: 1fr 1fr; gap: 7mm; }
.cols3 { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 4mm; }
.tile { background: __WASH__; border-radius: 2mm; padding: 3mm 3.5mm; }
.tile .v { font-family: __MONOF__; font-size: 17pt; font-weight: 600; line-height: 1.05; color: __NAVY__; }
.tile .l { font-size: 7.8pt; color: __INK2__; margin-top: 1mm; line-height: 1.3; }
.callout { background: __WASH__; border-left: 2.5px solid __BLUE__; padding: 2.6mm 3.5mm; border-radius: 0 1.5mm 1.5mm 0; margin: 2.5mm 0 3mm 0; }
.callout p:last-child { margin-bottom: 0; }
ul { margin: 0 0 2.5mm 0; padding-left: 4mm; }
li { margin-bottom: 1mm; }
li::marker { color: __BLUE__; }
.foot { position: absolute; left: 15mm; right: 15mm; bottom: 8mm; display: flex; justify-content: space-between;
  align-items: center; border-top: 1px solid __GRID__; padding-top: 2.5mm; }
.foot .logos img { height: 6mm; margin-right: 4mm; vertical-align: middle; }
.foot .logos img.agentic { height: 6mm; border-radius: 1mm; }
.foot .pn { font-family: __MONOF__; font-size: 7.5pt; color: __MUTED__; }
svg { display: block; }
.chart { margin: 1mm 0 3mm 0; }

/* cover */
.cover { padding: 14mm 15mm; display: flex; flex-direction: column; }
.cover .top { display: flex; justify-content: space-between; align-items: center; }
.cover .top .org img { height: 11mm; margin-right: 6mm; vertical-align: middle; }
.cover .top .org img.agentic { height: 11mm; border-radius: 2mm; }
.cover .for { text-align: right; }
.cover .for .k { font-family: __MONOF__; font-size: 7pt; letter-spacing: 0.14em; text-transform: uppercase; color: __MUTED__; margin-bottom: 1.5mm; }
.cover .for img { height: 7mm; }
.cover .hero { display: grid; grid-template-columns: 1fr 70mm; gap: 4mm; align-items: center; margin-top: 42mm; }
.cover .toc { margin-top: 18mm; display: grid; grid-template-columns: repeat(5, 1fr); gap: 3mm; }
.cover .toc div { border-top: 2px solid __GRID__; padding-top: 2mm; font-size: 8pt; color: __INK2__; }
.cover .toc b { display: block; font-family: __MONOF__; font-size: 8pt; color: __BLUE__; margin-bottom: 0.8mm; }
.cover h1 { font-size: 34pt; line-height: 1.02; letter-spacing: -0.03em; margin: 0 0 5mm 0; }
.cover h1 span { color: __BLUE__; }
.cover .lead { font-size: 12pt; color: __INK2__; max-width: 110mm; }
.cover .tag { font-family: __MONOF__; font-size: 8.5pt; color: __BLUE__; font-weight: 500; margin-bottom: 4mm; }
.cover .band { margin-top: auto; background: __NAVY__; color: #fff; border-radius: 3mm; padding: 6mm 7mm; }
.cover .band .row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 5mm; }
.cover .band .v { font-family: __MONOF__; font-size: 19pt; font-weight: 600; line-height: 1; }
.cover .band .l { font-size: 7.8pt; color: #b9c6e0; margin-top: 1.5mm; line-height: 1.3; }
.cover .band .meta { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 5mm; margin-top: 6mm; padding-top: 4mm; border-top: 1px solid rgba(255,255,255,0.18); font-size: 8pt; color: #b9c6e0; }
.cover .band .meta b { display: block; color: #fff; font-family: __MONOF__; font-weight: 500; font-size: 7pt; letter-spacing: 0.12em; text-transform: uppercase; margin-bottom: 1mm; }

/* tiers */
.tiers { display: grid; grid-template-columns: 1.2fr 1fr 1fr; gap: 4mm; margin: 2mm 0 4mm 0; }
.tier { border: 1px solid __GRID__; border-radius: 2.5mm; padding: 3.5mm 4mm; }
.tier.top { border: 2px solid __BLUE__; background: __WASH__; }
.tier .name { font-weight: 700; font-size: 10pt; }
.tier .price { font-family: __MONOF__; font-size: 15pt; font-weight: 600; color: __BLUE__; margin: 1mm 0 2mm 0; }
.tier .funds { font-size: 8pt; color: __INK2__; margin-bottom: 2mm; min-height: 9mm; }
.tier ul { font-size: 8.2pt; padding-left: 3.5mm; }
.tier li { margin-bottom: 0.7mm; }
.pill { display: inline-block; font-family: __MONOF__; font-size: 6.8pt; letter-spacing: 0.1em; text-transform: uppercase; background: __BLUE__; color: #fff; padding: 0.6mm 2mm; border-radius: 1mm; margin-left: 2mm; vertical-align: middle; }
.sched td:first-child { font-family: __MONOF__; font-size: 8pt; white-space: nowrap; color: __INK2__; width: 20mm; }
.contact { display: flex; gap: 6mm; align-items: center; }
.contact .logos img { height: 8mm; margin-right: 4mm; vertical-align: middle; }
.contact .logos img.agentic { border-radius: 1.5mm; }
"""
for k, v in {"__INTER__": FONTS["inter"], "__MONO__": FONTS["mono"], "__MONOF__": MONO, "__SANS__": SANS,
             "__INK__": INK, "__INK2__": INK2, "__MUTED__": MUTED, "__GRID__": GRID, "__BLUE__": BLUE,
             "__NAVY__": NAVY, "__WASH__": WASH}.items():
    CSS = CSS.replace(k, v)

TOTAL_PAGES = 6
pages = []


def logos_html(cls=""):
    return (f'<img class="agentic" src="{LOGOS["agentic"]}" alt="agentic.tm">'
            f'<img src="{LOGOS["upt"]}" alt="UPT">'
            f'<img src="{LOGOS["uvt"]}" alt="UVT">')


def page(body, cls=""):
    n = len(pages) + 1
    foot = "" if cls == "cover" else (
        f'<div class="foot"><span class="logos">{logos_html()}</span>'
        f'<span class="pn">Sponsorship proposal for Nokia · {n} / {TOTAL_PAGES}</span></div>')
    pages.append(f'<section class="page {cls}">{body}{foot}</section>')


# 1. Cover ------------------------------------------------------------------
page(f"""
<div class="top">
  <div class="org">{logos_html()}</div>
  <div class="for"><div class="k">Prepared for</div><img src="{LOGOS['nokia']}" alt="Nokia"></div>
</div>
<div class="hero">
  <div>
    <div class="tag">// sponsorship proposal · Timisoara · 27-29 Nov 2026</div>
    <h1>Agentic<br>Programming<br>Hackathon<br><span>human in the loop</span></h1>
    <p class="lead">{PARTICIPANTS} high school and university students from western Romania spend a weekend
    building AI agents that keep a person in control. We propose Nokia as the Title Partner.</p>
  </div>
  <div>{loop_diagram(270)}</div>
</div>
<div class="toc">
  <div><b>01</b>The event and what Nokia gets</div>
  <div><b>02</b>Budget: cash and in kind</div>
  <div><b>03</b>The $20,000 credits line</div>
  <div><b>04</b>Sponsorship packages</div>
  <div><b>05</b>Plan, risks, next steps</div>
</div>
<div class="band">
  <div class="row">
    <div><div class="v">{PARTICIPANTS}</div><div class="l">participants<br>{HIGH_SCHOOL} high school, {UNIVERSITY} university</div></div>
    <div><div class="v">{TEAMS}</div><div class="l">teams of two<br>bring your own laptop</div></div>
    <div><div class="v">44h</div><div class="l">Friday 17:00 to<br>Sunday 16:00</div></div>
    <div><div class="v">{eur(TITLE_TIER)}</div><div class="l">proposed Title Partner<br>package for Nokia</div></div>
  </div>
  <div class="meta">
    <div><b>Organizers</b>agentic.tm · Politehnica University of Timisoara · West University of Timisoara</div>
    <div><b>Date</b>{DATES}</div>
    <div><b>Venue</b>{VENUE}. Dorms on the UPT student campus.</div>
  </div>
</div>
""", "cover")

# 2. The event and what Nokia gets ------------------------------------------
page(f"""
<p class="kicker">01 · The event and what Nokia gets</p>
<h1>Two days with {PARTICIPANTS} of the region's strongest young programmers</h1>
<div class="cols">
<div>
<h2>Human in the loop</h2>
<p>Students build AI agents that reason, plan and act, with a person guiding, approving or correcting
them at the points that matter. The agent proposes, the human decides. That is how the agent systems that
work in production are built: a coding agent that opens a pull request for review, a network agent that
proposes a change and waits for an engineer to approve it.</p>
<p>Teams get Cursor with frontier models and API access, choose their own stack, and ship a working demo by
Sunday noon. No fixed problem list. A Nokia Challenge track for teams that want a problem from Nokia's world.</p>
<h3>Who participates</h3>
<table>
<tr><th>Group</th><th class="num">People</th><th>From</th></tr>
<tr><td>High school, grades 9 to 12</td><td class="num">{HIGH_SCHOOL}</td><td>Timis, Arad, Caras-Severin, Hunedoara, through school inspectorates and the universities' school partnerships</td></tr>
<tr><td>University students</td><td class="num">{UNIVERSITY}</td><td>UPT and UVT, bachelor's and master's</td></tr>
<tr class="total"><td>Total</td><td class="num">{PARTICIPANTS}</td><td>{TEAMS} teams of {TEAM_SIZE}, two judging tracks</td></tr>
</table>
<p class="small">Participation is free. Minors bring a signed parental consent and an accompanying teacher per school
group. High school and university teams are judged separately.</p>
<h3>The weekend</h3>
<table class="sched">
<tr><td>Fri 27 Nov</td><td>17:00 check-in, opening, Nokia keynote, theme briefing. Hacking starts 19:00</td></tr>
<tr><td>Sat 28 Nov</td><td>Hacking all day. Mentor office hours, two short workshops, Nokia Challenge briefing</td></tr>
<tr><td>Sun 29 Nov</td><td>12:00 code freeze. Demos from 13:00 in two rooms, one per track. 15:30 awards, closing, group photo</td></tr>
</table>
<h3>Organizers</h3>
<p class="small"><b>agentic.tm</b> is Timisoara's agentic AI community: 250 members on Discord, 500+ on LinkedIn,
monthly meetups since October 2025. It brings the program, the mentors and the sponsors.
<b>UPT</b> hosts the event at the Faculty of Automation and Computers on Bd. Vasile Parvan and houses
out-of-town students in its dorms. <b>UPT</b> and <b>UVT</b> provide faculty mentors and judges and reach
their student bodies.</p>
</div>
<div>
<h2>What the Title Partner gets</h2>
<table>
<tr><th>Benefit</th><th>Detail</th></tr>
<tr><td>Naming</td><td>"Powered by Nokia" on the site, registration page, stage backdrop, T-shirts, badges, every post and press release</td></tr>
<tr><td>Keynote</td><td>20 minutes at Friday's opening, in front of every participant and teacher</td></tr>
<tr><td>Challenge track</td><td>A Nokia-defined problem, Nokia judges, the Nokia Challenge Award</td></tr>
<tr><td>Mentors</td><td>Up to five Nokia engineers on the mentor roster, with Nokia badges</td></tr>
<tr><td>Jury</td><td>Two seats on the main jury plus the challenge track jury</td></tr>
<tr><td>Recruiting</td><td>Opt-in CV book of participants over 18, a Nokia table at the venue both days</td></tr>
<tr><td>Report</td><td>Recap video, photo set, written report with numbers and projects, within two weeks</td></tr>
<tr><td>Community</td><td>A Nokia talk at an agentic.tm meetup before or after the event</td></tr>
</table>
<div class="callout"><p><b>Why this fits Nokia Timisoara.</b> The campus employs about 1,300 people, roughly 600 of
them R&amp;D engineers, and hires mostly from UPT. The {HIGH_SCHOOL} high school students in the room are
the UPT intake of 2027 to 2029. The {UNIVERSITY} university students are hires of 2027.</p></div>
<h3>Nokia Challenge track: Nokia picks one of these two briefs</h3>
<ul>
  <li><b>Incident triage with approval.</b> An agent reads alarms and logs from a simulated network, proposes
  a diagnosis and a fix, and waits for an engineer to approve before acting.</li>
  <li><b>Configuration review.</b> An agent reviews a proposed configuration change, explains the risk in plain
  language, and asks the human the one question that decides it.</li>
</ul>
<p class="small">Nothing runs on Nokia infrastructure. Tooling runs on participants' laptops against the providers'
APIs, so Nokia's internal restrictions on cloud agents do not touch the event.</p>
</div>
</div>
""")

# 3. Budget -------------------------------------------------------------------
budget_rows = [(l, v) for l, v, _ in CASH_LINES] + [("Contingency", CONTINGENCY)]
page(f"""
<p class="kicker">02 · Budget</p>
<h1>Where the money goes: {eur(CASH_TOTAL)} in cash, {eur(IN_KIND_TOTAL)} in kind</h1>
<p class="lead">The universities and agentic.tm cover the venue, the beds, the compute and the mentoring. Sponsors
cover what has to be bought: tooling credits, food, prizes, and the small lines.</p>
<div class="cols">
<div>
<div class="chart">{hbar_chart(budget_rows, width=322, label_w=132)}</div>
<table>
<tr><th>Cash line</th><th class="num">EUR</th></tr>
{''.join(f'<tr><td>{esc(l)}<br><span class="note" style="color:{INK2};font-size:7.6pt">{esc(n)}</span></td><td class="num">{eur(v)}</td></tr>' for l, v, n in CASH_LINES)}
<tr class="sub"><td>Subtotal</td><td class="num">{eur(CASH_SUBTOTAL)}</td></tr>
<tr><td>Contingency {int(CONTINGENCY_RATE * 100)}% <span class="note" style="font-size:7.6pt">price changes, no-shows, unspent is reported back</span></td><td class="num">{eur(CONTINGENCY)}</td></tr>
<tr class="total"><td>Total cash</td><td class="num">{eur(CASH_TOTAL)}</td></tr>
</table>
</div>
<div>
<h3 style="margin-top:0">Food and drinks, per person</h3>
<table>
<tr><th>Meal</th><th class="num">Count</th><th class="num">Each</th><th class="num">Sub</th></tr>
{''.join(f'<tr><td>{esc(l)}</td><td class="num">{n}</td><td class="num">{eur(p)}</td><td class="num">{eur(n * p)}</td></tr>' for l, n, p in MEALS)}
<tr class="total"><td>Per person, × {PEOPLE_FED}</td><td class="num"></td><td class="num">{eur(FOOD_PER_PERSON)}</td><td class="num">{eur(FOOD_TOTAL)}</td></tr>
</table>
<p class="small">{PARTICIPANTS} participants, {MENTORS} mentors, {JUDGES} judges, {STAFF} organizers and volunteers.
Friday dinner to Sunday lunch, catering delivered to the venue, vegetarian option at every meal.</p>
<h3>Prize pool</h3>
<table>
<tr><th>Track</th><th>Awards</th><th class="num">EUR</th></tr>
{''.join(f'<tr><td>{esc(t)}</td><td>{", ".join(f"{esc(a)} {eur(v)}" for a, v in items)}</td><td class="num">{eur(sum(v for _, v in items))}</td></tr>' for t, items in PRIZES)}
<tr class="total"><td>Total</td><td></td><td class="num">{eur(PRIZES_TOTAL)}</td></tr>
</table>
<p class="small">Per team of two. High school winners receive vouchers rather than cash, which avoids tax and
guardianship paperwork for minors. Nokia's judges hand out the Nokia Challenge Award.</p>
<p class="small">Rate {USD_EUR} EUR per USD, mid-September 2026. Food, print and swag are Timisoara supplier
estimates; final quotes follow the date.</p>
</div>
</div>
""")

# 4. Credits ------------------------------------------------------------------
credit_rows = [(l, v) for l, v, _ in CREDITS]
page(f"""
<p class="kicker">03 · The {usd(CREDITS_TOTAL_USD)} credits line</p>
<h1>{usd(CREDITS_PER_PERSON_USD)} per participant: what it buys, and who pays it</h1>
<div class="cols">
<div>
<h2>The split</h2>
<div class="chart">{hbar_chart(credit_rows, width=322, label_w=128, value_fmt=lambda v: f"${v} / person")}</div>
<table>
<tr><th>Component</th><th class="num">Each</th><th class="num">× {PARTICIPANTS}</th></tr>
{''.join(f'<tr><td>{esc(l)}<br><span style="color:{INK2};font-size:7.6pt">{esc(n)}</span></td><td class="num">{usd(v)}</td><td class="num">{usd(v * PARTICIPANTS)}</td></tr>' for l, v, n in CREDITS)}
<tr class="total"><td>Total</td><td class="num">{usd(CREDITS_PER_PERSON_USD)}</td><td class="num">{usd(CREDITS_TOTAL_USD)}</td></tr>
</table>
<h3>Why $100 and not $10</h3>
<p>A chat app that calls a model once per message costs cents. An agent turns one task into dozens of model
calls, each carrying the whole context of the code so far. A team using a frontier model in an agentic coding
tool for two days burns through $50 to $150 of usage at list prices. Cursor's own plans show the scale: the $20
plan includes $20 of model usage, the $60 plan $70, the $200 plan $400. We size the pool so a team does not run
dry on Saturday evening, and keep a reserve instead of giving everyone the maximum.</p>
<p class="small">With no credits at all, every team can still build on the providers' free tiers (Gemini, Mistral,
Groq, GitHub Models). The credits are what put frontier models and an agentic coding tool in their hands.</p>
</div>
<div>
<h2>Who pays it: three scenarios</h2>
<div class="chart">{stacked_hbar_chart(SCENARIOS, [BLUE, AMBER, GREEN], width=322, label_w=118)}</div>
<table>
<tr><th>Scenario</th><th>Assumption</th><th class="num">Cash</th></tr>
<tr><td><b>A</b></td><td>Every credit bought at list price. <b>The base case; the whole budget is priced on it.</b></td><td class="num">{usd(20000)}<br><span style="color:{INK2}">{eur(20000 * USD_EUR)}</span></td></tr>
<tr><td><b>B</b></td><td>Cursor's hackathon program grants $50 per participant, what it gave at its Boston Tech Week hackathon in May 2026. Application submitted; their stated answer time is "the next few weeks".</td><td class="num">{usd(10000)}<br><span style="color:{INK2}">{eur(10000 * USD_EUR)}</span></td></tr>
<tr><td><b>C</b></td><td>B plus $6,000 from Anthropic, OpenAI or Mistral programs, which gave $25 to $50 per participant at comparable events. Mistral request pending; the others go in once the date is locked.</td><td class="num">{usd(4000)}<br><span style="color:{INK2}">{eur(4000 * USD_EUR)}</span></td></tr>
</table>
<div class="callout"><p><b>What this means for Nokia.</b> Any credits granted by Cursor or a model provider reduce
the cash Nokia spends on this line, one for one, and the final split is in the post-event report. Nokia's package
does not grow if the applications fail.</p></div>
<h3>What Cursor can and cannot do</h3>
<ul>
  <li>Cursor grants credits to hackathons "that meet our criteria", case by case. No published amount; recent events got $50 per participant, or prize credits of $500 to $3,500.</li>
  <li>Cursor's free year for students closed to new sign-ups in June 2026. Cursor does not sponsor food, prizes or venues.</li>
  <li>Nokia's own Cursor licences stay out of it: cloud agent features are restricted on Nokia's network. The event runs its own workspace.</li>
</ul>
</div>
</div>
""")

# 5. Packages -----------------------------------------------------------------
page(f"""
<p class="kicker">04 · Sponsorship packages</p>
<h1>Three tiers. We propose the first one for Nokia.</h1>
<div class="tiers">
  <div class="tier top">
    <div class="name">Title Partner <span class="pill">proposed for Nokia</span></div>
    <div class="price">{eur(TITLE_TIER)}</div>
    <div class="funds">One slot. Funds the developer tooling credits ({eur(CREDITS_TOTAL_EUR)}) and the prize pool ({eur(PRIZES_TOTAL)}): the two lines that carry a sponsor's name in front of every participant.</div>
    <ul>
      <li>"Powered by Nokia" naming everywhere</li>
      <li>20-minute opening keynote</li>
      <li>Nokia Challenge track and award</li>
      <li>Up to five mentors, two jury seats</li>
      <li>Logo on T-shirts, badges, stage, site</li>
      <li>Recruiting table, opt-in CV book</li>
      <li>Recap video, photos, written report</li>
      <li>Talk slot at an agentic.tm meetup</li>
    </ul>
  </div>
  <div class="tier">
    <div class="name">Gold</div>
    <div class="price">{eur(GOLD_TIER)}</div>
    <div class="funds">Up to two slots. Funds food, or the media and swag package.</div>
    <ul>
      <li>30-minute workshop on Saturday</li>
      <li>Two mentors, one jury seat</li>
      <li>Logo on site, stage, T-shirts</li>
      <li>Recruiting table</li>
      <li>Named in press and social posts</li>
      <li>Report and photo set</li>
    </ul>
  </div>
  <div class="tier">
    <div class="name">Silver</div>
    <div class="price">{eur(SILVER_TIER)}</div>
    <div class="funds">No limit on slots. In-kind partners (caterer, print shop, hardware for prizes) get Silver benefits against the value they bring.</div>
    <ul>
      <li>Logo on site and stage</li>
      <li>Mention at opening and closing</li>
      <li>Swag in the participant bag</li>
      <li>Social media mention</li>
    </ul>
  </div>
</div>
<h2>How the budget closes</h2>
<div class="chart">{stacked_hbar_chart([("Cash budget", [("Nokia, Title", TITLE_TIER), ("Gold ×1", GOLD_TIER), ("Silver ×2", 2 * SILVER_TIER), ("Credit programs", CASH_TOTAL - TITLE_TIER - GOLD_TIER - 2 * SILVER_TIER)])], [BLUE, AMBER, GREEN, NAVY], width=560, label_w=100, value_fmt=eur)}</div>
<div class="cols">
<div>
<p>Gold and Silver conversations run in parallel with this one, starting with companies already active in
Timisoara's universities and tech scene. The last {eur(CASH_TOTAL - TITLE_TIER - GOLD_TIER - 2 * SILVER_TIER)} is
covered by any credit program approval, which lowers the credits line.</p>
</div>
<div>
<p><b>The decision we ask of Nokia:</b> Title Partner at {eur(TITLE_TIER)}, confirmed by {DECISION_BY}. On a yes,
a one-page agreement lists the benefits above, the amount and the reporting. Two invoices from the organizing
entity: {eur(TITLE_TIER // 2)} on signing in October, {eur(TITLE_TIER // 2)} in December with the report.</p>
</div>
</div>
<div class="cols">
<div>
<h2>In kind, already committed: {eur(IN_KIND_TOTAL)}</h2>
<table>
<tr><th>Contribution</th><th>From</th><th class="num">Value</th></tr>
{''.join(f'<tr><td>{esc(l)}</td><td>{esc(f)}</td><td class="num">{eur(v)}</td></tr>' for l, f, v in IN_KIND)}
<tr class="total"><td>Total in kind</td><td></td><td class="num">{eur(IN_KIND_TOTAL)}</td></tr>
</table>
<p class="small">Valued at what the organizers would otherwise pay for the same thing.</p>
</div>
<div>
<h2>What each tier funds</h2>
<table>
<tr><th>Tier</th><th>Covers</th></tr>
<tr><td>Title</td><td>Developer tooling credits {eur(CREDITS_TOTAL_EUR)} and the prize pool {eur(PRIZES_TOTAL)}</td></tr>
<tr><td>Gold</td><td>Food and drinks {eur(FOOD_TOTAL)}, or swag, print, photo and video together</td></tr>
<tr><td>Silver</td><td>Mentor and judge costs, safety, website, contingency</td></tr>
</table>
</div>
</div>

""")

# 6. Plan, risks, next steps ----------------------------------------------------
months = ["Sep", "Oct", "Nov", "Dec", "Jan"]
phases = [
    ("Sponsor decisions, Nokia first", 0.4, 1.3, BLUE),
    ("Credit applications, four providers", 0.3, 2.0, BLUE),
    ("Site, identity, registration", 1.2, 2.2, BLUE),
    ("School outreach, four counties", 1.3, 2.8, BLUE),
    ("Mentor recruiting and briefing", 1.0, 2.6, BLUE),
    ("Seats and credits provisioned", 2.0, 2.8, BLUE),
    ("Event, 27 to 29 November", 2.87, 3.0, NAVY),
    ("Report and showcase to sponsors", 3.1, 3.7, BLUE),
]
page(f"""
<p class="kicker">05 · Plan, risks, next steps</p>
<h1>From today to the event</h1>
<p class="lead">The event is on {DATES} at {VENUE}. Sponsor decisions
come first, because the sponsor's name goes on the site and the school announcements when they launch on 20 October.</p>
<div class="chart">{timeline_chart(phases, months, width=560, label_w=190)}</div>
<div class="cols">
<div>
<h2>Milestones</h2>
<table>
<tr><th>When</th><th>What</th></tr>
<tr><td class="mono" style="font-size:7.8pt;white-space:nowrap">by 20 Sep</td><td>This proposal reviewed with Nokia</td></tr>
<tr><td class="mono" style="font-size:7.8pt;white-space:nowrap">by 10 Oct</td><td>Cursor and Mistral answers on credits; Anthropic and OpenAI applications in</td></tr>
<tr><td class="mono" style="font-size:7.8pt;white-space:nowrap">by 15 Oct</td><td>Nokia confirms the Title package and picks the challenge brief; agreement signed</td></tr>
<tr><td class="mono" style="font-size:7.8pt;white-space:nowrap">by 20 Oct</td><td>Site live, registration open, first school announcements</td></tr>
<tr><td class="mono" style="font-size:7.8pt;white-space:nowrap">by 10 Nov</td><td>10 mentors briefed; Nokia Challenge brief final</td></tr>
<tr><td class="mono" style="font-size:7.8pt;white-space:nowrap">13 Nov</td><td>Registration closes, consent forms in, seats and credits provisioned, tooling tested end to end</td></tr>
<tr><td class="mono" style="font-size:7.8pt;white-space:nowrap">27-29 Nov</td><td>The event</td></tr>
<tr><td class="mono" style="font-size:7.8pt;white-space:nowrap">by 11 Dec</td><td>Report, video and project showcase to sponsors and press; second invoice</td></tr>
</table>
<h2>Team</h2>
<p class="small"><b>Vlad Temian</b>, agentic.tm: program, sponsors, credits. <b>Ovidiu Banias</b>: universities, date,
venue, accommodation. <b>Marius</b>, agentic.tm: identity, site, media. <b>Daniel Adrelean</b>, Nokia: liaison.</p>
</div>
<div>
<h2>Risks and what we do about them</h2>
<table>
<tr><th>Risk</th><th>Response</th></tr>
<tr><td>No provider grants credits</td><td>The budget assumes exactly that. Any grant is upside. The providers' free tiers guarantee every team can build.</td></tr>
<tr><td>Venue falls through</td><td>UVT's campus is the backup, same weekend. Sponsor money is not spent before the venue booking is signed.</td></tr>
<tr><td>Minors and accounts</td><td>Seats are created by the organizers, so no student signs a contract or enters a card. Parental consent covers participation and photos. Teacher per school group, medical assistance on site.</td></tr>
<tr><td>Fewer participants</td><td>Food, swag and credits scale with headcount. Unspent money is reported and returned or rolled into prizes, as the sponsor prefers.</td></tr>
<tr><td>Teams run out of credits</td><td>Per-seat caps stop one team draining the pool. The reserve covers Sunday. Free tiers are the fallback.</td></tr>
</table>
<div class="callout">
<p><b>Next step:</b> Nokia confirms the Title Partner package ({eur(TITLE_TIER)}) and picks one Nokia Challenge
brief by {DECISION_BY}. We send the one-page agreement the same week.</p>
<p style="margin-top:2mm"><b>Contact</b> · Vlad Temian, agentic.tm · <span class="mono">me@vtemian.com</span></p>
</div>
</div>
</div>
""")

assert len(pages) == TOTAL_PAGES, f"expected {TOTAL_PAGES} pages, got {len(pages)}"

# ---------------------------------------------------------------- WRITE -----
doc = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<title>Agentic Programming Hackathon Timisoara: sponsorship proposal for Nokia</title>
<style>{CSS}</style></head>
<body>
{''.join(pages)}
</body></html>"""
OUT_HTML.write_text(doc)
print(f"wrote {OUT_HTML}")


def find_chrome():
    env = os.environ.get("CHROME_BIN")
    if env:
        return env
    candidates = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "google-chrome", "google-chrome-stable", "chromium", "chromium-browser",
    ]
    for c in candidates:
        if os.path.isabs(c) and os.path.exists(c):
            return c
        if not os.path.isabs(c) and shutil.which(c):
            return shutil.which(c)
    return None


chrome = find_chrome()
if not chrome:
    raise SystemExit("no Chrome found; set CHROME_BIN")
subprocess.run([chrome, "--headless=new", "--disable-gpu", "--no-sandbox", "--no-pdf-header-footer",
                f"--print-to-pdf={OUT_PDF}", OUT_HTML.as_uri()], check=True, capture_output=True)
print(f"wrote {OUT_PDF}")
print(f"cash {eur(CASH_TOTAL)}  in-kind {eur(IN_KIND_TOTAL)}  credits {usd(CREDITS_TOTAL_USD)} = {eur(CREDITS_TOTAL_EUR)}  title {eur(TITLE_TIER)}")
