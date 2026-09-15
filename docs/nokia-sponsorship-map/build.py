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

# Prizes, EUR, per team of two
PRIZES = [
    ("High school track", [("1st place", 1500), ("2nd place", 1000), ("3rd place", 500)]),
    ("University track", [("1st place", 1500), ("2nd place", 1000), ("3rd place", 500)]),
    ("Special awards", [("Nokia Challenge Award", 1000),
                        ("Best human-in-the-loop", 400),
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
]

CONTINGENCY_RATE = 0.08

CASH_LINES = [
    ("Developer tooling credits", CREDITS_TOTAL_EUR, f"{'${:,}'.format(CREDITS_TOTAL_USD)}, detailed on page 4"),
    ("Prize pool", PRIZES_TOTAL, "Two tracks plus three special awards"),
    ("Swag", SWAG_TOTAL, f"T-shirts {PEOPLE_FED + 10} × €7, lanyards and badges, stickers"),
] + [(l, v, n) for l, v, n in OTHER]
CASH_SUBTOTAL = sum(v for _, v, _ in CASH_LINES)
CONTINGENCY = round(CASH_SUBTOTAL * CONTINGENCY_RATE)
CASH_TOTAL = CASH_SUBTOTAL + CONTINGENCY

TITLE_TIER = 25000
GOLD_TIER = 6500
SILVER_TIER = 2500
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
    "spacexai": data_uri(ASSETS / "spacexai-full-logo.svg", "image/svg+xml"),
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


def split_bar(parts, width=322, bar_h=18):
    """One bar split into labeled segments: (label, value, color)."""
    total = sum(v for _, v, _ in parts)
    h = bar_h + 30
    out = [f'<svg viewBox="0 0 {width} {h}" width="{width}" height="{h}" font-family="{SANS}" font-size="8.5">']
    x = 0
    for label, v, c in parts:
        w = width * v / total
        out.append(f'<rect x="{x:.1f}" y="0" width="{max(0, w - 2):.1f}" height="{bar_h}" fill="{c}"/>')
        out.append(f'<text x="{x + 6:.1f}" y="{bar_h * 0.7:.1f}" fill="#fff" font-family="{MONO}" font-size="9" font-weight="600">{v}</text>')
        out.append(f'<text x="{x:.1f}" y="{bar_h + 13}" fill="{INK2}">{esc(label)}</text>')
        x += w
    out.append("</svg>")
    return "\n".join(out)


def schedule_chart(width=322):
    """Three day strips, hours across, one labeled block per activity."""
    days = [
        ("Fri 27", [(17, 19, "17:00 opening, keynote", NAVY), (19, 24, "hacking", BLUE)]),
        ("Sat 28", [(0, 24, "hacking, workshops, mentor office hours", BLUE)]),
        ("Sun 29", [(0, 12, "hacking", BLUE), (12, 16, "12:00 freeze · 13:00 demos · 15:30 awards", GREEN)]),
    ]
    label_w = 44
    row_h = 16
    gap = 14
    top = 12
    plot_w = width - label_w - 4
    h = top + len(days) * (row_h + gap)
    out = [f'<svg viewBox="0 0 {width} {h}" width="{width}" height="{h}" font-family="{SANS}" font-size="8">']
    for hr in (0, 6, 12, 18, 24):
        x = label_w + plot_w * hr / 24
        out.append(f'<text x="{x:.1f}" y="8" text-anchor="middle" fill="{MUTED}" font-family="{MONO}" font-size="7">{hr:02d}:00</text>')
        out.append(f'<line x1="{x:.1f}" y1="{top}" x2="{x:.1f}" y2="{h - gap + 2}" stroke="{GRID}" stroke-width="1"/>')
    y = top + 2
    for d, blocks in days:
        out.append(f'<text x="{label_w - 8}" y="{y + row_h * 0.72:.1f}" text-anchor="end" fill="{INK2}" font-family="{MONO}">{d}</text>')
        below = []
        for a, b, txt, c in blocks:
            x1 = label_w + plot_w * a / 24
            w = plot_w * (b - a) / 24
            out.append(f'<rect x="{x1:.1f}" y="{y}" width="{max(0, w - 1.5):.1f}" height="{row_h}" fill="{c}" rx="2"/>')
            if w > 4.6 * len(txt) + 8:
                out.append(f'<text x="{x1 + 4:.1f}" y="{y + row_h * 0.7:.1f}" fill="#fff" font-weight="600">{esc(txt)}</text>')
            else:
                below.append((x1 + w / 2, txt))
        for k, (bx, txt) in enumerate(below):
            anchor = "end" if bx > label_w + plot_w * 0.55 else "middle"
            bx = min(bx + 40, label_w + plot_w) if anchor == "end" else bx
            out.append(f'<text x="{bx:.1f}" y="{y + row_h + 9}" text-anchor="{anchor}" fill="{INK2}">{esc(txt)}</text>')
        y += row_h + gap
    out.append("</svg>")
    return "\n".join(out)


def grouped_hbar(rows, colors, width=322, label_w=80, bar_h=8, gap=3, group_gap=8):
    """rows: (label, [(series, value), ...]) drawn as thin bars per group with a legend."""
    series = [s for s, _ in rows[0][1]]
    max_v = max(v for _, segs in rows for _, v in segs)
    plot_w = width - label_w - 50
    n = len(series)
    gh = n * bar_h + (n - 1) * gap
    h = len(rows) * (gh + group_gap) + 18
    out = [f'<svg viewBox="0 0 {width} {h}" width="{width}" height="{h}" font-family="{SANS}" font-size="8.5">']
    y = 0
    for label, segs in rows:
        out.append(f'<text x="{label_w - 8}" y="{y + gh / 2 + 3:.1f}" text-anchor="end" fill="{INK2}">{esc(label)}</text>')
        for k, (sname, v) in enumerate(segs):
            w = plot_w * v / max_v
            yy = y + k * (bar_h + gap)
            out.append(f'<rect x="{label_w}" y="{yy}" width="{w:.1f}" height="{bar_h}" fill="{colors[k]}" rx="1"/>')
            out.append(f'<text x="{label_w + w + 5:.1f}" y="{yy + bar_h - 1}" fill="{INK}" font-family="{MONO}" font-size="8">${v}</text>')
        y += gh + group_gap
    lx = label_w
    for k, sname in enumerate(series):
        out.append(f'<rect x="{lx}" y="{y + 2}" width="8" height="8" fill="{colors[k]}" rx="2"/>')
        out.append(f'<text x="{lx + 12}" y="{y + 9}" fill="{INK2}" font-size="8">{esc(sname)}</text>')
        lx += 12 + 5 * len(sname) + 14
    out.append("</svg>")
    return "\n".join(out)


def grouped_prize_chart(groups, width=322, bar_h=11, gap=5, label_w=120):
    """Bars grouped under a header per track: (track, [(award, value), ...])."""
    max_v = max(v for _, items in groups for _, v in items)
    plot_w = width - label_w - 60
    h = sum(14 + len(items) * (bar_h + gap) + 6 for _, items in groups)
    out = [f'<svg viewBox="0 0 {width} {h}" width="{width}" height="{h}" font-family="{SANS}" font-size="8.5">']
    y = 0
    for track, items in groups:
        out.append(f'<text x="0" y="{y + 9}" fill="{NAVY}" font-family="{MONO}" font-size="7.5" font-weight="600">{esc(track.upper())}</text>')
        y += 14
        for award, v in items:
            w = plot_w * v / max_v
            out.append(f'<text x="{label_w - 8}" y="{y + bar_h * 0.78:.1f}" text-anchor="end" fill="{INK2}">{esc(award)}</text>')
            out.append(f'<rect x="{label_w}" y="{y}" width="{w:.1f}" height="{bar_h}" fill="{BLUE}" rx="1.5"/>')
            out.append(f'<text x="{label_w + w + 5:.1f}" y="{y + bar_h * 0.78:.1f}" fill="{INK}" font-family="{MONO}" font-size="8.5">{eur(v)}</text>')
            y += bar_h + gap
        y += 6
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
.cols { display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); gap: 7mm; }
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

.benefits { display: grid; grid-template-columns: 1fr 1fr; gap: 2.5mm; margin: 1mm 0 3mm 0; }
.benefits .b { background: __WASH__; border-radius: 2mm; padding: 2.4mm 3mm; border-left: 2.5px solid __BLUE__; }
.benefits .t { font-family: __MONOF__; font-weight: 600; font-size: 8.6pt; color: __NAVY__; }
.benefits .d { font-size: 7.8pt; color: __INK2__; line-height: 1.3; margin-top: 0.6mm; }
.briefs { display: grid; grid-template-columns: 1fr 1fr; gap: 3mm; margin: 1mm 0 2.5mm 0; }
.brief { border: 1px solid __GRID__; border-radius: 2mm; padding: 2.5mm 3mm; font-size: 8pt; color: __INK2__; line-height: 1.35; }
.brief b { display: block; color: __INK__; margin-bottom: 1mm; }
.orgrow { display: flex; align-items: center; gap: 5mm; margin: 1.5mm 0 2mm 0; }
.orgrow img { height: 5.5mm; }
.orgrow img.sx { height: 3.4mm; }
.orgrow img.agentic { border-radius: 1.2mm; }
.covered { display: grid; grid-template-columns: 1fr 1fr; gap: 2.5mm; }
.covered div { background: __WASH__; border-radius: 2mm; padding: 2.4mm 3mm; font-size: 7.8pt; color: __INK2__; line-height: 1.3; }
.covered b { display: block; font-family: __MONOF__; font-size: 8pt; color: __NAVY__; margin-bottom: 0.6mm; }
.sponsor-tile { display: flex; flex-direction: column; gap: 2.5mm; align-items: flex-start; border: 1px solid __GRID__; border-radius: 2mm; padding: 3mm 3.5mm; font-size: 8.4pt; color: __INK2__; }
.sponsor-tile img { height: 4.5mm; }

/* cover */
.cover { padding: 14mm 15mm; display: flex; flex-direction: column; }
.cover .top { display: flex; justify-content: space-between; align-items: center; }
.cover .top .org { display: flex; align-items: center; gap: 5mm; flex: none; }
.cover .top .org img { height: 9mm; }
.cover .top .org img.agentic { border-radius: 1.6mm; }
.cover .for { text-align: right; }
.cover .for .k { font-family: __MONOF__; font-size: 7pt; letter-spacing: 0.14em; text-transform: uppercase; color: __MUTED__; margin-bottom: 1.5mm; }
.cover .for img { height: 7mm; }
.cover .for img.sx { height: 5mm; margin-top: 1mm; }
.cover .right { display: flex; gap: 8mm; align-items: flex-end; flex: none; }
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
  <div class="right">
    <div class="for"><div class="k">Confirmed sponsor</div><img class="sx" src="{LOGOS['spacexai']}" alt="SpaceXAI"></div>
    <div class="for"><div class="k">Prepared for</div><img src="{LOGOS['nokia']}" alt="Nokia"></div>
  </div>
</div>
<div class="hero">
  <div>
    <div class="tag">// sponsorship proposal · Timisoara · 27-29 Nov 2026</div>
    <h1>Agentic<br>Hackathon<br><span>human in<br>the loop</span></h1>
    <p class="lead">{PARTICIPANTS} high school and university students from western Romania spend a weekend
    building AI agents that keep a person in control. We propose Nokia as the Title Partner.</p>
  </div>
  <div>{loop_diagram(270)}</div>
</div>
<div class="toc">
  <div><b>01</b>The event and what Nokia gets</div>
  <div><b>02</b>Budget</div>
  <div><b>03</b>The $20,000 credits line</div>
  <div><b>04</b>Sponsorship packages</div>
  <div><b>05</b>Plan and next step</div>
</div>
<div class="band">
  <div class="row">
    <div><div class="v">{PARTICIPANTS}</div><div class="l">participants<br>{HIGH_SCHOOL} high school, {UNIVERSITY} university</div></div>
    <div><div class="v">{TEAMS}</div><div class="l">teams of two<br>bring your own laptop</div></div>
    <div><div class="v">44h</div><div class="l">Friday 17:00 to<br>Sunday 16:00</div></div>
    <div><div class="v">{eur(TITLE_TIER)}</div><div class="l">proposed Title Partner<br>package for Nokia</div></div>
  </div>
  <div class="meta">
    <div><b>Organizers</b>agentic.tm · UPT · UVT</div>
    <div><b>Date</b>{DATES}</div>
    <div><b>Venue</b>{VENUE}</div>
  </div>
</div>
""", "cover")

# 2. The event and what Nokia gets ------------------------------------------
benefits = [
    ("Powered by Nokia", "naming on site, stage, T-shirts, badges, every post"),
    ("20 min keynote", "Friday opening, all participants and teachers"),
    ("Nokia Challenge", "your problem, your judges, your award"),
    ("5 mentors", "Nokia engineers at the tables both days"),
    ("2 jury seats", "plus the challenge track jury"),
    ("Recruiting", "table at the venue, opt-in CV book"),
    ("Report", "video, photos, numbers, projects, in two weeks"),
    ("Meetup talk", "a Nokia slot at agentic.tm"),
]
page(f"""
<p class="kicker">01 · The event and what Nokia gets</p>
<h1>Two days with {PARTICIPANTS} of the region's strongest young programmers</h1>
<div class="cols">
<div>
<h2>Human in the loop</h2>
<p>Teams build agents that reason, plan and act, with a person approving the steps that matter. The agent
proposes, the human decides. Cursor with frontier models, any stack, a working demo by Sunday noon.</p>
<h3>Who is in the room</h3>
<div class="chart">{split_bar([("High school students, grades 9 to 12", HIGH_SCHOOL, BLUE), ("University students, UPT and UVT", UNIVERSITY, NAVY)], width=322)}</div>
<p class="small">From Timis, Arad, Caras-Severin and Hunedoara. Free to enter. Minors come with parental consent and a
teacher per school group. Two judging tracks, so a 15-year-old is not scored against a third-year student.</p>
<h3>The weekend</h3>
<div class="chart">{schedule_chart(width=322)}</div>
<h3>Organizers and partners</h3>
<div class="orgrow">{logos_html()}<img class="sx" src="{LOGOS['spacexai']}" alt="SpaceXAI"></div>
<p class="small">agentic.tm, Timisoara's agentic AI community, runs the program and brings mentors and sponsors.
UPT hosts and houses the participants; UPT and UVT feed them and add faculty mentors and judges.
SpaceXAI has confirmed sponsorship.</p>
</div>
<div>
<h2>What the Title Partner gets</h2>
<div class="benefits">
{''.join(f'<div class="b"><div class="t">{esc(t)}</div><div class="d">{esc(d)}</div></div>' for t, d in benefits)}
</div>
<div class="callout"><p><b>Why Nokia Timisoara.</b> About 1,300 people on campus, 600 of them R&amp;D engineers, hired
mostly from UPT. The {HIGH_SCHOOL} high school students here are the UPT intake of 2027 to 2029; the
{UNIVERSITY} university students are hires of 2027.</p></div>
<h3>Nokia Challenge: pick one brief</h3>
<div class="briefs">
  <div class="brief"><b>Incident triage with approval</b>An agent reads alarms and logs from a simulated network,
  proposes a diagnosis and a fix, and waits for an engineer to approve.</div>
  <div class="brief"><b>Configuration review</b>An agent reviews a proposed change, explains the risk in plain
  language, and asks the one question that decides it.</div>
</div>
<p class="small">Nothing runs on Nokia infrastructure: laptops and the providers' APIs only.</p>
</div>
</div>
""")

# 3. Budget -------------------------------------------------------------------
budget_rows = [(l, v) for l, v, _ in CASH_LINES] + [("Contingency", CONTINGENCY)]
page(f"""
<p class="kicker">02 · Budget</p>
<h1>Where the money goes: {eur(CASH_TOTAL)}</h1>
<p class="lead">Sponsors pay for what has to be bought: tooling credits, prizes, and the small lines.
Venue, food, drinks and beds come from the universities.</p>
<div class="cols">
<div>
<div class="chart">{hbar_chart(budget_rows, width=322, label_w=132)}</div>
<table>
<tr><th>Cash line</th><th class="num">EUR</th></tr>
{''.join(f'<tr><td>{esc(l)}<br><span style="color:{INK2};font-size:7.6pt">{esc(n)}</span></td><td class="num">{eur(v)}</td></tr>' for l, v, n in CASH_LINES)}
<tr class="sub"><td>Subtotal</td><td class="num">{eur(CASH_SUBTOTAL)}</td></tr>
<tr><td>Contingency {int(CONTINGENCY_RATE * 100)}%</td><td class="num">{eur(CONTINGENCY)}</td></tr>
<tr class="total"><td>Total</td><td class="num">{eur(CASH_TOTAL)}</td></tr>
</table>
</div>
<div>
<h3 style="margin-top:0">Prize pool: {eur(PRIZES_TOTAL)}, per team of two</h3>
<div class="chart">{grouped_prize_chart(PRIZES, width=322)}</div>
<p class="small">High school winners get vouchers, which avoids tax and guardianship paperwork for minors.
Nokia's judges hand out the Nokia Challenge Award.</p>
<h3>Covered by the partners</h3>
<div class="covered">
  <div><b>Venue</b>UPT, Faculty of Automation and Computers</div>
  <div><b>Food and drinks</b>UPT and UVT, six meals plus coffee, water, snacks for {PEOPLE_FED} people</div>
  <div><b>Accommodation</b>UPT dorms for out-of-town participants</div>
  <div><b>Design and mentoring</b>agentic.tm, {MENTORS} mentors, identity, site, media</div>
</div>
</div>
</div>
""")

# 4. Credits ------------------------------------------------------------------
credit_rows = [(l, v) for l, v, _ in CREDITS]
plans = [("Pro $20", [("Plan price", 20), ("Model usage included", 20)]),
         ("Pro+ $60", [("Plan price", 60), ("Model usage included", 70)]),
         ("Ultra $200", [("Plan price", 200), ("Model usage included", 400)])]
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
<h3>Why $100: an agent burns usage, a chatbot does not</h3>
<p class="small">One task becomes dozens of model calls, each carrying the whole codebase context. A team on a frontier
model spends $50 to $150 over a weekend at list prices. Cursor's own plans show the scale:</p>
<div class="chart">{grouped_hbar(plans, [BLUE, AMBER], width=322, label_w=80)}</div>
<p class="small">With no credits, teams still build on the providers' free tiers. Credits put frontier models
and an agentic coding tool in their hands.</p>
</div>
<div>
<h2>Who pays it: three scenarios</h2>
<div class="chart">{stacked_hbar_chart(SCENARIOS, [BLUE, AMBER, GREEN], width=322, label_w=118)}</div>
<table>
<tr><th></th><th>Assumption</th><th class="num">Cash</th></tr>
<tr><td><b>A</b></td><td>Every credit bought at list price. <b>The budget is priced on this.</b></td><td class="num">{usd(20000)}</td></tr>
<tr><td><b>B</b></td><td>Cursor's hackathon program grants $50 per participant, as at its Boston event in May 2026. Application in; answer expected in weeks.</td><td class="num">{usd(10000)}</td></tr>
<tr><td><b>C</b></td><td>B plus $6,000 from Anthropic, OpenAI or Mistral programs, which gave $25 to $50 per participant at comparable events.</td><td class="num">{usd(4000)}</td></tr>
</table>
<div class="callout"><p><b>For Nokia:</b> any credits granted reduce the cash on this line one for one, and the final split
is in the post-event report. Nokia's package does not grow if the applications fail.</p></div>
<h3>How credits reach the teams</h3>
<ul>
  <li>One Cursor Teams workspace owned by the organizers: a seat per participant, a spend cap per seat, no card from any student.</li>
  <li>Cursor's own licences at Nokia stay out of it; cloud agents are restricted on Nokia's network.</li>
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
    <div class="funds">One slot. Credits {eur(CREDITS_TOTAL_EUR)} + prize pool {eur(PRIZES_TOTAL)}: the two lines every participant sees.</div>
    <ul>
      <li>"Powered by Nokia" naming</li>
      <li>20-minute opening keynote</li>
      <li>Nokia Challenge track and award</li>
      <li>Five mentors, two jury seats</li>
      <li>Logo on T-shirts, badges, stage, site</li>
      <li>Recruiting table, opt-in CV book</li>
      <li>Video, photos, written report</li>
      <li>Talk at an agentic.tm meetup</li>
    </ul>
  </div>
  <div class="tier">
    <div class="name">Gold</div>
    <div class="price">{eur(GOLD_TIER)}</div>
    <div class="funds">One slot. Everything the Title package does not cover: swag, print, media, contingency.</div>
    <ul>
      <li>30-minute Saturday workshop</li>
      <li>Two mentors, one jury seat</li>
      <li>Logo on site, stage, T-shirts</li>
      <li>Recruiting table</li>
      <li>Report and photo set</li>
    </ul>
  </div>
  <div class="tier">
    <div class="name">Silver</div>
    <div class="price">{eur(SILVER_TIER)}</div>
    <div class="funds">Open. Cash or services: print, prize hardware, media.</div>
    <ul>
      <li>Logo on site and stage</li>
      <li>Mention at opening and closing</li>
      <li>Swag in the participant bag</li>
    </ul>
  </div>
</div>
<h2>How the budget closes</h2>
<div class="chart">{stacked_hbar_chart([("Cash budget", [("Nokia, Title", TITLE_TIER), ("Gold ×1", CASH_TOTAL - TITLE_TIER)])], [BLUE, AMBER], width=560, label_w=100, value_fmt=eur)}</div>
<div class="cols">
<div>
<p>Nokia's {eur(TITLE_TIER)} is {round(100 * TITLE_TIER / CASH_TOTAL)}% of the cash budget. One Gold sponsor covers the remaining {eur(CASH_TOTAL - TITLE_TIER)}.</p>
<div class="sponsor-tile"><img src="{LOGOS['spacexai']}" alt="SpaceXAI"><div><b>Confirmed sponsor.</b> Package being finalized, not yet counted above.
Whatever it and the credit programs bring lowers the Gold slot and the credits line, and is reported back to Nokia.</div></div>
</div>
<div>
<div class="callout" style="margin-top:0"><p><b>The decision we ask of Nokia:</b> Title Partner at {eur(TITLE_TIER)}, confirmed by {DECISION_BY},
and one Nokia Challenge brief. Then a one-page agreement and two invoices: {eur(TITLE_TIER // 2)} on signing in
October, {eur(TITLE_TIER // 2)} in December with the report.</p></div>
</div>
</div>
""")

