#!/usr/bin/env python3
"""Build the Nokia sponsorship map (HTML + PDF).

All numbers live in the BUDGET section below. Run `python3 build.py` from this
directory; it writes ../nokia-sponsorship-map.html and ../nokia-sponsorship-map.pdf
(PDF via headless Google Chrome).
"""
import html
import os
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT_HTML = HERE.parent / "nokia-sponsorship-map.html"
OUT_PDF = HERE.parent / "nokia-sponsorship-map.pdf"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

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
    ("Cursor seat, Teams plan, one month", 40,
     "Central billing, spend limits per seat, admin can see usage. "
     "Includes Cursor's own usage allowance and unlimited Auto mode."),
    ("Frontier model usage at API rates", 50,
     "Claude, GPT and Gemini calls made through Cursor or through the "
     "team's own API key. This is the pool that empties on a hackathon weekend."),
    ("Reserve for the final-day crunch", 10,
     "Topped up only for teams that run dry on Sunday morning. Unused reserve "
     "is not spent."),
]
CREDITS_PER_PERSON_USD = sum(v for _, v, _ in CREDITS)
CREDITS_TOTAL_USD = CREDITS_PER_PERSON_USD * PARTICIPANTS
CREDITS_TOTAL_EUR = round(CREDITS_TOTAL_USD * USD_EUR)

# Food, EUR per person, Friday evening to Sunday afternoon
MEALS = [
    ("Breakfast, Saturday and Sunday", 2, 6),
    ("Lunch, Saturday and Sunday", 2, 11),
    ("Dinner, Friday and Saturday", 2, 9),
    ("Coffee, water, snacks, three days", 1, 12),
]
FOOD_PER_PERSON = sum(n * p for _, n, p in MEALS)
FOOD_TOTAL = FOOD_PER_PERSON * PEOPLE_FED

# Prizes, EUR, per team (teams of two)
PRIZES = [
    ("High school track", [("1st place", 1500), ("2nd place", 1000), ("3rd place", 500)]),
    ("University track", [("1st place", 1500), ("2nd place", 1000), ("3rd place", 500)]),
    ("Special awards", [("Nokia Challenge Award", 1000),
                        ("Best Human-in-the-Loop design", 500),
                        ("Community choice", 500)]),
]
PRIZES_TOTAL = sum(v for _, items in PRIZES for _, v in items)

# Everything else, EUR
SWAG_ITEMS = [
    ("T-shirts", PEOPLE_FED + 10, 7),
    ("Lanyards and badges", PEOPLE_FED + 10, 1.5),
    ("Stickers", 1, 160),
]
SWAG_TOTAL = round(sum(n * p for _, n, p in SWAG_ITEMS))

OTHER = [
    ("Print and signage", 700, "Four roll-ups, one stage banner, posters, room signs."),
    ("Photo and video", 1000, "Photographer both days, one edited recap video for sponsors and press."),
    ("Mentor and judge costs", 600, "Travel for out-of-town mentors, thank-you gifts."),
    ("Safety and first aid", 500, "Medical assistance on site, consent-form handling for minors."),
    ("Website and registration", 150, "Domain, hosting, registration and submission tooling."),
]
OTHER_TOTAL = sum(v for _, v, _ in OTHER)

CONTINGENCY_RATE = 0.08

CASH_LINES = [
    ("Developer tooling credits", CREDITS_TOTAL_EUR, f"${CREDITS_TOTAL_USD:,} at {USD_EUR} EUR/USD"),
    ("Food and drinks", FOOD_TOTAL, f"{PEOPLE_FED} people, six meals plus snacks"),
    ("Prize pool", PRIZES_TOTAL, "Two tracks plus three special awards"),
    ("Swag", SWAG_TOTAL, "T-shirts, badges, stickers"),
    ("Print and signage", 700, ""),
    ("Photo and video", 1000, ""),
    ("Mentor and judge costs", 600, ""),
    ("Safety and first aid", 500, ""),
    ("Website and registration", 150, ""),
]
CASH_SUBTOTAL = sum(v for _, v, _ in CASH_LINES)
CONTINGENCY = round(CASH_SUBTOTAL * CONTINGENCY_RATE)
CASH_TOTAL = CASH_SUBTOTAL + CONTINGENCY

IN_KIND = [
    ("Venue: amphitheatre, labs, network", "UPT / UVT", 4500),
    ("Accommodation for out-of-town participants", "UPT / UVT dorms", 3600),
    ("GPU cluster for open-weight models", "UPT / UVT", 2000),
    ("Design: identity, site, media graphics", "agentic.tm", 2500),
    ("Mentoring, 10 mentors, two days", "agentic.tm, UPT, UVT", 10000),
]
IN_KIND_TOTAL = sum(v for _, _, v in IN_KIND)

TIERS = [
    ("Title Partner", 25000, "Funds the developer tooling credits and the prize pool."),
    ("Gold", 10000, "Up to two slots. Funds food or the media and swag package."),
    ("Silver", 5000, "No limit on slots."),
]

# Credit funding scenarios, USD
SCENARIOS = [
    ("A. No provider support", [("Sponsor cash", 20000)]),
    ("B. Cursor credits approved", [("Sponsor cash", 10000), ("Cursor credits", 10000)]),
    ("C. Cursor plus model providers", [("Sponsor cash", 4000), ("Cursor credits", 10000),
                                        ("Model provider programs", 6000)]),
]

# ---------------------------------------------------------------- STYLE -----
BLUE = "#2a78d6"
ORANGE = "#eb6834"
AQUA = "#1baf7a"
YELLOW = "#eda100"
INK = "#0b0b0b"
INK2 = "#52514e"
MUTED = "#898781"
GRID = "#e1e0d9"
SURFACE = "#fcfcfb"


