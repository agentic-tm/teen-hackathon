# Google Programs for Free/Discounted API Credits — Deep Research

**Compiled:** 2026-04-01
**Purpose:** Exhaustive breakdown of every Google program that could provide free or discounted API credits, cloud credits, or Gemini API access for a ~100-student high school hackathon in Timisoara, Romania (May 15-17, 2026).

---

## Executive Summary

Google has **no single "hackathon credits" application form** like OpenAI does. Instead, credit access is fragmented across 10+ programs with different eligibility, amounts, and application paths. The most actionable paths for your event, in priority order:

1. **Gemini API Free Tier** (zero-cost, immediate) — usable today, no application needed
2. **MLH Event Membership** (gets you into the MLH-Google partnership pipeline)
3. **Google Cloud for Education — Teaching Credits** (via UPT/UVT faculty, Romania is eligible)
4. **Google Developer Program — $10/month credits** (per-participant, via Google AI Pro student route)
5. **Google Cloud $300 Free Trial** (per-participant, but Gemini API excluded after March 2, 2026)
6. **Google Cloud for Education — Research Credits** (via UPT/UVT faculty/PhD students)
7. **Kaggle Community Hackathons** (free platform infrastructure, no credits)
8. **Google.org AI Opportunity Fund** (long shot, Romania is eligible region)

---

## 1. Gemini API Free Tier (Google AI Studio)

**This is your baseline.** Every participant can use this with zero application or sponsorship.

### What's Free (as of March 2026)

| Model | RPM | Requests/Day | TPM | Context Window |
|-------|-----|-------------|-----|----------------|
| **Gemini 2.5 Pro** | 5 | 100 | 250,000 | 1M tokens |
| **Gemini 2.5 Flash** | 10 | 250 | 250,000 | 1M tokens |
| **Gemini 2.5 Flash-Lite** | 15 | 1,000 | 250,000 | 1M tokens |
| **Gemini 3 Flash Preview** | Limited | Limited | Limited | 1M tokens |
| **Gemini 3.1 Flash-Lite Preview** | Limited | Limited | Limited | 1M tokens |

**Also free:** Gemini Embedding model.

### Is This Enough for a Hackathon Team?

Fo shure, for prototyping. A team using Flash-Lite gets 1,000 requests/day — that is enough to build and iterate on an agent over 48 hours. Flash gives 250 requests/day with better reasoning. Pro is tight at 100 requests/day but usable for a final demo model.

**The real constraint is RPM, not RPD.** At 5-15 RPM, a team doing rapid iteration will hit rate limits. For agentic workflows that make multiple sequential LLM calls per user action, this gets tight fast.

**Practical recommendation:** Use Flash-Lite for development/testing loops, Flash for agent reasoning, Pro for final demo polish. This layered approach maximizes throughput within free tier.

### Key Caveats

- **Rate limits apply per Google Cloud project**, not per API key. Multiple keys in one project share the same quota.
- **Each participant needs their own Google account** to get their own project/quota.
- **Age restriction:** Google accounts require users to be 13+ (or 16+ in some EU countries). Romanian law follows GDPR minimum of 16 for Google account consent. **This is a problem for younger participants.** Parental consent may be needed.
- **December 2025 cuts:** Google reduced free tier limits by 50-80% in December 2025, citing fraud/abuse. The original generous limits were "only supposed to be available for a single weekend" per Google's Logan Kilpatrick.
- **Free tier data used for training:** Google's terms state "content used to improve our products" for free tier users. Paid tier opts out.
- **Daily quotas reset at midnight Pacific Time** (9 AM Romania time during summer).

### How to Get API Key

1. Go to https://aistudio.google.com
2. Sign in with Google account
3. Click "Get API Key"
4. No credit card required

**URL:** https://ai.google.dev/gemini-api/docs/pricing

---

## 2. MLH + Google Cloud Partnership (Three-Year Deal)

### What It Is

