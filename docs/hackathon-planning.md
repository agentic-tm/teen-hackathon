# Agentic Programming Hackathon — Planning Document

**Organizers:** agentic.tm, UPT (Politehnica University of Timisoara), UVT (West University of Timisoara)
**Part of:** [olimpiada-ai.ro](https://olimpiada-ai.ro/en/calendar)
**Date:** May 15–17, 2026 (Friday–Sunday)
**Venue:** TBD (Timisoara)
**Participants:** ~100 high school students from Romania's west region
**Format:** Team-based

---

## 1. Hackathon Concept

### What is it?

A 3-day hackathon where high school students build **agentic AI applications** using LLM APIs. Teams receive API credits from sponsors (Anthropic, OpenAI, Google, etc.) and use them to create projects that demonstrate autonomous agent behavior — not just chatbots, but systems that reason, plan, use tools, and take actions.

### Why agentic programming?

Agentic AI is the next frontier of applied AI. Teaching students to build agents — rather than simple prompt-and-response apps — prepares them for where the industry is heading. This hackathon gives students hands-on experience with real APIs and real constraints (budgets, rate limits, reliability).

### Open Questions — Concept

| # | Question | Options | Notes |
|---|----------|---------|-------|
| 1 | **What does "agentic" mean for this hackathon?** Should we define a minimum bar for what counts as an "agent"? | A) Must use tool calling / function calling. B) Must have a planning/reasoning loop (not just single-shot). C) Must involve multi-step autonomous action. D) Keep it loose — any LLM-powered app is fine. | Recommendation: Option B or C. Too loose and we get chatbot wrappers. Too strict and beginners can't participate. |
| 2 | **Should we restrict which LLM providers students can use?** | A) Only sponsors' APIs (incentivizes sponsorship). B) Any provider, but we only supply credits for sponsors. C) Any provider, including open-source/local models. | Recommendation: Option B — don't restrict, but only fund sponsors. |
| 3 | **What's the skill level assumption?** Most high schoolers won't have API experience. | A) Assume zero experience — Day 1 is a full workshop. B) Require basic programming as prerequisite, teach APIs on Day 1. C) Provide starter templates/scaffolding so teams can focus on the agent logic. | Recommendation: B + C. Require basic Python/JS, provide starter code. |

---

## 2. Event Structure

### Proposed Schedule

**Day 1 — Friday, May 15**
- Morning: Check-in, opening ceremony, keynote
- Late morning: Workshops (intro to LLM APIs, tool calling, agent patterns)
- Afternoon: Challenge reveal, team formation, hacking begins
- Evening: Mentor office hours

**Day 2 — Saturday, May 16**
- Full day: Hacking
- Midday: Check-in / progress demos (optional)
- Afternoon: Technical mentor sessions
- Evening: Social event / lightning talks

**Day 3 — Sunday, May 17**
- Morning: Final hacking hours, code freeze
- Midday: Team presentations / demos
- Afternoon: Judging, awards ceremony, closing

### Open Questions — Event Structure

| # | Question | Options | Notes |
|---|----------|---------|-------|
| 4 | **Venue — which university campus?** | A) UPT campus. B) UVT campus. C) Shared/alternating. D) External venue (coworking, conference center). | Need: reliable WiFi for ~100 people, power outlets everywhere, projector, breakout rooms. |
| 5 | **Team size?** | A) 3 people. B) 4 people. C) 3–5 people (flexible). | Recommendation: 4 people. ~25 teams is manageable. |
| 6 | **How do teams form?** | A) Pre-formed teams only (register as a team). B) Solo registration, teams formed on Day 1. C) Mix — can register as team or individual, individuals matched on Day 1. | Recommendation: Option C — maximizes accessibility. |
| 7 | **Do students bring their own laptops?** | A) Yes, BYOD required. B) We provide workstations. C) BYOD preferred, but have backup machines available. | Recommendation: Option A with a few backup machines. |

---

## 3. Challenges & Judging

### Open Questions — Challenges

| # | Question | Options | Notes |
|---|----------|---------|-------|
| 8 | **Challenge format — tracks or open?** | A) 2–3 defined tracks (e.g., "research agent", "data agent", "creative agent") — teams pick one. B) Single open challenge — "build the best agent for X domain." C) Fully open — build any agent you want. | Recommendation: Option A gives structure while allowing creativity. |
| 9 | **Judging criteria** — what matters most? | A) Technical sophistication (agent architecture, tool use, reasoning). B) Impact / usefulness (does it solve a real problem?). C) Creativity / novelty. D) Balanced scorecard across all three. | Recommendation: Option D with weights (e.g., 40% technical, 30% impact, 30% creativity). |
| 10 | **Prize structure** | A) Overall winners only (1st, 2nd, 3rd). B) Per-track winners + overall. C) Category awards (Best Technical, Most Creative, Best Pitch, etc.). D) Mix of B and C. | |