def eur(v):
    return f"€{round(v):,}"


def usd(v):
    return f"${round(v):,}"


def esc(s):
    return html.escape(str(s))


# ---------------------------------------------------------------- CHARTS ----
def hbar_chart(rows, width=640, bar_h=22, gap=10, label_w=230, value_fmt=eur, color=BLUE,
               max_value=None, colors=None):
    """Horizontal bars, one per row: (label, value). Direct labels, no legend."""
    max_value = max_value or max(v for _, v in rows)
    h = len(rows) * (bar_h + gap) + gap
    plot_w = width - label_w - 90
    out = [f'<svg viewBox="0 0 {width} {h}" width="{width}" height="{h}" '
           f'font-family="system-ui,-apple-system,Segoe UI,sans-serif" font-size="12">']
    y = gap
    for i, (label, v) in enumerate(rows):
        w = max(2, plot_w * v / max_value)
        c = colors[i] if colors else color
        out.append(f'<text x="{label_w - 10}" y="{y + bar_h * 0.68:.1f}" text-anchor="end" '
                   f'fill="{INK2}">{esc(label)}</text>')
        out.append(f'<rect x="{label_w}" y="{y}" width="{w:.1f}" height="{bar_h}" fill="{c}" '
                   f'rx="0" />')
        out.append(f'<rect x="{label_w + w - 4:.1f}" y="{y}" width="4" height="{bar_h}" fill="{c}" rx="3"/>')
        out.append(f'<text x="{label_w + w + 8:.1f}" y="{y + bar_h * 0.68:.1f}" fill="{INK}" '
                   f'font-variant-numeric="tabular-nums">{esc(value_fmt(v))}</text>')
        y += bar_h + gap
    out.append(f'<line x1="{label_w}" y1="{gap - 4}" x2="{label_w}" y2="{h - gap + 4}" stroke="#c3c2b7" stroke-width="1"/>')
    out.append("</svg>")
    return "\n".join(out)


def stacked_hbar_chart(rows, series_colors, width=640, bar_h=26, gap=14, label_w=210,
                       value_fmt=usd, total_label=True):
    """rows: (label, [(series, value), ...]). Legend built from series order."""
    series = []
    for _, segs in rows:
        for s, _ in segs:
            if s not in series:
                series.append(s)
    max_total = max(sum(v for _, v in segs) for _, segs in rows)
    plot_w = width - label_w - 80
    h = len(rows) * (bar_h + gap) + gap + 28
    out = [f'<svg viewBox="0 0 {width} {h}" width="{width}" height="{h}" '
           f'font-family="system-ui,-apple-system,Segoe UI,sans-serif" font-size="12">']
    y = gap
    for label, segs in rows:
        out.append(f'<text x="{label_w - 10}" y="{y + bar_h * 0.66:.1f}" text-anchor="end" fill="{INK2}">{esc(label)}</text>')
        x = label_w
        for s, v in segs:
            w = plot_w * v / max_total
            c = series_colors[series.index(s)]
            out.append(f'<rect x="{x:.1f}" y="{y}" width="{max(0, w - 2):.1f}" height="{bar_h}" fill="{c}"/>')
            if w > 70:
                out.append(f'<text x="{x + 6:.1f}" y="{y + bar_h * 0.66:.1f}" fill="#ffffff" font-weight="600" '
                           f'font-variant-numeric="tabular-nums">{esc(value_fmt(v))}</text>')
            x += w
        if total_label:
            total = sum(v for _, v in segs)
            out.append(f'<text x="{x + 8:.1f}" y="{y + bar_h * 0.66:.1f}" fill="{INK}" '
                       f'font-variant-numeric="tabular-nums">{esc(value_fmt(total))}</text>')
        y += bar_h + gap
    # legend
    lx = label_w
    ly = y + 6
    for s in series:
        c = series_colors[series.index(s)]
        out.append(f'<rect x="{lx}" y="{ly}" width="12" height="12" fill="{c}" rx="2"/>')
        out.append(f'<text x="{lx + 18}" y="{ly + 10}" fill="{INK2}">{esc(s)}</text>')
        lx += 18 + 7 * len(s) + 24
    out.append("</svg>")
    return "\n".join(out)


def timeline_chart(phases, months, width=640, label_w=210):
    """phases: (label, start_idx, end_idx) over the month list (fractional allowed)."""
    row_h = 22
    gap = 8
    plot_w = width - label_w - 20
    top = 26
    h = top + len(phases) * (row_h + gap) + 10
    out = [f'<svg viewBox="0 0 {width} {h}" width="{width}" height="{h}" '
           f'font-family="system-ui,-apple-system,Segoe UI,sans-serif" font-size="12">']
    mw = plot_w / len(months)
    for i, m in enumerate(months):
        x = label_w + i * mw
        out.append(f'<text x="{x + mw / 2:.1f}" y="14" text-anchor="middle" fill="{MUTED}">{esc(m)}</text>')
        out.append(f'<line x1="{x:.1f}" y1="{top - 6}" x2="{x:.1f}" y2="{h - 6}" stroke="{GRID}" stroke-width="1"/>')
    y = top
    for label, s, e in phases:
        out.append(f'<text x="{label_w - 10}" y="{y + row_h * 0.68:.1f}" text-anchor="end" fill="{INK2}">{esc(label)}</text>')
        x1 = label_w + s * mw
        x2 = label_w + e * mw
        out.append(f'<rect x="{x1:.1f}" y="{y + 4}" width="{x2 - x1:.1f}" height="{row_h - 8}" fill="{BLUE}" rx="3"/>')
        y += row_h + gap
    out.append("</svg>")
    return "\n".join(out)