# 6. Plan, risks, next step ------------------------------------------------------
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
<p class="kicker">05 · Plan and next step</p>
<h1>From today to the event</h1>
<div class="chart">{timeline_chart(phases, months, width=560, label_w=190)}</div>
<div class="cols">
<div>
<h2>Milestones</h2>
<table>
<tr><th>When</th><th>What</th></tr>
<tr><td class="mono" style="font-size:7.8pt;white-space:nowrap">15 Oct</td><td>Nokia confirms the Title package and the challenge brief; agreement signed</td></tr>
<tr><td class="mono" style="font-size:7.8pt;white-space:nowrap">20 Oct</td><td>Site live, registration open, school announcements go out</td></tr>
<tr><td class="mono" style="font-size:7.8pt;white-space:nowrap">10 Nov</td><td>10 mentors briefed, Nokia Challenge brief final</td></tr>
<tr><td class="mono" style="font-size:7.8pt;white-space:nowrap">13 Nov</td><td>Registration closes, seats and credits provisioned, tooling tested</td></tr>
<tr><td class="mono" style="font-size:7.8pt;white-space:nowrap">27-29 Nov</td><td>The event, {VENUE}</td></tr>
<tr><td class="mono" style="font-size:7.8pt;white-space:nowrap">11 Dec</td><td>Report, video and showcase to sponsors and press; second invoice</td></tr>
</table>
</div>
<div>
<h2>Risks</h2>
<table>
<tr><th>Risk</th><th>Response</th></tr>
<tr><td>No provider grants credits</td><td>The budget already assumes it. Free tiers keep every team building.</td></tr>
<tr><td>Venue falls through</td><td>UVT's campus, same weekend. No sponsor money is spent before the booking is signed.</td></tr>
<tr><td>Minors and accounts</td><td>Organizers create every seat; no student signs a contract or enters a card. Consent forms, a teacher per school group, medical assistance on site.</td></tr>
<tr><td>Fewer participants</td><td>Swag and credits scale with headcount; unspent money is reported and returned.</td></tr>
</table>
<div class="callout">
<p><b>Next step:</b> Nokia confirms the Title Partner package ({eur(TITLE_TIER)}) and picks one Nokia Challenge
brief by {DECISION_BY}. We send the one-page agreement the same week.</p>
</div>
</div>
</div>
""")

assert len(pages) == TOTAL_PAGES, f"expected {TOTAL_PAGES} pages, got {len(pages)}"

# ---------------------------------------------------------------- WRITE -----
doc = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<title>Agentic Hackathon: human in the loop. Sponsorship proposal for Nokia</title>
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
print(f"cash {eur(CASH_TOTAL)}  credits {usd(CREDITS_TOTAL_USD)} = {eur(CREDITS_TOTAL_EUR)}  title {eur(TITLE_TIER)}")
