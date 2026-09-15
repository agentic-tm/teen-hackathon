# Agentic Hackathon: human in the loop

A weekend hackathon in Timisoara where high school and university students build AI
agents that keep a person in control. The agent proposes, the human decides.

- **When:** 27-29 November 2026, Friday 17:00 to Sunday 16:00
- **Where:** UPT, Faculty of Automation and Computers, Bd. Vasile Parvan 2, Timisoara
- **Who:** 200 participants, 140 high school students (grades 9 to 12) and 60 university
  students, from Timis, Arad, Caras-Severin and Hunedoara
- **Teams:** 100 teams of two, bring your own laptop, two judging tracks (high school,
  university)
- **Tooling:** one Cursor Teams seat per participant plus a pooled reserve; any stack,
  any model
- **Prizes:** $5,000 across two tracks plus a Nokia Challenge Award, a best
  human-in-the-loop design award and a community choice award
- **Organizers:** UPT, UVT, agentic.tm
- **Sponsors:** SpaceXAI (confirmed), Nokia (proposed Title Partner, $15,000)

Participation is free. Venue, food, drinks and dorm rooms come from UPT and UVT.

## Sponsorship proposal

`docs/nokia-sponsorship-map.pdf` is the six-page proposal for Nokia. Every number,
logo and font lives in `docs/nokia-sponsorship-map/`; the PDF and the self-contained
HTML are generated, never edited by hand.

```sh
make pdf       # rebuild docs/nokia-sponsorship-map.{html,pdf} with headless Chrome
make preview   # one PNG per page in /tmp/nokia-sponsorship-map-preview
make open      # rebuild and open the PDF
```

Needs Python 3 and Google Chrome (set `CHROME_BIN` to point at another Chromium).
A GitHub Actions workflow rebuilds and commits the PDF on every push to `main` that
touches `docs/nokia-sponsorship-map/`, so pull before editing locally.

## Other documents

`docs/` also holds the April 2026 planning and research notes on credit programs and
sponsorship. Their dates, headcounts and the olimpiada-ai.ro affiliation are out of
date; the proposal above is the current source of truth.

## Attribution

The county map in the proposal is derived from
[Romania, administrative divisions - XY.svg](https://commons.wikimedia.org/wiki/File:Romania,_administrative_divisions_-_XY.svg)
on Wikimedia Commons, CC BY-SA 3.0.