# ---------------------------------------------------------------- PAGES -----
CSS = f"""
@page {{ size: A4; margin: 0; }}
* {{ box-sizing: border-box; }}
html, body {{ margin: 0; padding: 0; background: #ffffff; color: {INK};
  font-family: system-ui, -apple-system, "Segoe UI", Helvetica, Arial, sans-serif;
  font-size: 11pt; line-height: 1.45; }}
.page {{ width: 210mm; height: 297mm; padding: 18mm 18mm 16mm 18mm; position: relative;
  page-break-after: always; overflow: hidden; background: #ffffff; }}
.page:last-child {{ page-break-after: auto; }}
.kicker {{ font-size: 9pt; letter-spacing: 0.12em; text-transform: uppercase; color: {BLUE};
  font-weight: 600; margin: 0 0 4mm 0; }}
h1 {{ font-size: 26pt; line-height: 1.15; margin: 0 0 6mm 0; font-weight: 700; letter-spacing: -0.01em; }}
h2 {{ font-size: 13pt; margin: 7mm 0 2.5mm 0; font-weight: 700; }}
h2:first-of-type {{ margin-top: 0; }}
p {{ margin: 0 0 3mm 0; }}
.lead {{ font-size: 12.5pt; color: {INK2}; }}
.foot {{ position: absolute; left: 18mm; right: 18mm; bottom: 9mm; font-size: 8.5pt; color: {MUTED};
  display: flex; justify-content: space-between; border-top: 1px solid {GRID}; padding-top: 2.5mm; }}
table {{ border-collapse: collapse; width: 100%; font-size: 10pt; margin: 0 0 4mm 0; }}
th, td {{ text-align: left; padding: 2mm 2.5mm; border-bottom: 1px solid {GRID}; vertical-align: top; }}
th {{ font-size: 8.5pt; text-transform: uppercase; letter-spacing: 0.06em; color: {MUTED}; font-weight: 600; }}
td.num, th.num {{ text-align: right; font-variant-numeric: tabular-nums; white-space: nowrap; }}
tr.total td {{ font-weight: 700; border-top: 2px solid {INK}; border-bottom: none; }}
tr.sub td {{ color: {INK2}; }}
td.note {{ color: {INK2}; font-size: 9pt; }}
.grid2 {{ display: grid; grid-template-columns: 1fr 1fr; gap: 6mm; }}
.grid3 {{ display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 5mm; }}
.tile {{ border: 1px solid {GRID}; border-radius: 3mm; padding: 4mm 5mm; }}
.tile .v {{ font-size: 22pt; font-weight: 700; line-height: 1.1; letter-spacing: -0.01em; }}
.tile .l {{ font-size: 9pt; color: {INK2}; margin-top: 1mm; }}
.callout {{ background: #eef4fc; border-left: 3px solid {BLUE}; padding: 3.5mm 5mm; border-radius: 0 2mm 2mm 0; margin: 4mm 0; }}
.callout p:last-child {{ margin-bottom: 0; }}
ul {{ margin: 0 0 3mm 0; padding-left: 5mm; }}
li {{ margin-bottom: 1.2mm; }}
.small {{ font-size: 9pt; color: {INK2}; }}
.cover {{ background: {BLUE}; color: #ffffff; padding: 24mm 20mm; }}
.cover .kicker {{ color: #cde2fb; }}
.cover h1 {{ font-size: 36pt; margin-top: 30mm; }}
.cover .lead {{ color: #e6effc; font-size: 14pt; max-width: 140mm; }}
.cover .meta {{ position: absolute; bottom: 22mm; left: 20mm; right: 20mm; color: #cde2fb; font-size: 10pt;
  display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 6mm; }}
.cover .meta b {{ display: block; color: #ffffff; font-size: 12pt; margin-bottom: 1mm; }}
.tier {{ border: 1px solid {GRID}; border-radius: 3mm; padding: 4mm 5mm; margin-bottom: 4mm; }}
.tier.top {{ border: 2px solid {BLUE}; }}
.tier h3 {{ margin: 0 0 1mm 0; font-size: 12pt; display: flex; justify-content: space-between; }}
.tier h3 span {{ color: {BLUE}; font-variant-numeric: tabular-nums; }}
.tier p {{ margin-bottom: 2mm; }}
.tier ul {{ font-size: 9.5pt; columns: 2; column-gap: 6mm; }}
.sched td:first-child {{ white-space: nowrap; color: {INK2}; width: 22mm; }}
svg {{ display: block; margin: 2mm 0 4mm 0; }}
"""

pages = []
FOOT_L = "Agentic Programming Hackathon, Timisoara · Sponsorship proposal for Nokia"


def page(body, cls=""):
    n = len(pages) + 1
    foot = "" if cls == "cover" else f'<div class="foot"><span>{FOOT_L}</span><span>{n}</span></div>'
    pages.append(f'<section class="page {cls}">{body}{foot}</section>')


# 1. Cover
page(f"""
<p class="kicker">Sponsorship proposal · Timisoara</p>
<h1>Agentic Programming Hackathon</h1>
<p class="lead">{PARTICIPANTS} high school and university students from western Romania build
AI agents that keep a human in the loop. Two days, {TEAMS} teams, one national stage.
A proposal for Nokia to power the event.</p>
<div class="meta">
  <div><b>Organizers</b>agentic.tm · Politehnica University of Timisoara (UPT) · West University of Timisoara (UVT)</div>
  <div><b>Date</b>Late November 2026, or 23 January 2027. Locked with UPT and UVT in early October.</div>
  <div><b>Part of</b>olimpiada-ai.ro, the national AI olympiad network</div>
</div>
""", "cover")