---

## 4. LLM API Credits — Sponsor Outreach

> **THIS IS TOP PRIORITY.** Credits are the core resource students need. Without them, the hackathon doesn't work.

### Credit Requirements Estimate

| Parameter | Estimate |
|-----------|----------|
| Teams | ~25 |
| Duration | ~48 hours of active hacking |
| Estimated usage per team | Heavy experimentation during development, moderate during final runs |
| Budget target per team | $50–100 in API credits (enough for thousands of API calls) |
| **Total credits needed** | **$1,250–2,500 per provider** (if offering multiple providers) |

### Target Providers

| Provider | Product | Contact Path | Status |
|----------|---------|-------------|--------|
| **Anthropic** | Claude API | Developer relations / education programs | Not started |
| **OpenAI** | GPT-4 / GPT-4o API | Education sponsorship program | Not started |
| **Google** | Gemini API | Google for Education / Developer programs | Not started |
| **Mistral** | Mistral API | Developer relations | Not started |
| **Groq** | Fast inference | Developer community programs | Not started |

### Open Questions — Credits & Sponsors

| # | Question | Options | Notes |
|---|----------|---------|-------|
| 11 | **How many providers should we target?** | A) One primary sponsor (simpler, deeper relationship). B) 2–3 providers (gives students choice, reduces risk). C) As many as possible (maximize resources). | Recommendation: B — 2–3 providers. More manageable than "all of them" but less risky than relying on one. |
| 12 | **What do we offer sponsors in return?** | A) Logo placement + mention in opening/closing. B) A + dedicated sponsor workshop/demo slot. C) A + B + access to winning project demos. D) Full partnership package (all above + recruitment access). | Need to define sponsorship tiers. |
| 13 | **Credit distribution model** — how do teams get credits? | A) Shared API key per provider with per-team rate limits. B) Individual API keys per team with hard spending caps. C) Provider-managed (ask sponsor to set up team accounts). | Depends on what providers offer for events. |
| 14 | **Backup plan** — what if we don't get enough sponsored credits? | A) Organizers fund credits from event budget. B) Use open-source/local models as fallback (Ollama, etc.). C) Reduce team count to match available credits. D) Mix — some sponsored, some self-funded, local model option. | Must have a plan for this. |

### Outreach Timeline

| When | What |
|------|------|
| **Now – April 15** | Draft sponsorship pitch deck / email. Identify contacts at each provider. |
| **April 15 – April 30** | Send outreach. Follow up. |
| **May 1 – May 7** | Confirm credits. Set up accounts/keys. Test access. |
| **May 8 – May 14** | Distribute credentials to team lead system. Dry run. |

---

## 5. Participant Logistics

### Open Questions — Logistics

| # | Question | Options | Notes |
|---|----------|---------|-------|
| 15 | **Registration process** | A) Google Form. B) Custom registration page on olimpiada-ai.ro. C) Eventbrite or similar platform. | |
| 16 | **Prerequisites** — what should students know before arriving? | A) Basic programming (any language). B) Python specifically. C) No prerequisites — we'll teach everything. | Recommendation: A — basic programming. We provide API/agent workshops. |
| 17 | **Food & accommodation** | A) Organizers provide meals only (students stay locally or commute). B) Full board — meals + accommodation for out-of-town students. C) Meals provided, accommodation partnerships with local hostels/dorms. | |
| 18 | **Mentors** — who helps students during hacking? | A) University staff/PhD students from UPT and UVT. B) Industry volunteers from agentic.tm network. C) Mix of both. | Recommendation: C. |

---

## 6. Next Steps — Action Items

| Priority | Action | Owner | Deadline |
|----------|--------|-------|----------|
| **P0** | Finalize hackathon concept (resolve questions 1–3) | All organizers | April 7 |
| **P0** | Draft sponsor outreach email/pitch | | April 10 |
| **P0** | Send outreach to Anthropic, OpenAI, Google | | April 15 |
| **P1** | Confirm venue | | April 15 |
| **P1** | Define challenge tracks and judging criteria | | April 20 |
| **P1** | Open registration | | April 20 |
| **P2** | Recruit mentors | | May 1 |
| **P2** | Prepare workshop materials | | May 10 |
| **P2** | Set up credit distribution system | | May 12 |
