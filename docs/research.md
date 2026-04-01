# Research: Similar Hackathons, Credit Solutions & Sponsorship

> Compiled April 1, 2026. Sources and URLs included for verification.

---

## 1. Similar Hackathons (Teen / AI / Agentic)

### Teen-Only AI Events

| Event | Organizer | Ages | Format | API/Credits | URL |
|-------|-----------|------|--------|-------------|-----|
| **Teens in AI Global Techathon** | Teens in AI (UK nonprofit) | 13-18 | Multi-phase, teams of 5-6, 101 countries. Ukraine & Albania have national stages. | Tools/mentors provided, credits not documented | [teensinai.com](https://www.teensinai.com/global-techathon/) |
| **WAICY** (World AI Competition for Youth) | ReadyAI (Pittsburgh) | K-12 | Hybrid. Has a dedicated **LLM track**. | Not documented | [waicy.org](https://www.waicy.org/) |
| **MIT RAISE Global AI Hackathon** | MIT RAISE + App Inventor | Grades 9-12 | Virtual, free. Winners flown to MIT. | Uses MIT App Inventor's built-in AI (no raw APIs) | [raise.mit.edu](https://raise.mit.edu/events/global-ai-hackathon-2025/) |
| **Masters' Union AI Hackathon** | Masters' Union (India) | Grades 9-12 | 3 rounds, finale in-person. Rs. 20 lakhs (~$24K) prizes. | **Explicitly provides APIs, cloud credits, and masterclasses** | [mastersunion.org](https://mastersunion.org/events/ai-hackathon) |
| **FutureHacks** | AiGoLearning | All students | Online, free. Solo or pairs. | Not documented | [futurehacks](https://futurehacks-7.devpost.com/) |
| **SPARK HACK** | BetterMind Labs | High school | Virtual, teams of 2-3. Healthcare/FinTech/Climate tracks. | Not documented | [bettermindlabs.org](https://www.bettermindlabs.org/hackathon) |
| **Gravitas AI Hackathon** | Stony Brook School | Grades 6-12 | 4-day virtual. Students use ChatGPT, Runway, Replit. | Students use existing free tiers | [gravitas.sbs.org](https://gravitas.sbs.org/blog/global-virtual-ai-hackathon-empowers-students-to-build-a-better-world-with-ai/) |

### Romania-Specific

| Event | Organizer | Format | Relevance |
|-------|-----------|--------|-----------|
| **Cluj Hackathon 2025 — "AI Agents Everywhere"** | Community + Bosch Cluj | 3-day, 50+ teams, MLH top-100. **A 14-year-old won 1st place.** | Closest existing event to ours. Proves teen audience is viable in Romania. |
| **UniHack** | Liga AC / UPT, Timisoara | 48hr, teams of 5, open to high school + university. MLH-sanctioned. | Same city, same university. Potential collaboration. |
| **HackTM 2026** | CJT, Timisoara | 6-day, 10K EUR prizes, has **Best AI** award. May 11-16. | Runs the week before our event! |
| **ITFest** | OSUT / UVT student org | 48hr hackathon within larger festival. | Same university (UVT). |

### Agentic-Focused (Open Age)

| Event | Key Insight |
|-------|-------------|
| **UC Berkeley LLM Agents Hackathon** (2024) | Gold standard. 3000+ participants, $200K prizes. Sponsors provided Llama endpoints, GPU credits, AWS credits. |
| **Microsoft AI Agents Hackathon** (2025) | **Did NOT provide free credits.** Used GitHub Models (free LLMs via GitHub account) as the zero-cost approach. |
| **HuggingFace Agents-MCP Hackathon** | Gave **$25 per participant** from both Anthropic and OpenAI to first 1,000 registrants. |

### Key Takeaway

**No existing event combines "teen-only" + "agentic AI" + "LLM API credits."** This hackathon occupies a genuinely novel niche. Cluj Hackathon proves the audience exists in Romania. The main precedents for credit distribution come from open-age events.

---

## 2. How Hackathons Solve the Credit Problem

### Option A: Apply to Provider Programs (Recommended First Step)

| Provider | Program | What You Get | How to Apply | Lead Time |
|----------|---------|-------------|-------------|-----------|
| **OpenAI** | Hackathon Support Program | API credits, Codex, prizes, workshops, mentoring | [openai.com/form/hackathon-support](https://openai.com/form/hackathon-support/) | **≥1 month** (apply by April 10) |
| **Anthropic** | Community Ambassadors | API credits, event funding, swag, promotion | [claude.com/community/ambassadors](https://claude.com/community/ambassadors) | Apply ASAP |
| **Anthropic** | Claude for Student Builders | ~$50/student in API credits | Through Anthropic Console | Ongoing |
| **Anthropic** | Claude Campus Program | Claude Pro + monthly API credits for university clubs | [claude.com/programs/campus](https://claude.com/programs/campus) | Cohort-based |
| **Google** | Google Cloud Credits | $300/participant via redemption codes | Via MLH partnership or direct | Varies |
| **Groq** | Hackathon Credits (self-serve) | $10/participant, $300 for best Groq project | [console.groq.com/landing/hackathon](https://console.groq.com/landing/hackathon) | Instant |
| **Together AI** | Sign-up bonus | **$100 free credits** per new account | [together.ai](https://together.ai) | Instant |
| **MLH** | Event Membership | Free, gets sponsor network access + Google/Gemini perks | [mlh.io/event-membership](https://mlh.io/event-membership) | Apply ASAP (usually 3-4 months) |

### Option B: Free Tiers (Zero-Cost Fallback)

Stack these and each participant gets substantial free access without sponsorship:

| Provider | Free Tier | Limitation |
|----------|-----------|-----------|
| Gemini 2.0 Flash | Free, rate-limited | 15 req/min |
| Mistral | Free, rate-limited | 2 req/min, 1B tokens/month |
| Groq | Free, rate-limited | Ultra-fast inference |
| OpenAI | $5 trial credits | Expires after 3 months |
| Anthropic | $5 trial credits | After phone verification |
| Together AI | $100 sign-up credits | 200+ open-source models |

**Catch for teen hackathons:** Every participant needs to create accounts. Age restrictions may apply (most require 18+ or parental consent).

### Option C: Technical Gateways (Manage Sponsored Keys)

If you get bulk API keys from sponsors, use a gateway to distribute access with per-team budgets:

| Solution | Type | Key Feature | URL |
|----------|------|-------------|-----|
| **OpenRouter Provisionary Keys** | SaaS | Generate temp keys with preset credit limits. No participant accounts needed. $5-10/key. | [openrouter.ai](https://openrouter.ai) |
| **Portkey** | SaaS | Per-team workspaces, budget alerts at 80%, rate limiting, real-time dashboard | [portkey.ai](https://portkey.ai/blog/how-to-host-an-ai-hackathon-without-losing-control-of-your-keys-or-budget/) |
| **LiteLLM Proxy** | Self-hosted (OSS) | Virtual keys, per-team budgets, 100+ providers, OpenAI-compatible | [docs.litellm.ai](https://docs.litellm.ai/docs/simple_proxy) |
| **Helicone AI Gateway** | Self-hosted (OSS) | Rust-based, per-user quotas, daily budgets | [github.com/Helicone](https://github.com/Helicone/ai-gateway) |
| **LLM-API-Key-Proxy** | Self-hosted (OSS) | Multi-provider, auto key rotation, Docker deploy | [github.com/Mirrowel](https://github.com/Mirrowel/LLM-API-Key-Proxy) |

### Option D: Microsoft's Zero-Cost Approach

Microsoft's AI Agents Hackathon provided **no credits at all**. Participants used **GitHub Models** — free LLMs accessible via a GitHub account. This sidesteps the entire credit management problem.

---

## 3. Cost Estimates for ~25 Teams

### Per-Team Spend (Based on Portkey's Data)

A team making 500-1,000 API calls over 48 hours on budget models (GPT-4o-mini, Gemini Flash, Haiku) typically spends **$5-15**.

| Scenario | Per-Team Budget | Total (25 teams) | Notes |
|----------|----------------|-------------------|-------|
| Conservative | $10-20 | $250-500 | Cheap models only |
| Moderate | $20-40 | $500-1,000 | Mix of models |
| Generous | $40-75 | $1,000-1,875 | Any model including flagship |
| **Recommended (2-3x buffer)** | — | **$1,500-3,000** | Prevents teams running out mid-hack |

Your original estimate of $50-100/team ($1,250-2,500 total per provider) is **right in the sweet spot** and very modest by industry standards.

---

## 4. Sponsorship Strategy

### Outreach Priorities (Time-Ordered)

| Priority | Action | Deadline | Notes |
|----------|--------|----------|-------|
| **NOW** | Apply to OpenAI Hackathon Support | April 10 | 1-month minimum lead time |
| **NOW** | Apply to Anthropic Community Ambassadors | April 5 | Open applications via Typeform |
| **NOW** | Apply for MLH Event Membership | April 5 | Gets Google/Gemini perks automatically |
| **This week** | Set up Groq hackathon credits | April 7 | Self-serve, instant |
| **This week** | Email Mistral DevRel | April 7 | European company angle — "EU AI company supporting EU student talent" |
| **Next week** | Email Google DevRel | April 14 | Warm lead — they already sponsor ONIA |
| **Next week** | Contact Together AI | April 14 | $100/signup is most generous |

### What Works for Outreach (Per MLH + Experienced Organizers)

- **First email:** Short, personal, NO attachments (spam filters). Just introduce the event.
- **Follow-up:** 1-2 weeks later with a 2-3 page prospectus.
- **Target:** DevRel / Developer Advocacy roles, not generic emails.
- **Best send time:** Tuesday/Thursday mornings, 8 AM in recipient's timezone.
- **Conversion rate:** ~1 sponsor per 50 cold emails. Warm intros convert much better.
- **Frame the ask around credits, not cash.** API credits cost providers pennies in compute.

### What to Offer Sponsors

Typical tier structure from comparable events:

| Tier | Contribution | What They Get |
|------|-------------|---------------|
| **Gold** | API credits for all teams + prizes | Logo on all materials, workshop slot, recruitment access, demo day presence |
| **Silver** | API credits for subset of teams | Logo on materials, mention in opening/closing |
| **Bronze** | Swag / small credit contribution | Logo on website, social media mentions |

### Warm Leads (Already in Romanian AI Education)

These companies already sponsor ONIA (Romanian AI Olympiad):
- **Bitdefender** — platinum ONIA sponsor
- **Google** — platinum ONIA sponsor
- **GitHub** — platinum ONIA sponsor
- **eMAG** — platinum ONIA sponsor

Also: **Anthropic is hiring a "Developer Community Lead - EMEA"** — they're actively building European presence. Strong angle for outreach.

---

## 5. Romanian Ecosystem Context

### olimpiada-ai.ro / ONIA

- Ministry of Education-accredited National AI Olympiad, grades 9-12
- 2026: 298 students in simulation, nationals April 17-20 at Politehnica Bucharest
- Your hackathon date (May 15-17) is confirmed; ONIA team training will adjust
- Scientific committee includes 40+ faculty from UB, Politehnica, Babes-Bolyai, UVT, UAIC

### agentic.tm

- Founded August 2025, 142 members
- 4 meetups held (Oct 2025 – Mar 2026), 12-26 attendees
- Focus: agentic coding, AI agents, AI-assisted development
- **Value:** Local technical network + mentor recruitment pool

### Timisoara Hackathon Scene

- **UniHack** (UPT/Liga AC) — MLH-sanctioned, open to high school + uni
- **HackTM 2026** — May 11-16, the week before your event
- **ITFest** (UVT/OSUT) — 48hr hackathon within festival
- **Innovation Labs** — 30hr hackathon at Cowork Timisoara

### International Pipeline

Romania already sends teams to IOAI (1 gold, 4 silver, 3 bronze in Beijing 2025). CEOAI inaugural edition in Cluj, July 2026. Two parallel national AI competition tracks exist (ONIA → IOAI, ROAI → IAIO/CEOAI).

---

## 6. Recommended Credit Strategy (Summary)

**Layer 1 — Sponsored credits (apply now):**
Apply to OpenAI, Anthropic, and Mistral programs. Target $1,500-3,000 total.

**Layer 2 — Free tiers as baseline:**
Ensure every team can use Gemini Flash, Mistral, and Groq for free regardless of sponsorship outcome.

**Layer 3 — Gateway for distribution:**
If you get bulk keys, use OpenRouter provisionary keys (easiest) or LiteLLM (most control, self-hosted).

**Layer 4 — Fallback:**
Together AI's $100 sign-up bonus + GitHub Models (free) ensure teams can build even if all sponsorship falls through.