# 2. At a glance
page(f"""
<p class="kicker">At a glance</p>
<h1>The event in one page</h1>
<div class="grid3">
  <div class="tile"><div class="v">{PARTICIPANTS}</div><div class="l">participants: {HIGH_SCHOOL} high school, {UNIVERSITY} university students</div></div>
  <div class="tile"><div class="v">{TEAMS}</div><div class="l">teams of two, bring your own laptop</div></div>
  <div class="tile"><div class="v">44h</div><div class="l">Friday 17:00 to Sunday 16:00, on campus in Timisoara</div></div>
</div>
<div class="grid3" style="margin-top:5mm">
  <div class="tile"><div class="v">{eur(CASH_TOTAL)}</div><div class="l">total cash budget, including {int(CONTINGENCY_RATE*100)}% contingency</div></div>
  <div class="tile"><div class="v">{eur(IN_KIND_TOTAL)}</div><div class="l">in-kind from the universities and agentic.tm: venue, dorms, GPUs, mentors, design</div></div>
  <div class="tile"><div class="v">{eur(TIERS[0][1])}</div><div class="l">proposed Nokia Title Partner package: credits plus prize pool</div></div>
</div>

<h2>What we are asking</h2>
<p>We propose Nokia as the Title Partner of the hackathon, at {eur(TIERS[0][1])}. That package pays for
the two lines that carry a sponsor's name in front of every participant: the developer tooling
credits each team uses to build ({eur(CREDITS_TOTAL_EUR)}, {usd(CREDITS_TOTAL_USD)}) and the prize pool
({eur(PRIZES_TOTAL)}). Everything else, food, swag, media, is covered by the universities, by
agentic.tm and by Gold and Silver sponsors we approach in parallel.</p>
<p>The credits line is the one that needs the most explanation, so pages 7 and 8 break it down
per person, per component, and by who pays it under three scenarios. In the best scenario Cursor
and the model providers fund half of it and Nokia's cash need drops accordingly.</p>

<h2>What Nokia gets</h2>
<ul>
  <li><b>The name on the event.</b> "Powered by Nokia" on the site, stage, T-shirts, every post and every press mention, through olimpiada-ai.ro's national channels.</li>
  <li><b>A Nokia Challenge track</b> with its own award, on a problem from Nokia's domain, judged by Nokia engineers.</li>
  <li><b>Two days with {PARTICIPANTS} future engineers.</b> Nokia mentors at the tables, a keynote at the opening, seats on the jury, an opt-in CV book afterwards.</li>
  <li><b>A report you can send upward.</b> Numbers, photos, the recap video and the winning projects, delivered within two weeks of the event.</li>
</ul>
<div class="callout"><p><b>Why this matters for Nokia Timisoara.</b> Nokia's Timisoara campus employs about 1,300 people, roughly 600 of them
R&amp;D engineers, and hires mostly from UPT. The {HIGH_SCHOOL} high school students in this room are the UPT
intake of 2027 to 2029. The {UNIVERSITY} university students are hires of 2027.</p></div>
""")

# 3. Concept
page(f"""
<p class="kicker">The hackathon</p>
<h1>Human in the loop</h1>
<p class="lead">Students build AI agents that reason, plan and act, with a person guiding, approving or
correcting them at the points that matter. The agent proposes, the human decides.</p>
<h2>Why this theme</h2>
<p>The agent systems that work in production today are the ones that keep people in control:
a coding agent that opens a pull request for review, a support agent that drafts a reply for
an operator, a network agent that proposes a change and waits for an engineer to approve it.
Teaching students to design that boundary from their first project is the point of the event.</p>
<p>Teams get developer tooling (Cursor with frontier models) and API access, choose their own
stack, and ship a working demo by Sunday noon. There is no fixed problem list. There is a
Nokia Challenge track for teams that want a problem from Nokia's world, for example an agent
that triages network incidents and proposes fixes an engineer signs off on.</p>

<h2>Who participates</h2>
<table>
<tr><th>Group</th><th class="num">Participants</th><th>Where they come from</th></tr>
<tr><td>High school students, grades 9 to 12</td><td class="num">{HIGH_SCHOOL}</td><td>Timis, Arad, Caras-Severin, Hunedoara, through the olimpiada-ai.ro school network and county inspectorates</td></tr>
<tr><td>University students</td><td class="num">{UNIVERSITY}</td><td>UPT and UVT, years one to three, plus master's students</td></tr>
<tr class="total"><td>Total</td><td class="num">{PARTICIPANTS}</td><td>{TEAMS} teams of {TEAM_SIZE}</td></tr>
</table>
<p class="small">Participation is free. Teams register through olimpiada-ai.ro. High school students need a
signed parental consent and an accompanying teacher per school group. Two judging tracks
(high school, university) so that a 15-year-old is not scored against a third-year student.</p>

<h2>The weekend</h2>
<table class="sched">
<tr><th>When</th><th>What</th></tr>
<tr><td>Friday 17:00</td><td>Check-in, opening, keynote (Nokia slot), theme briefing, hacking starts at 19:00</td></tr>
<tr><td>Saturday</td><td>Hacking all day. Mentor office hours, two short workshops (agent design, evaluation), Nokia Challenge briefing</td></tr>
<tr><td>Sunday 12:00</td><td>Code freeze and submissions</td></tr>
<tr><td>Sunday 13:00</td><td>Demos in front of the jury, two parallel rooms by track</td></tr>
<tr><td>Sunday 15:30</td><td>Awards, closing, group photo</td></tr>
</table>
""")

