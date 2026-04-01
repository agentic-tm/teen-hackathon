# Agentic Programming Hackathon — Planning Document

**Organizers:** agentic.tm, UPT (Politehnica University of Timisoara), UVT (West University of Timisoara)
**Part of:** [olimpiada-ai.ro](https://olimpiada-ai.ro/en/calendar)
**Date:** May 15–17, 2026 (Friday–Sunday)
**Venue:** TBD (Timisoara)
**Participants:** ~100 high school students from Romania's west region
**Format:** Team-based (~25 teams of 4)

---

## 1. Hackathon Concept

### What is it?

A 3-day hackathon where high school students build **agentic AI applications** using LLM APIs. Teams receive API credits from sponsors and free-tier signups, and use them to create projects that demonstrate autonomous agent behavior — not just chatbots, but systems that reason, plan, use tools, and take actions.

### Why agentic programming?

Agentic AI is the next frontier of applied AI. Teaching students to build agents — rather than simple prompt-and-response apps — prepares them for where the industry is heading. This hackathon gives students hands-on experience with real APIs and real constraints (budgets, rate limits, reliability).

### What makes this unique?

No existing event combines **teen-only + agentic AI + LLM API credits**. This is genuinely novel:
- Teens in AI (UK) and WAICY (US) run teen AI events but focus on general AI/data science
- Cluj Hackathon 2025 ("AI Agents Everywhere") was agentic-focused but open-age — a 14-year-old won 1st place, proving the teen audience works in Romania
- ONIA (Romania's AI Olympiad) focuses on ML model training, not building with LLM APIs
- UniHack (Timisoara) and HackTM are general tech hackathons

### Open Questions — Concept

| # | Question | Options | Notes |
|---|----------|---------|-------|
| 1 | **What does "agentic" mean for this hackathon?** Should we define a minimum bar for what counts as an "agent"? | A) Must use tool calling / function calling. B) Must have a planning/reasoning loop (not just single-shot). C) Must involve multi-step autonomous action. D) Keep it loose — any LLM-powered app is fine. | Recommendation: Option B or C. Too loose and we get chatbot wrappers. Too strict and beginners can't participate. |
| 2 | **Should we restrict which LLM providers students can use?** | A) Only sponsors' APIs (incentivizes sponsorship). B) Any provider, but we only supply credits for sponsors. C) Any provider, including open-source/local models. | Recommendation: Option C — don't restrict at all, let teams choose their stack. Credits from multiple providers will be available. |
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

## 4. LLM API Credits

> **THIS IS TOP PRIORITY.** Credits are the core resource students need.

### The Good News: Credits Are Not a Blocker

Deep research shows the credit problem is solvable through multiple independent paths. Self-serve signups alone yield ~$14,000 in credits before any sponsorship.

### Credit Budget