Announced October 22, 2025. A **three-year, multimillion-dollar partnership** integrating Google's Gemini models across MLH's network of 4,000+ community chapters, reaching 1M+ developers.

### What MLH Member Events Get

**Phase One (current):** Gemini featured at 250+ MLH hackathons with:
- Dedicated "Best Use of Gemini" prize category
- Workshops and developer resources
- Access to Gemini hackathon hub (https://www.mlh.com/partners/gemini)

**Credits distributed to participants:**
- **Students:** Google AI Pro free for one year (which includes $10/month in Google Cloud credits)
- **New account holders:** $300 in Google Cloud credits with a new account
- **All participants:** Access to Gemini API documentation, cookbook, and AI Studio

### How to Get This for Your Event

1. Apply for MLH Event Membership at https://mlh.io/event-membership
2. Normally requires 3-4 months lead time (tight for May 15, but possible)
3. MLH sends registered hackers emails with credit links before the event
4. 2026 season runs July 1, 2025 - June 30, 2026 (your event fits)

### What You Actually Get vs. What It Sounds Like

Be realistic here. The MLH partnership does NOT mean Google sends you a bulk credit allocation. It means:
- Participants individually claim credits through Google's existing programs
- MLH provides the links/instructions and the "Best Use of Gemini" prize framing
- The $300 new-account credits have a critical limitation (see section below)
- The $10/month via Google AI Pro is real and useful

**URL:** https://news.mlh.io/major-league-hacking-google-cloud-partnership-10-22-2025

---

## 3. Google Cloud for Education — Teaching Credits

### What It Is

Google provides cloud credits to **faculty** at accredited higher education institutions. Faculty apply on behalf of students.

### Credit Amounts

| Recipient | Amount |
|-----------|--------|
| Teaching staff | Up to **$100** per person |
| Students | Up to **$50** per student |

### Eligibility

- **Faculty only can apply.** Students cannot apply directly.
- Must be at a regionally accredited higher education institution that awards degrees
- **Romania is an eligible country** (confirmed in the European country list alongside Austria, Belgium, Bulgaria, Czech Republic, etc.)
- Does NOT support for-profit institutions
- Must use an official school email (.edu or equivalent)

### How to Apply

1. Faculty member goes to https://edu.google.com/intl/ALL_us/programs/credits/teaching/
2. Provides institutional info, faculty directory link, course details
3. Specifies expected student count and staff/TA count
4. Can apply for up to 3 courses per application

### Credit Terms

- Redeemable within **16 weeks** of approval
- Valid for **12 months** after course start date
- Course start date must be within 1 year of application
- Credits cover most Google Cloud Platform products

### Can These Be Used for Gemini API?

**Critical question.** The credits are Google Cloud credits, which means:
- **Vertex AI (which hosts Gemini models):** Likely YES — Vertex AI is a GCP product
- **Gemini API via AI Studio:** Potentially NO — AI Studio billing is separate from GCP billing as of March 2026

**Recommendation:** If applying through this route, use Vertex AI endpoint for Gemini models, not AI Studio. The API is functionally identical but bills through GCP.

### Applicability to Your Event

A UPT or UVT faculty member could apply for a "course" framed as a workshop/lab component. 100 students x $50 = **$5,000 in Google Cloud credits**. This is substantial.

**Catch:** The program is designed for semester-long courses, not 3-day hackathons. The application asks for course details. You'd need a faculty member willing to frame it as an educational workshop tied to a course.

**URL:** https://edu.google.com/intl/ALL_us/programs/credits/teaching/

---

## 4. Google Cloud for Education — Research Credits

### Credit Amounts

| Recipient | Amount |
|-----------|--------|
| Faculty / Postdoctoral researchers | Up to **$5,000** per award |
| PhD students | Up to **$1,000** per year (renewable for 5 years) |
| Nonprofit lab researchers | Up to **$5,000** |
| Masters students | **NOT eligible** |

### Eligibility

- Faculty, PhD students, postdocs at accredited higher education institutions
- Nonprofit research institutions
- 60+ approved countries (Romania likely eligible based on the teaching credits list)
- Research proposal required (max 250 words)

### What Credits Can Be Used For

- Proof of concept
- Evaluation/comparison
- Workshop or training
- Developing open source software
- Non-transferable, cannot fund commercial purposes

### Application Process

1. Go to https://edu.google.com/intl/ALL_us/programs/credits/research/
2. Submit: personal details, institution info, research proposal, expected costs, billing account ID
3. Rolling applications — no deadline
4. Credits expire 365 days from redemption or when fully used

### Applicability to Your Event

A UPT/UVT professor or PhD student could apply with a proposal framed around AI agent research. "Workshop or training" and "developing open source software" are explicitly listed as eligible uses.

$5,000 from a faculty member would cover your entire event's Google Cloud needs.

**URL:** https://edu.google.com/intl/ALL_us/programs/credits/research/

---

## 5. Google Cloud $300 Free Trial (New Accounts)

### What It Is

Every new Google Cloud account gets **$300 in credits** for 90 days. No strings attached except a credit card for identity verification.

### CRITICAL LIMITATION (March 2026 Change)

**Accounts created after March 2, 2026 CANNOT use the $300 credits for Gemini API / AI Studio usage.**

However:
- Credits **CAN** still be used for **Vertex AI** (which provides access to the same Gemini models)
- Credits CAN be used for Compute Engine, Cloud Run, BigQuery, etc.
- Accounts created **before** March 2, 2026 can still use remaining credits for Gemini API

### Applicability to Your Event

If participants access Gemini via **Vertex AI** (not AI Studio), the $300 credits should still work. This is functionally equivalent — same models, same capabilities — but uses a different API endpoint.

100 participants x $300 = $30,000 in potential credits. Even if only half create new accounts, that's $15,000.

**Catch:** Requires credit card for each account. High schoolers (especially minors) may not have credit cards. Some participants may already have Google Cloud accounts.

**URL:** https://cloud.google.com/free

---

## 6. Google Developer Program — Monthly API Credits

### What It Is

Google integrated Developer Program Premium benefits into Google AI Pro subscriptions as of January 27, 2026.

### Tiers

| Plan | Cost | Monthly Cloud Credit | Notes |
|------|------|---------------------|-------|
| **Standard (Free)** | $0 | None (just Google Skills credits) | Basic access only |
| **Premium (Google AI Pro)** | $19.99/month | **$10/month** GenAI + Cloud credits | Includes Gemini app access |
| **Premium (Monthly)** | $24.99/month | **$45/month** + $500 one-time bonus | Includes certification voucher |
| **Premium (Yearly)** | $299/year | **$550/year** + $500 bonus | Best value for sustained use |
| **Ultra** | Higher tier | **$100/month** | Premium Gemini models |

### Student Access

Students who obtained Google AI Pro through:
- Student verification (SheerID) — **EXPIRED March 11, 2026** for new sign-ups
- GitHub Student Developer Pack
- MLH membership

...can claim the $10/month credits via https://developers.google.com/program/my-benefits

### Applicability to Your Event

If students already have Google AI Pro (from the student offer or GitHub Student Pack), they can claim $10/month in credits. For a hackathon team of 4, that's $40/month — modest but real.

**Problem:** The student trial offer expired March 11, 2026. New student sign-ups can no longer get it free. Students who already had it keep it for their 12-month period.

**URL:** https://developers.google.com/program/plans-and-pricing

---

## 7. Google for Startups Cloud Program

### What It Is

Tiered credit program for startups, not directly for hackathons.

### Tiers

| Tier | Eligibility | Credits |
|------|------------|---------|
| **Start** | < 5 years old, no VC funding, minimal prior GCP credits | $2,000 for 12 months + $200 training |
| **Scale** | VC-backed (Seed-Series A) | Up to $200,000 over 2 years |
| **AI-First** | AI as core tech, equity funding Seed-Series A, < 10 years old | Up to $350,000 |

### Could a Hackathon Qualify?

**No.** This program requires:
- A registered business entity
- Active product development
- Revenue or funding stage

A university hackathon is not a startup. However, if the hackathon is organized by or through a registered nonprofit or company (e.g., agentic.tm as a registered association), the Start tier ($2,000) *might* be worth exploring.

**URL:** https://cloud.google.com/startup/benefits

---

## 8. Google Cloud for Nonprofits

### What It Is

Cloud credits for verified nonprofit organizations.

### Credits

- Up to **$10,000/year** in Google Cloud credits
- Additional **$250/month** for Google Maps Platform
- Validation through TechSoup or local equivalent

### Eligibility

- Must be a registered nonprofit
- Validated through Google for Nonprofits program
- Available in Romania

### Applicability to Your Event

If the hackathon is organized under a nonprofit entity (e.g., a registered association), this is worth applying for. $10,000/year is generous.

**Catch:** Validation process can take weeks. May not be fast enough for a May 15 event unless you already have nonprofit status.

**URL:** https://support.google.com/nonprofits/answer/16245748

---

## 9. Google Developer Student Clubs / GDG on Campus

### What It Is

Google Developer Groups on Campus (formerly GDSC) are university-based developer communities. Romania has active chapters, including **GDG on Campus at Politehnica Bucharest** (which ran OpenHack 2025).

### Credits Program

GDG on Campus does NOT have a formal credit allocation program. What they provide:
- Community infrastructure (event pages, mailing lists)
- Access to Google's "Build with AI" hackathon series
- Networking with Google DevRel
- Workshop materials and speaker support
- Potential connection to Google Cloud credits through event sponsorship

### Applicability to Your Event

Check if **UPT Timisoara** or **UVT Timisoara** has a GDG on Campus chapter. If so:
- Co-brand the hackathon as a GDG event
- Use the GDG platform for registration/promotion
- Leverage the GDG network for Google DevRel introductions

If no chapter exists, a student or faculty member could start one. But this is a medium-term play, not useful for May 15.

**URL:** https://gdg.community.dev/

---

## 10. Google.org Grants

### AI Opportunity Fund — Europe

Google.org funds nonprofits delivering AI training in Europe. **Romania is explicitly in scope** — Progress Foundation Bistrita (Romania) is already a recipient, training rural librarians with AI skills.

| Detail | Info |
|--------|------|
| **Amount** | Up to EUR 100,000 per organization |
| **Scope** | 24 countries including Romania |
| **Target** | Nonprofits upskilling underserved workers with AI |
| **Includes** | Google Cloud credits as part of accelerator participation |

### AI for Science Impact Challenge

| Detail | Info |
|--------|------|
| **Amount** | $500,000 - $3,000,000 per organization |
| **Deadline** | April 17, 2026 |
| **Scope** | Research organizations using AI for scientific breakthroughs |
| **Includes** | 6 months pro bono Google technical support + Cloud credits |

### Applicability to Your Event

These are large-scale programs for established nonprofits, not hackathon credit requests. **Not a fit for direct hackathon credits.**

However, if the hackathon is part of a broader AI education initiative (olimpiada-ai.ro), a Romanian nonprofit partner could apply to the AI Opportunity Fund for the broader program, with the hackathon as one component.

**URL:** https://aiopportunityfund.withgoogle.com/

---

## 11. Google Cloud Skills Boost (Qwiklabs)

### What It Is

Google's learning platform with hands-on labs using real Google Cloud resources.

### Credit Types (Not Cloud Credits)

| Who | Skills Boost Credits | Notes |
|-----|---------------------|-------|
| Google Cloud Innovators members | 35/month | For labs and courses |
| Students (via education program) | 200 total | One-time allocation |
| Faculty | Up to 5,000 | To distribute in courses |
| GEAR program members | 35/month | Free community program |

### Applicability to Your Event

These are **learning platform credits** (for taking courses/labs), NOT Google Cloud API credits. They cannot be used for Gemini API calls.

However, a faculty member with 5,000 Skills Boost credits could set up a pre-hackathon training program where students complete Gemini API labs.

**URL:** https://www.cloudskillsboost.google

---

## 12. Firebase / Vertex AI Credits

### Firebase

Firebase has a generous free tier (Spark plan) that includes:
- Authentication, Firestore, Realtime Database, Cloud Functions (limited invocations)
- No Gemini API access directly

### Vertex AI

Vertex AI is the **enterprise path to Gemini models** on Google Cloud. Key facts:
- Same Gemini models as AI Studio
- Bills through Google Cloud billing (so GCP credits work)
- $300 free trial credits CAN be used for Vertex AI (even after March 2026)
- Education credits CAN be used for Vertex AI
- More complex setup than AI Studio (requires GCP project, IAM, etc.)

### Applicability to Your Event

**Vertex AI is the recommended path if you obtain Google Cloud credits through any program** (education, nonprofit, free trial). It gives access to the same Gemini models but bills through GCP, where your credits are valid.

**URL:** https://cloud.google.com/vertex-ai

---

## 13. Kaggle Community Hackathons

### What It Is

Kaggle (owned by Google) now allows anyone to host community hackathons for free on their platform.

### What You Get

- Free platform infrastructure (data hosting, notebooks, discussion forums)
- Submission and judging system
- Project gallery
- Prize pools up to $10,000 permitted
- No Google Cloud credits included

### Applicability to Your Event

Could be useful as a secondary platform for submissions/judging, but does NOT solve the credits problem.

**URL:** https://blog.google/innovation-and-ai/technology/developers-tools/introducing-kaggle-community-hackathons/

---

## 14. Google-Run Hackathons (Reference — What They Give Participants)

These show what Google considers normal credit allocations:

| Hackathon | Credits to Participants | Prizes |
|-----------|------------------------|--------|
| **Google Cloud Gemini Hackathon (EMEA)** | $300/participant (new accounts) | Not specified |
| **ADK (Agent Development Kit) Hackathon** | Not specified | $15,000 + $3,000 GCP credits (winner) |
| **GKE Turns 10 Hackathon** | Not specified | $15,000 + $3,000 GCP credits (winner) |
| **Gemini 3 Hackathon (DeepMind)** | Not specified | $100,000 prize pool |
| **Gemini Live Agent Challenge** | Not specified | $25,000 + $3,000 GCP credits (winner) |
| **Google Cloud x MLB Hackathon** | Not specified | $20,000 + $5,000 GCP credits (winner) |
| **Vertex AI Agent Builder Hackathon** | Not specified | $3,000 + $1,000 GCP credits (winner) |
| **BigQuery AI Hackathon** | Not specified | $100,000 prize pool |

**Pattern:** Google gives credits as **winner prizes** ($1,000-$5,000 GCP credits), not bulk participant allocations. The EMEA Gemini Hackathon was an exception where all participants got $300 via new-account credits.

**Key insight:** Romania was explicitly listed as an eligible country for the EMEA Gemini Hackathon. Google is willing to target Romanian developers.

---

## 15. Gemini API Paid Tier Pricing (If You Need to Buy Credits)

If free tier + education credits aren't enough, here's what paid usage costs:

### Most Relevant Models for Hackathon

| Model | Input (per 1M tokens) | Output (per 1M tokens) | Best For |
|-------|----------------------|------------------------|----------|
| **Gemini 2.5 Flash-Lite** | $0.10 | $0.40 | High-volume, simple tasks |
| **Gemini 2.5 Flash** | $0.30 | $2.50 | Agent reasoning, good balance |
| **Gemini 2.5 Pro** | $1.25 (<=200K) / $2.50 (>200K) | $10.00 / $15.00 | Complex reasoning, demos |
| **Gemini 3 Flash Preview** | $0.50 | $3.00 | Latest capabilities |

### Cost Estimate for Your Event

Assuming 25 teams, each making 500-1,000 API calls over 48 hours using Flash models:
- **Per-team cost:** $5-15 on Flash-Lite, $15-40 on Flash, $40-100 on Pro
- **Total (Flash-Lite):** $125-375
- **Total (Flash mix):** $375-1,000
- **Total (Pro-heavy):** $1,000-2,500

Flash-Lite is absurdly cheap. Even without any credits, $500 of paid usage would cover the entire event.

---

## Recommended Strategy for Your Event

### Tier 1 — Do Immediately (Free, No Application)

1. **Have every participant create a Google AI Studio account** and generate a free API key
2. **Use Gemini 2.5 Flash-Lite** as the default development model (1,000 req/day free)
3. **Use Gemini 2.5 Flash** for agent reasoning tasks (250 req/day free)
4. **Use Gemini 2.5 Pro** sparingly for complex tasks (100 req/day free)

### Tier 2 — Apply This Week (1-2 Week Lead Time)

5. **Ask a UPT or UVT faculty member to apply for Teaching Credits:** $50/student x 100 = $5,000 in GCP credits. Use via Vertex AI endpoint.
6. **Ask a UPT/UVT professor or PhD student to apply for Research Credits:** Up to $5,000.
7. **Apply for MLH Event Membership** to get into the Google/Gemini partnership pipeline.

### Tier 3 — Pursue if Tier 2 Succeeds

8. **Route all sponsored credits through Vertex AI** (not AI Studio) so GCP credits work.
9. **Set up a LiteLLM proxy** with Vertex AI backend to distribute access with per-team budgets.

### Tier 4 — Fallback

10. **If all else fails, buy $500 of Gemini Flash-Lite credits.** This covers the entire event. At $0.10/1M input tokens + $0.40/1M output tokens, a team could make thousands of calls for under $20.

---

## Key Contacts and URLs

| Resource | URL |
|----------|-----|
| Gemini API Pricing | https://ai.google.dev/gemini-api/docs/pricing |
| Gemini API Rate Limits | https://ai.google.dev/gemini-api/docs/rate-limits |
| Google AI Studio (get free API key) | https://aistudio.google.com |
| Google Cloud Education — Teaching Credits | https://edu.google.com/intl/ALL_us/programs/credits/teaching/ |
| Google Cloud Education — Research Credits | https://edu.google.com/intl/ALL_us/programs/credits/research/ |
| Google Cloud Education — Eligibility | https://support.google.com/google-cloud-higher-ed/answer/10324705 |
| Google Cloud Free Trial ($300) | https://cloud.google.com/free |
| Google for Startups | https://cloud.google.com/startup/benefits |
| Google for Nonprofits | https://support.google.com/nonprofits/answer/16245748 |
| Google Developer Program Benefits | https://developers.google.com/program/my-benefits |
| MLH + Google Partnership Announcement | https://news.mlh.io/major-league-hacking-google-cloud-partnership-10-22-2025 |
| MLH Gemini Hackathon Hub | https://www.mlh.com/partners/gemini |
| MLH Event Membership Application | https://mlh.io/event-membership |
| GDG on Campus Directory | https://gdg.community.dev/ |
| Google.org AI Opportunity Fund | https://aiopportunityfund.withgoogle.com/ |
| Kaggle Community Hackathons | https://www.kaggle.com/competitions |
| Google Cloud Hackathon Toolkit (GitHub) | https://github.com/GoogleCloudPlatform/hackathon-toolkit |
| Vertex AI | https://cloud.google.com/vertex-ai |
| Google Cloud Gemini Hackathon (EMEA, archived) | https://googlecloudgeminihackathon.devpost.com/ |

---

## Sources

- [Gemini API Pricing — Google AI for Developers](https://ai.google.dev/gemini-api/docs/pricing)
- [Gemini API Rate Limits — Google AI for Developers](https://ai.google.dev/gemini-api/docs/rate-limits)
- [Gemini API Free Tier Complete Guide (2026)](https://www.aifreeapi.com/en/posts/gemini-api-free-tier-complete-guide)
- [Google Cloud Free Trial and Free Tier](https://cloud.google.com/free)
- [Google Cloud Education Programs Overview](https://cloud.google.com/edu)
- [Google Cloud Teaching Credits](https://edu.google.com/intl/ALL_us/programs/credits/teaching/)
- [Google Cloud Research Credits](https://edu.google.com/intl/ALL_us/programs/credits/research/)
- [Google Cloud Education Eligibility](https://support.google.com/google-cloud-higher-ed/answer/10324705)
- [Google Cloud Education Program Info](https://support.google.com/google-cloud-higher-ed/answer/10723679)
- [Google Cloud Billing — Education Credits](https://docs.cloud.google.com/billing/docs/how-to/edu-grants)
- [Google for Startups Benefits](https://cloud.google.com/startup/benefits)
- [2026 Ultimate Guide to Google for Startups](https://medium.com/google-cloud/the-2026-ultimate-guide-to-google-for-startups-4117c0c34416)
- [Google Cloud for Nonprofits Credits](https://support.google.com/nonprofits/answer/16245748)
- [MLH + Google Cloud Partnership Announcement](https://news.mlh.io/major-league-hacking-google-cloud-partnership-10-22-2025)
- [MLH Gemini Partner Page](https://www.mlh.com/partners/gemini)
- [Google Developer Program Plans & Pricing](https://developers.google.com/program/plans-and-pricing)
- [Google AI Pro Developer Credits Integration](https://www.adwaitx.com/google-ai-pro-developer-program-cloud-credits/)
- [Google AI Pro Student Trial](https://support.google.com/gemini/answer/16417758)
- [Gemini API Billing — Free Trial Exclusion](https://ai.google.dev/gemini-api/docs/billing)
- [Free Trial Credits Not Applied to Gemini API (Forum)](https://discuss.ai.google.dev/t/free-trial-credits-not-applied-to-gemini-api-usage-via-ai-studio/135129)
- [Google Cloud Gemini Hackathon EMEA (Devpost)](https://googlecloudgeminihackathon.devpost.com/)
- [Google Cloud Hackathon Toolkit (GitHub)](https://github.com/GoogleCloudPlatform/hackathon-toolkit)
- [GDG on Campus — Politehnica Bucharest](https://gdg.community.dev/gdg-on-campus-national-university-of-science-and-technology-politehnica-bucharest-bucharest-romania/)
- [Google.org AI Opportunity Fund](https://aiopportunityfund.withgoogle.com/)
- [Google.org AI Opportunity Fund — Europe Recipients](https://blog.google/outreach-initiatives/google-org/googleorg-ai-opportunity-fund-europe/)
- [Google.org AI for Science Impact Challenge](https://grantedai.com/grants/google-org-impact-challenge-ai-for-science-2026-google-org-a1b2c3d4)
- [Kaggle Community Hackathons Announcement](https://blog.google/innovation-and-ai/technology/developers-tools/introducing-kaggle-community-hackathons/)
- [Introducing Kaggle Community Hackathons (Dev.to)](https://dev.to/googleai/now-anyone-can-host-a-global-ai-challenge-on-kaggle-2hp6)
- [Google Cloud Research Credits Expand to Nonprofit Researchers](https://cloud.google.com/blog/topics/public-sector/google-cloud-research-credits-expand-nonprofit-researchers)
- [2026 Developer's Guide to Free Google Cloud Credits](https://dev.to/behruamm/the-2026-developers-guide-to-free-google-cloud-credits-for-ai-side-projects-1ac5)
- [Google Gemini Student Plan — 120+ Countries Guide](https://www.aifreeapi.com/en/posts/gemini-student-plan)