# 4. Organizers and reach
page(f"""
<p class="kicker">Who is behind it</p>
<h1>Organizers and reach</h1>
<table>
<tr><th>Organizer</th><th>Role</th><th>Brings</th></tr>
<tr><td><b>agentic.tm</b></td><td>Concept, program, mentors, sponsors</td><td>Timisoara's agentic AI community: 200+ members on Discord, 500+ on LinkedIn, monthly meetups since October 2025. Mentors with hands-on LLM and agent experience.</td></tr>
<tr><td><b>UPT</b> Politehnica University of Timisoara</td><td>Venue, accommodation, compute</td><td>Amphitheatre and labs, dorm rooms for out-of-town students, GPU cluster for open-weight models, faculty mentors and judges.</td></tr>
<tr><td><b>UVT</b> West University of Timisoara</td><td>Venue, accommodation, compute</td><td>Same as UPT, plus the AI and data science faculty. Final venue is chosen between the two campuses when the date is locked.</td></tr>
<tr><td><b>olimpiada-ai.ro</b></td><td>National umbrella</td><td>The Ministry of Education accredited national AI olympiad. Registration, school outreach and national visibility run through its channels.</td></tr>
</table>

<h2>Who sees the event</h2>
<div class="grid3">
  <div class="tile"><div class="v">4</div><div class="l">counties recruited through school inspectorates and the olympiad network</div></div>
  <div class="tile"><div class="v">2</div><div class="l">universities, both campuses, both student bodies</div></div>
  <div class="tile"><div class="v">700+</div><div class="l">agentic.tm community members across Discord and LinkedIn</div></div>
</div>
<p style="margin-top:4mm">Communication runs on three levels: olimpiada-ai.ro to schools and the ministry network
nationally, UPT and UVT to their students and press offices, and agentic.tm to the local tech
industry. A recap video and a written report go to every sponsor and to the press after the event.</p>

<h2>Precedents in Timisoara</h2>
<p>Timisoara already runs hackathons at this scale: HackTM (six days, EUR 10,000 in prizes),
UniHack at UPT (48 hours, MLH-sanctioned, open to high school and university students) and ITFest
at UVT. What none of them does is put agentic AI and a human-in-the-loop brief in front of high
school students with proper tooling. The nearest example is Cluj Hackathon 2025, "AI Agents
Everywhere", where a 14-year-old took first place.</p>
""")

# 5. Why Nokia
page(f"""
<p class="kicker">Why Nokia</p>
<h1>What the Title Partner gets</h1>
<p class="lead">A hackathon is two days of undivided attention from {PARTICIPANTS} of the strongest young
programmers in the region, and a story Nokia can tell for a year afterwards.</p>

<h2>Employer brand where hiring happens</h2>
<p>Nokia Timisoara hires its engineers mainly from UPT. Every participant in this event is on that
path: the university students are one to three years from a first job, and the high school
students are choosing a university and a field in the next two years. A Nokia keynote on Friday,
Nokia engineers as mentors on Saturday and a Nokia Challenge award on Sunday put the company in
front of them as the place where this kind of engineering happens.</p>

<h2>The Nokia Challenge track</h2>
<p>Nokia defines one problem from its own domain and teams opt in. Two examples we would propose:</p>
<ul>
  <li><b>Incident triage with approval.</b> An agent reads alarms and logs from a simulated network,
  proposes a diagnosis and a fix, and waits for an engineer to approve before acting.</li>
  <li><b>Configuration review.</b> An agent reviews a proposed configuration change, explains the risk
  in plain language, and asks the human the one question that decides it.</li>
</ul>
<p>Nokia engineers judge this track and hand out the award. Winning projects come with a short
write-up Nokia can reuse internally.</p>

<h2>Everything in the package</h2>
<table>
<tr><th>Benefit</th><th>Detail</th></tr>
<tr><td>Naming</td><td>"Powered by Nokia" on the site, registration page, stage backdrop, T-shirts, badges, all social posts and press releases</td></tr>
<tr><td>Keynote</td><td>20 minutes at Friday's opening, in front of all participants and teachers</td></tr>
<tr><td>Challenge track</td><td>Nokia-defined problem, Nokia judges, Nokia Challenge Award ({eur(1000)})</td></tr>
<tr><td>Mentors</td><td>Up to five Nokia engineers on the mentor roster, with visible Nokia badges</td></tr>
<tr><td>Jury</td><td>Two seats on the main jury, plus the challenge track jury</td></tr>
<tr><td>Recruiting</td><td>Opt-in CV book of participants over 18, a Nokia table at the venue both days</td></tr>
<tr><td>Content</td><td>Recap video, photo set, written report with numbers and projects, within two weeks</td></tr>
<tr><td>Community</td><td>A Nokia talk at an agentic.tm meetup before or after the event</td></tr>
</table>
""")

# 6. Budget overview
budget_rows = [(l, v) for l, v, _ in CASH_LINES] + [("Contingency", CONTINGENCY)]
page(f"""
<p class="kicker">Budget</p>
<h1>Where the money goes</h1>
<p class="lead">Total cash budget {eur(CASH_TOTAL)}. The universities and agentic.tm add {eur(IN_KIND_TOTAL)} in kind,
so the venue, beds, compute and mentoring cost the sponsors nothing.</p>
{hbar_chart(budget_rows, width=620, bar_h=18, gap=8)}
<table>
<tr><th>Line</th><th class="num">EUR</th><th>Basis</th></tr>
{''.join(f'<tr><td>{esc(l)}</td><td class="num">{eur(v)}</td><td class="note">{esc(n)}</td></tr>' for l, v, n in CASH_LINES)}
<tr class="sub"><td>Subtotal</td><td class="num">{eur(CASH_SUBTOTAL)}</td><td></td></tr>
<tr><td>Contingency {int(CONTINGENCY_RATE*100)}%</td><td class="num">{eur(CONTINGENCY)}</td><td class="note">Price changes, no-shows, last-minute needs</td></tr>
<tr class="total"><td>Total cash</td><td class="num">{eur(CASH_TOTAL)}</td><td></td></tr>
</table>
<p class="small">Exchange rate {USD_EUR} EUR per USD, mid-September 2026. Food and swag prices are Timisoara
catering and print estimates; final quotes come with the date. Pages 7 to 10 detail every line.</p>
""")