| Parameter | Estimate |
|-----------|----------|
| Teams | ~25 |
| Duration | ~48 hours of active hacking |
| Per-team spend (budget models) | $5–15 ([Portkey's hackathon data](https://portkey.ai/blog/how-to-host-an-ai-hackathon-without-losing-control-of-your-keys-or-budget/): 500-1,000 API calls on GPT-4o-mini/Gemini Flash) |
| Per-team budget (with buffer) | $50–100 |
| **Total needed** | **$1,500–3,000** |
| **Total achievable** | **$30,000–50,000+** (across all paths) |

### Layer 1: Self-Serve Credits (Students Sign Up — No Sponsorship Needed)

Every student creates accounts on these platforms before the event:

| Provider | Per-Student Credit | Total (100 students) | What They Get | Source |
|----------|-------------------|---------------------|---------------|--------|
| **Together AI** | $100 signup bonus | **$10,000** | 200+ open-source models (Llama 4, DeepSeek, Qwen) | [together.ai/pricing](https://www.together.ai/pricing), [community confirmation](https://thinktank.ottomator.ai/t/together-ai-offering-100-free-credits-and-deepseek-r1/4892) |
| **xAI (Grok)** | $25 signup | **$2,500** | Grok models | [xAI free credits details](https://www.getaiperks.com/en/blogs/22-xai-grok-free-credits), [API docs](https://grok-api.apidog.io/free-credits-934025m0) |
| **Gemini (Google)** | 1,000 req/day free (Flash-Lite) | **100K req/day** | Gemini 2.5 Flash-Lite, Flash, Pro | [Gemini API pricing](https://ai.google.dev/gemini-api/docs/pricing), [rate limits](https://ai.google.dev/gemini-api/docs/rate-limits) |
| **Mistral** | 1B tokens/mo free (all models) | **Massive** | Mistral Large, Small, Codestral, Pixtral | [Mistral pricing](https://mistral.ai/pricing), [Experiment plan FAQ](https://help.mistral.ai/en/articles/455206-how-can-i-try-the-api-for-free-with-the-experiment-plan) |
| **Groq** | Free tier (rate-limited) | **Free** | Llama, Mixtral — ultra-fast inference | [Groq rate limits](https://console.groq.com/docs/rate-limits), [free tier FAQ](https://community.groq.com/t/is-there-a-free-tier-and-what-are-its-limits/790) |
| **DeepSeek** | 5M tokens (~$8.40) | **$840** | DeepSeek V3, R1 | [DeepSeek pricing](https://deepseek.ai/pricing), [free tier details](https://mydeepseekapi.com/blog/deepseek-api-free-tiers) |
| **GitHub Models** | 50 req/day GPT-4o | **5,000/day** | GPT-4o, Grok-3, DeepSeek-R1, Llama | [GitHub Models docs](https://docs.github.com/en/github-models/prototyping-with-ai-models), [billing](https://docs.github.com/billing/managing-billing-for-your-products/about-billing-for-github-models) |
| **OpenAI** | $5 trial | **$500** | GPT-4o, GPT-4o-mini | [OpenAI rate limits](https://platform.openai.com/docs/guides/rate-limits) |
| **Anthropic** | $5 trial | **$500** | Claude Sonnet, Haiku | [Anthropic rate limits & tiers](https://platform.claude.com/docs/en/api/rate-limits) |

**Age caveat:** Most providers require 18+ or parental consent. Google requires 16+ in EU ([GDPR reference](https://commission.europa.eu/law/law-topic/data-protection_en)). Address this in registration.

### Layer 2: Sponsored Credits (Apply Now)

| Provider | Program | How to Apply | Expected Credits | Deadline | Source |
|----------|---------|-------------|-----------------|----------|--------|
| **OpenAI** | Hackathon Support Program | [openai.com/form/hackathon-support](https://openai.com/form/hackathon-support/) | $500–2,500 | **April 10** (1-month lead time) | [OpenAI hackathon page](https://developers.openai.com/hackathons), [community thread](https://community.openai.com/t/is-there-a-way-to-apply-for-openai-credits-for-a-hackathon-im-organizing/1028795) |
| **Anthropic** | Community Ambassadors | [Typeform](https://form.typeform.com/to/OIUYgsnS) | Monthly credits + event funding | **April 5** | [Ambassador program page](https://claude.com/community/ambassadors) |
| **Anthropic** | Student Builders (per student) | [anthropic.com/contact-sales/for-student-builders](https://www.anthropic.com/contact-sales/for-student-builders) | ~$50/student | 5-7 business days | [Program details](https://aistudentdiscount.com/claude-api-student-builder/), [Campus program](https://claude.com/programs/campus) |
| **Mistral** | Direct outreach (EU angle) | Email Sophia Yang (Head of DevRel) — [LinkedIn](https://www.linkedin.com/in/sophiamyang/), contact@mistral.ai | Hackathon API access | **April 7** | [Mistral contact](https://mistral.ai/contact), [Sophia Yang on Mistralship](https://x.com/sophiamyang/status/1862177692780495356) |
| **Mistral** | Ambassador Program | [Google Form](https://docs.google.com/forms/d/e/1FAIpQLSdBSiRzm2xBpMszB_9fBixJNyKdGnPMj99DtZbagHMdHgkGUg/viewform) | Free credits + event support | Rolling | [Ambassador docs](https://docs.mistral.ai/guides/contribute/ambassador/) |
| **Groq** | Hackathon Credits (self-serve) | [console.groq.com/landing/hackathon](https://console.groq.com/landing/hackathon) + [Discord](https://discord.gg/groq) DM DevRel | $10/participant | **April 7** | [Global Agent Hackathon (Groq sponsor)](https://github.com/global-agent-hackathon/global-agent-hackathon-may-2025) |
| **MLH** | Event Membership | [mlh.io/event-membership](https://mlh.io/event-membership) | $10/student OpenRouter + Google perks | **ASAP** (usually 3-4 months) | [MLH software resources](https://www.mlh.com/resources/software), [MLH+Google partnership](https://news.mlh.io/major-league-hacking-google-cloud-partnership-10-22-2025), [MLH+OpenRouter](https://gist.github.com/thisisryanswift/615ab9fa80590e380b46e36a1b5dcfe4) |

**Mistral pitch angle:** "European AI company supporting European student talent." Mistral is French, investing heavily in EU AI sovereignty ([€830M data center](https://sifted.eu/articles/mistral-830m-loan-data-centres), [Franco-German sovereign AI](https://planet.news/article/mistral-ai-european-expansion-march-2026), French military contract). A Romanian university hackathon is a natural fit.

**Warm leads (already sponsor ONIA — Romanian AI Olympiad):** Bitdefender, Google, GitHub, eMAG. See [olimpiada-ai.ro](https://olimpiada-ai.ro/en/calendar).

**Precedents for how much sponsors give hackathons:**
- HuggingFace Agents-MCP Hackathon: [$25/participant from Anthropic + OpenAI](https://huggingface.co/Agents-MCP-Hackathon) to first 1,000 registrants
- Anthropic Built with Opus 4.6: [$500/participant](https://www.adwaitx.com/claude-code-hackathon-opus-4-6/) (500 participants, $100K pool)
- Mistral Worldwide Hackathon: [48hr API access for all + $100/participant](https://worldwide-hackathon.mistral.ai/) for fine-tuning events
- Google EMEA Gemini Hackathon: [$300/participant](https://googlecloudgeminihackathon.devpost.com/) via new GCP accounts

### Layer 3: University Credit Programs

| Program | Credits | Who Applies | Application URL | Source / Notes |
|---------|---------|------------|-----------------|----------------|
| **Google Cloud Teaching Credits** | $50/student ($5,000 total) | UPT or UVT faculty | [edu.google.com/.../teaching](https://edu.google.com/intl/ALL_us/programs/credits/teaching/) | Romania is eligible ([country list](https://support.google.com/google-cloud-higher-ed/answer/10324705)). Faculty frames hackathon as workshop/lab. Credits valid 12 months, must use via [Vertex AI](https://cloud.google.com/vertex-ai) (not AI Studio — [billing change March 2026](https://ai.google.dev/gemini-api/docs/billing)). |
| **Google Cloud Research Credits** | Up to $5,000 | UPT/UVT professor or PhD student | [edu.google.com/.../research](https://edu.google.com/intl/ALL_us/programs/credits/research/) | Rolling applications, no deadline. "Workshop or training" is explicitly listed as eligible use. |
| **AWS Educate** | $75-100/student ($7,500-10,000) | Students with school email | [aws.amazon.com/education/awseducate](https://aws.amazon.com/education/awseducate/) | Credits work on [Amazon Bedrock](https://aws.amazon.com/bedrock/) (Claude, Llama, Mistral). [AWS confirmed Activate credits accepted for third-party Bedrock models](https://aws.amazon.com/blogs/startups/aws-activate-credits-now-accepted-for-third-party-models-on-amazon-bedrock/). |
| **Azure for Students** | $100/student ($10,000) | Students with school email, no card | [azure.microsoft.com/free/students](https://azure.microsoft.com/en-us/free/students) | Gives access to [Azure OpenAI Service](https://azure.microsoft.com/en-us/products/ai-services/openai-service) (GPT-4o). Caveat: Azure OpenAI requires [separate access approval](https://learn.microsoft.com/en-us/azure/ai-services/openai/overview#how-do-i-get-access-to-azure-openai). |

Note: Google Cloud and Azure credits give access to Gemini, GPT-4o, Claude, Mistral, and Llama through their respective AI services (Vertex AI, Azure OpenAI, Bedrock).

### Layer 4: Technical Distribution (If We Get Bulk Keys)

| Solution | Type | Best For | Source |
|----------|------|----------|--------|
| **OpenRouter Provisionary Keys** | SaaS | Simplest — generate temp keys with credit limits, 500+ models, no student accounts needed | [Provisioning docs](https://openrouter.ai/docs/features/provisioning-api-keys), [Goose workshop example](https://block.github.io/goose/blog/2025/07/29/openrouter-unlocks-workshops/) |
| **LiteLLM Proxy** | Self-hosted (free) | Maximum control — per-team budgets, 100+ providers, OpenAI-compatible | [LiteLLM docs](https://docs.litellm.ai/docs/simple_proxy) |
| **Portkey** | SaaS | Real-time dashboards, budget alerts at 80%, rate limiting | [Portkey hackathon guide](https://portkey.ai/blog/how-to-host-an-ai-hackathon-without-losing-control-of-your-keys-or-budget/) |

### Layer 5: University GPU Clusters + Local Inference

**UPT and UVT have GPU clusters** that can host open-source models for the hackathon. This is potentially the strongest fallback — zero external dependency, zero cost, high throughput.

**Setup:** Deploy open-source models (Llama 4, Mistral, DeepSeek) on university GPUs using [vLLM](https://github.com/vllm-project/vllm) or [Ollama](https://ollama.com). Expose an OpenAI-compatible API endpoint on the university network. Use [LiteLLM](https://docs.litellm.ai/docs/simple_proxy) in front to add per-team budgets and rate limits.

**Advantages over cloud APIs:**
- No age/consent issues — organizer-controlled, no student accounts needed
- No rate limits imposed by external providers
- No cost (university infrastructure)
- Full control over which models are available
- Works even if the venue WiFi is unreliable for external APIs

**Models to deploy (depending on GPU VRAM):**

| Model | VRAM Needed | Quality | Notes |
|-------|-----------|---------|-------|
| Llama 4 Scout 17B | ~12 GB (quantized) | Excellent | Meta's latest |
| Mistral Small 3.1 24B | ~16 GB (quantized) | Excellent | Strong reasoning |
| DeepSeek-V3 (quantized) | ~40 GB | Top-tier | Needs larger GPU |
| Llama 3.1 70B | ~40 GB (Q4) | Flagship | Needs A100/H100 |
| Phi-4-mini 3.8B | ~3 GB | Good for basics | Runs on any GPU |

**Open questions for UPT/UVT:**
- What GPU hardware is available? (NVIDIA A100, H100, V100, consumer GPUs?)
- How many GPUs can be allocated for the event weekend?
- Is there a sysadmin who can help with deployment?
- Can the cluster be accessed from the hackathon venue network?

**Additional fallbacks:**
- **Ollama on student laptops:** Phi-4-mini (2.5GB RAM), Llama 3.2 8B (6GB RAM). Works offline. [Ollama model library](https://ollama.com/library)
- **Buy $500 of Gemini Flash-Lite** ([$0.10/1M input tokens](https://ai.google.dev/gemini-api/docs/pricing)) — covers the entire event at paid rates.

### Open Questions — Credits

| # | Question | Options | Notes |
|---|----------|---------|-------|
| 11 | **Primary credit distribution model?** | A) Students create their own accounts on multiple providers (simplest). B) OpenRouter provisionary keys (unified, organizer-controlled). C) Mix — self-serve for free tiers, OpenRouter for sponsored credits. | Recommendation: Option C. |
| 12 | **What do we offer sponsors in return?** | A) Logo + mention in opening/closing. B) A + dedicated workshop/demo slot. C) A + B + access to winning project demos. D) Full partnership (all above + recruitment access). | Need to define sponsorship tiers. |
| 13 | **How do we handle the age/consent issue?** | A) Require parental consent forms for all account creation. B) Organizers create shared accounts and distribute keys. C) Focus on providers with no age restriction or lower thresholds. | Legal question — needs organizer decision. |

---

## 5. Participant Logistics

### Open Questions — Logistics

| # | Question | Options | Notes |
|---|----------|---------|-------|
| 14 | **Registration process** | A) Google Form. B) Custom registration page on olimpiada-ai.ro. C) Eventbrite or similar platform. | |
| 15 | **Prerequisites** — what should students know before arriving? | A) Basic programming (any language). B) Python specifically. C) No prerequisites — we'll teach everything. | Recommendation: A — basic programming. We provide API/agent workshops. |
| 16 | **Food & accommodation** | A) Organizers provide meals only (students stay locally or commute). B) Full board — meals + accommodation for out-of-town students. C) Meals provided, accommodation partnerships with local hostels/dorms. | |
| 17 | **Mentors** — who helps students during hacking? | A) University staff/PhD students from UPT and UVT. B) Industry volunteers from agentic.tm network (142 members). C) Mix of both. | Recommendation: C. agentic.tm provides technical agentic AI expertise, universities provide academic support. |

---

## 6. Ecosystem Context

### Timisoara Hackathon Scene
- **HackTM 2026:** May 11-16 (the week before us!) — 10K EUR prizes, has "Best AI" award
- **UniHack:** UPT/Liga AC, MLH-sanctioned, open to high school + university
- **ITFest:** UVT/OSUT student org, 48hr hackathon within festival

### Romanian AI Competition Pipeline
- **ONIA:** Ministry-accredited National AI Olympiad (grades 9-12). 298 students in 2026 simulation. Nationals April 17-20.
- **IOAI:** Romania sent 8 students to Beijing 2025 — 1 gold, 4 silver, 3 bronze.
- **CEOAI 2026:** Inaugural Central European AI Olympiad, July 14-19 in Cluj-Napoca.

### Our Differentiation
ONIA trains ML models. UniHack/HackTM are general tech. We teach students to **build with LLM APIs and create AI agents** — a practical skill gap that no other Romanian event fills.

---

## 7. Action Items

### P0 — This Week (by April 7)

| # | Action | Owner | Status |
|---|--------|-------|--------|
| 1 | Finalize hackathon concept (resolve questions 1–3) | All organizers | |
| 2 | Apply to OpenAI Hackathon Support | | |
| 3 | Apply to Anthropic Community Ambassadors | | |
| 4 | Apply for MLH Event Membership | | |
| 5 | Set up Groq hackathon credits | | |
| 6 | Email Mistral DevRel (Sophia Yang) | | |

### P0 — Next Week (by April 14)

| # | Action | Owner | Status |
|---|--------|-------|--------|
| 7 | UPT/UVT faculty: apply for Google Cloud Teaching Credits | | |
| 8 | UPT/UVT faculty: apply for Google Cloud Research Credits | | |
| 9 | Draft sponsor outreach email/pitch deck | | |
| 10 | Contact warm leads (Bitdefender, Google, GitHub — already sponsor ONIA) | | |

### P1 — By April 20

| # | Action | Owner | Status |
|---|--------|-------|--------|
| 11 | Confirm venue | | |
| 12 | Define challenge tracks and judging criteria | | |
| 13 | Open registration | | |
| 14 | Resolve age/consent question for API accounts | | |

### P2 — By May 1

| # | Action | Owner | Status |
|---|--------|-------|--------|
| 15 | Recruit mentors (UPT, UVT, agentic.tm) | | |
| 16 | Prepare workshop materials (LLM APIs, tool calling, agent patterns) | | |
| 17 | Build starter templates/scaffolding for students | | |

### P2 — Pre-Event (May 1–14)

| # | Action | Owner | Status |
|---|--------|-------|--------|
| 18 | Have students create accounts: Together AI, Groq, Mistral, Google AI Studio, GitHub | | |
| 19 | Set up credit distribution (OpenRouter keys or direct) | | |
| 20 | Pre-install Ollama on backup machines | | |
| 21 | Test all API access and rate limits end-to-end | | |
| 22 | Dry run of full event flow | | |