# 7. Credits in detail
credit_rows = [(l, v) for l, v, _ in CREDITS]
page(f"""
<p class="kicker">Budget · developer tooling credits</p>
<h1>The {usd(CREDITS_TOTAL_USD)} credits line, split</h1>
<p class="lead">{usd(CREDITS_PER_PERSON_USD)} per participant, {usd(CREDITS_PER_PERSON_USD * TEAM_SIZE)} per team,
{PARTICIPANTS} participants. Here is what that buys and why the number is what it is.</p>
{hbar_chart(credit_rows, width=620, value_fmt=lambda v: f"${v} / person", label_w=250)}
<table>
<tr><th>Component</th><th class="num">Per person</th><th class="num">Total</th><th>What it is</th></tr>
{''.join(f'<tr><td>{esc(l)}</td><td class="num">{usd(v)}</td><td class="num">{usd(v * PARTICIPANTS)}</td><td class="note">{esc(n)}</td></tr>' for l, v, n in CREDITS)}
<tr class="total"><td>Total</td><td class="num">{usd(CREDITS_PER_PERSON_USD)}</td><td class="num">{usd(CREDITS_TOTAL_USD)}</td><td class="note">{eur(CREDITS_TOTAL_EUR)}</td></tr>
</table>

<h2>Why $100 and not $10</h2>
<p>A chat app that calls a model once per message costs cents. An agent turns one task into dozens
of model calls, each carrying the whole context of the code so far. A team using a frontier
model in an agentic coding tool for two days burns through $50 to $150 of usage at list prices.
Cursor's own plans show the scale: the $20 plan includes $20 of model usage, the $60 plan $70,
the $200 plan $400. We size the pool so a team does not run dry on Saturday evening, and keep a
reserve instead of giving everyone the maximum.</p>

<h2>How the credits are handed out</h2>
<ul>
  <li><b>Seats</b> live in one Cursor Teams workspace owned by the organizers, one per participant for the event
  month. Central billing, per-seat spend limit, no card from any student.</li>
  <li><b>Model usage</b> comes from the workspace pool with a hard cap per seat. Teams that want raw API access get
  a key through a gateway on a UPT server, with the same per-team budget.</li>
  <li><b>The reserve</b> is released on Sunday morning to teams close to their cap.</li>
  <li><b>With no credits at all,</b> every team can still build on free tiers and on open-weight models served
  from the UPT and UVT GPU clusters. The credits are what put frontier models in their hands.</li>
</ul>
""")

# 8. Who pays the credits
page(f"""
<p class="kicker">Budget · developer tooling credits</p>
<h1>Who pays the credits: three scenarios</h1>
<p class="lead">The cash need for credits is {usd(CREDITS_TOTAL_USD)} if no provider helps, and drops to
{usd(4000)} in the best case. Applications are in progress; the answer decides the sponsor cash.</p>
{stacked_hbar_chart(SCENARIOS, [BLUE, ORANGE, AQUA], width=620, label_w=200)}
<table>
<tr><th>Scenario</th><th>Assumption</th><th class="num">Sponsor cash</th><th>Status</th></tr>
<tr><td><b>A</b> No provider support</td><td>Every credit is bought at list price.</td><td class="num">{usd(20000)}<br><span class="small">{eur(20000 * USD_EUR)}</span></td><td class="note">The base case. Everything in this document is budgeted on it.</td></tr>
<tr><td><b>B</b> Cursor credits approved</td><td>Cursor's hackathon program grants $50 per participant, the amount it gave at its Boston Tech Week hackathon in May 2026.</td><td class="num">{usd(10000)}<br><span class="small">{eur(10000 * USD_EUR)}</span></td><td class="note">Application submitted through Cursor's hackathon form. Their stated response time is "the next few weeks". Direct contact at Cursor in parallel.</td></tr>
<tr><td><b>C</b> Cursor plus model providers</td><td>Scenario B plus $6,000 from Anthropic, OpenAI or Mistral hackathon programs, which have given $25 to $50 per participant at comparable events.</td><td class="num">{usd(4000)}<br><span class="small">{eur(4000 * USD_EUR)}</span></td><td class="note">Mistral: request pending (UPT). Anthropic and OpenAI: applications go in once the date is locked; both need at least a month of lead time.</td></tr>
</table>
<div class="callout">
<p><b>What this means for Nokia.</b> The Title Partner package is priced on scenario A. Any credits granted by
Cursor or a model provider reduce the cash Nokia spends on this line, one for one, and we report the
final split in the post-event report. Nokia's package does not grow if the applications fail.</p>
</div>
<h2>What Cursor can and cannot do</h2>
<ul>
  <li>Cursor grants credits to hackathons "that meet our criteria", case by case. There is no published amount; recent events received $50 per participant, or prize credits of $500 to $3,500.</li>
  <li>Cursor's free year for students closed to new sign-ups in June 2026, so it is not a route for the {UNIVERSITY} university students. Cursor does not sponsor food, prizes or venues.</li>
  <li>Nokia's own Cursor licences are not usable: cloud agent features are restricted on Nokia's network. The event runs its own workspace on the universities' and participants' machines.</li>
</ul>
""")

# 9. Other expenses
page(f"""
<p class="kicker">Budget · other expenses</p>
<h1>Food, prizes, swag and the rest</h1>
<h2>Food and drinks: {eur(FOOD_TOTAL)}</h2>
<p>{PEOPLE_FED} people to feed: {PARTICIPANTS} participants, {MENTORS} mentors, {JUDGES} judges, {STAFF} organizers and volunteers.
Six meals from Friday dinner to Sunday lunch, plus coffee, water and snacks around the clock.</p>
<table>
<tr><th>Item</th><th class="num">Count</th><th class="num">Per person</th><th class="num">Subtotal</th></tr>
{''.join(f'<tr><td>{esc(l)}</td><td class="num">{n}</td><td class="num">{eur(p)}</td><td class="num">{eur(n * p * PEOPLE_FED)}</td></tr>' for l, n, p in MEALS)}
<tr class="total"><td>Total</td><td class="num"></td><td class="num">{eur(FOOD_PER_PERSON)}</td><td class="num">{eur(FOOD_TOTAL)}</td></tr>
</table>
<p class="small">Catering delivered to the venue, vegetarian option at every meal. Accommodation is not in this
budget: UPT and UVT house out-of-town participants in their dorms.</p>

<h2>Prize pool: {eur(PRIZES_TOTAL)}</h2>
<table>
<tr><th>Track</th><th>Award</th><th class="num">EUR</th></tr>
{''.join(''.join(f'<tr><td>{esc(t) if i == 0 else ""}</td><td>{esc(a)}</td><td class="num">{eur(v)}</td></tr>' for i, (a, v) in enumerate(items)) for t, items in PRIZES)}
<tr class="total"><td>Total</td><td></td><td class="num">{eur(PRIZES_TOTAL)}</td></tr>
</table>
<p class="small">Prizes go to teams of two. High school winners receive vouchers rather than cash, which avoids tax
and guardianship paperwork for minors. The Nokia Challenge Award is handed out by Nokia's judges.</p>
""")

# 10. In kind and the rest
page(f"""
<p class="kicker">Budget · in kind and the rest</p>
<h1>Partner contributions and the small lines</h1>
<h2>In kind, already committed: {eur(IN_KIND_TOTAL)}</h2>
<p>These do not appear in the cash budget. They are what the universities and agentic.tm put in,
valued at what the organizers would otherwise pay.</p>
<table>
<tr><th>Contribution</th><th>From</th><th class="num">Value</th></tr>
{''.join(f'<tr><td>{esc(l)}</td><td>{esc(f)}</td><td class="num">{eur(v)}</td></tr>' for l, f, v in IN_KIND)}
<tr class="total"><td>Total in kind</td><td></td><td class="num">{eur(IN_KIND_TOTAL)}</td></tr>
</table>
<p class="small">Venue value is the commercial rate for an amphitheatre plus labs for three days. Accommodation
assumes 120 out-of-town participants, two nights each. Mentoring is 10 mentors at 20 hours each,
at a senior engineer's day rate.</p>

<h2>Everything else: {eur(SWAG_TOTAL + OTHER_TOTAL)}</h2>
<table>
<tr><th>Line</th><th class="num">EUR</th><th>Detail</th></tr>
<tr><td>Swag</td><td class="num">{eur(SWAG_TOTAL)}</td><td class="note">{', '.join(f'{l.lower()} {n} × {eur(p)}' if n > 1 else f'{l.lower()} {eur(p)}' for l, n, p in SWAG_ITEMS)}</td></tr>
{''.join(f'<tr><td>{esc(l)}</td><td class="num">{eur(v)}</td><td class="note">{esc(n)}</td></tr>' for l, v, n in OTHER)}
<tr class="total"><td>Total</td><td class="num">{eur(SWAG_TOTAL + OTHER_TOTAL)}</td><td></td></tr>
</table>
<p class="small">Contingency of {int(CONTINGENCY_RATE*100)}% ({eur(CONTINGENCY)}) sits on top of all cash lines and is
reported back unspent.</p>
""")

# 10. Tiers
title_t, gold_t, silver_t = TIERS
page(f"""
<p class="kicker">Sponsorship packages</p>
<h1>Three tiers, one recommended for Nokia</h1>
<div class="tier top">
  <h3>Title Partner <span>{eur(title_t[1])}</span></h3>
  <p>{esc(title_t[2])} One slot. This is the package we propose for Nokia.</p>
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
  <h3>Gold <span>{eur(gold_t[1])}</span></h3>
  <p>{esc(gold_t[2])}</p>
  <ul>
    <li>30-minute workshop on Saturday</li>
    <li>Two mentors, one jury seat</li>
    <li>Logo on site, stage, T-shirts</li>
    <li>Recruiting table</li>
    <li>Named in all press and social posts</li>
    <li>Report and photo set</li>
  </ul>
</div>
<div class="tier">
  <h3>Silver <span>{eur(silver_t[1])}</span></h3>
  <p>{esc(silver_t[2])}</p>
  <ul>
    <li>Logo on site and stage</li>
    <li>Mention at opening and closing</li>
    <li>Swag in the participant bag</li>
    <li>Social media mention</li>
  </ul>
</div>
<h2>How the budget closes</h2>
{stacked_hbar_chart([("Funding sources", [("Nokia, Title", 25000), ("Gold ×1", 10000), ("Silver ×2", 10000), ("Credit programs", CASH_TOTAL - 45000)])], [BLUE, ORANGE, AQUA, YELLOW], width=620, label_w=150, value_fmt=eur)}
<p class="small">Gold and Silver conversations run in parallel with this one, starting with companies that already
sponsor the national AI olympiad. The last {eur(CASH_TOTAL - 45000)} is covered by any credit program
approval, which lowers the credits line. In-kind partners (a caterer, a print shop, a hardware vendor for
prizes) get Silver benefits against the value they contribute.</p>
""")

# 11. Timeline and plan
months = ["Sep", "Oct", "Nov", "Dec", "Jan", "Feb"]
phases = [
    ("Sponsor decisions, Nokia first", 0.4, 1.3),
    ("Credit applications, four providers", 0.3, 2.0),
    ("Date and venue locked", 0.8, 1.4),
    ("Site, identity, registration", 1.2, 2.2),
    ("School outreach, four counties", 1.3, 2.8),
    ("Mentor recruiting and briefing", 1.0, 2.6),
    ("Seats and credits provisioned", 2.0, 2.8),
    ("Event weekend, late November", 2.8, 3.05),
    ("Alternative weekend, 23 January", 4.7, 4.95),
    ("Report and showcase to sponsors", 3.1, 3.7),
]
page(f"""
<p class="kicker">Plan</p>
<h1>From today to the event</h1>
<p class="lead">Two candidate weekends: the end of November 2026, or 23 January 2027. UPT and UVT confirm in
early October. Everything before the date lock runs now; everything after shifts by two months if
January wins.</p>
{timeline_chart(phases, months, width=620, label_w=250)}
<h2>Milestones</h2>
<table>
<tr><th>When</th><th>What</th><th style="white-space:nowrap">Owner</th></tr>
<tr><td>Week of 21 September</td><td>This proposal reviewed with Nokia; sponsor decision requested by mid-October</td><td style="white-space:nowrap">Vlad, Daniel</td></tr>
<tr><td>By 10 October</td><td>Date and venue confirmed with UPT and UVT</td><td>Ovidiu</td></tr>
<tr><td>By 10 October</td><td>Cursor and Mistral answers on credits; Anthropic and OpenAI applications submitted</td><td style="white-space:nowrap">Vlad, Ovidiu</td></tr>
<tr><td>By 20 October</td><td>Site live, registration open on olimpiada-ai.ro, first school announcements</td><td style="white-space:nowrap">Marius, Vlad</td></tr>
<tr><td>By 10 November</td><td>10 mentors confirmed and briefed; Nokia Challenge problem statement final</td><td style="white-space:nowrap">Vlad, Nokia</td></tr>
<tr><td>Two weeks before</td><td>Registration closes, teams formed, consent forms collected, seats and credits provisioned, end-to-end test of tooling</td><td>All</td></tr>
</table>
<p class="small">Vlad Temian (agentic.tm) leads the program, sponsors and credits. Ovidiu Banias handles the
universities, date, venue and accommodation. Marius (agentic.tm) does identity, site and media.
Daniel Adrelean is the Nokia liaison.</p>
""")

# 12. Risks and next steps
page(f"""
<p class="kicker">Risks and next steps</p>
<h1>What could go wrong, and what we do about it</h1>
<table>
<tr><th>Risk</th><th>What we do</th></tr>
<tr><td>Cursor and the model providers grant nothing</td><td>The budget assumes exactly that (scenario A). Any grant is upside. Free tiers and the university GPU clusters guarantee every team can build regardless.</td></tr>
<tr><td>The date slips to January</td><td>Both weekends are held with the universities. Registration and outreach are sized for either. Sponsor money is not spent before the date is locked.</td></tr>
<tr><td>Minors and accounts</td><td>Seats are created by the organizers in one workspace, so no student signs a contract or enters a card. Parental consent covers participation and photos. An accompanying teacher per school group, medical assistance on site.</td></tr>
<tr><td>Fewer participants than planned</td><td>Food, swag and credits scale with headcount. Unspent credits and contingency are reported and returned or rolled into prizes, as the sponsor prefers.</td></tr>
<tr><td>Teams run out of credits</td><td>Per-seat caps stop one team draining the pool. The reserve covers the Sunday crunch. Open-weight models on the cluster are the fallback.</td></tr>
<tr><td>Nokia's internal tooling restrictions</td><td>Nothing runs on Nokia infrastructure. Nokia's contribution is money, people and a challenge brief.</td></tr>
</table>

<h2>Next steps</h2>
<ul>
  <li><b>This week:</b> review this proposal together, adjust the package and the prize structure to what Nokia can carry.</li>
  <li><b>By mid-October:</b> Nokia's decision on the Title Partner package, so the name can go on the site and registration materials when they launch.</li>
  <li><b>On a yes:</b> a one-page agreement listing the benefits on page 5, the amount, and the reporting Nokia receives. Invoice from the organizing entity, payable in two parts: half on signing, half after the event with the report.</li>
</ul>

<div class="callout">
<p><b>Contact</b><br>Vlad Temian, agentic.tm · me@vtemian.com<br>
Ovidiu Banias · universities and logistics</p>
</div>
<p class="small">Numbers in this document are estimates as of mid-September 2026 and are updated when quotes and
the date come in. Sources for market figures: Cursor pricing and hackathon program pages (cursor.com),
Nokia Romania careers pages and press on the Timisoara campus, provider hackathon programs
(Anthropic, OpenAI, Mistral, Groq), and the organizers' quotes from Timisoara suppliers.</p>
""")

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

if os.path.exists(CHROME):
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={OUT_PDF}", OUT_HTML.as_uri()],
                   check=True, capture_output=True)
    print(f"wrote {OUT_PDF}")

print(f"cash total {eur(CASH_TOTAL)}  in-kind {eur(IN_KIND_TOTAL)}  credits {usd(CREDITS_TOTAL_USD)} = {eur(CREDITS_TOTAL_EUR)}")
