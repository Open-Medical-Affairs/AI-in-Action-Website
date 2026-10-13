# 02 · Insights Engine: agenda and facilitator guide

**AI in Action for Medical Affairs** · October 13–14, 2026 · Convene (2nd floor), Two Commerce Square, 2001 Market St, Philadelphia · Host and keynote: Vivek Mukhatyar · Companion site: [aiinaction.up.railway.app](https://aiinaction.up.railway.app)

> **Assumption:** one team per vertical (four teams). The Day 1 afternoon agenda below is an optional suggestion; teams may move faster or slower.

## At a glance

| | |
|---|---|
| Vertical | 02 · Insights Engine: *From field insights to care and knowledge gaps to curated HCP content for each persona and stage.* |
| Warm-up missions | [`field-insights`](https://aiinaction.up.railway.app/missions/field-insights) · Level 2 Pair · "What should leadership know?"; [`medical-information`](https://aiinaction.up.railway.app/missions/medical-information) · Level 1 Starter · "Handle the enquiry queue" |
| Facilitators | John and Anjali (insights pillar leads) |
| Lead skill for the hack | [`field-insight-synthesis`](https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills/blob/HEAD/skills/field-insight-synthesis/SKILL.md) |
| Practice data | Any TA; synthetic data (fictional Nordvant Biopharma) with seeded safety findings and a promotional objective to catch. |
| Day 2 presentation | This team presents second (02 of 04): teams present in order 01→04 after the final build, about 20 minutes each including a few questions |

## 1. Challenge statement

Field insights, enquiries and needs assessments point to the same care and knowledge gaps, but the signal rarely reaches the content plan. A community specialist new to the data and an academic expert get the same deck.

## 2. Sharpened problem prompt

> Build an AI workforce that reads field observations, enquiries and the needs assessment, raises safety findings first, and names care and knowledge gaps (source IDs, confidence). It segments HCPs by persona and knowledge stage (aware, exploring, applying, expert), maps gaps to those cells, and curates a draft content plan: reuse, adapt or create, with the gap each item closes. Humans approve gaps and segments; MLR reviews new items.

Teams can keep this prompt or narrow it to one workflow they know. A good narrowed prompt names the role, the trigger, the deliverable and the decision it serves.

## 3. Day 1 afternoon: suggested agenda (Tue Oct 13)

Context: Day 1 morning: registration, opening keynote and sandbox intro, team creation and function audit; lunch; then **the build afternoon** (four blocks, about 3¼ hours in all); evening cocktail reception. All durations below are approximate.

| About | Block (in order) | Done looks like |
|---|---|---|
| about 30 min | 1 · Set up Grok Bot and load the skills | Every member signed in; the driver's conversation has the skills loaded and has read one practice file; capture log started |
| about 40 min | 2 · Warm-up missions: `field-insights` + `medical-information` | Field insights (safety finding raised first) and an enquiry register exist; the team agreed one shared gap; 3 observations logged |
| about 45 min | 3 · Workflow ideation: the gap-to-content cycle | The gap-to-content cycle mapped; one problem chosen; hours per cycle and number of people involved estimated; ideas marked Efficiency or Opportunity |
| about 80 min (about 1½ hours) | 4 · The hack: build the Insights Engine swarm | Gap table with source IDs, persona × stage matrix and draft content plan with MLR pack, stopping at both gates; safety list first; screenshots and timings captured |

Suggested roles (rotate if you like): **driver** (types into Grok Bot), **navigator** (reads the mission and pushes back), **scribe** (owns the capture log), **timekeeper and presenter**.

### Block 1 · Set up Grok Bot and load the skills (about 30 min)

| About | What happens (in order) |
|---|---|
| about 5 min | Huddle: agree roles and pick one practice therapeutic area (TA). |
| about 10 min | Everyone opens [https://aiinaction.up.railway.app/grokbot](https://aiinaction.up.railway.app/grokbot): event sign-up link, credits code (both shared at the conference), new conversation. Can't open GitHub? Upload the starter bundle linked on that page. |
| about 10 min | The driver pastes the setup prompt below. Others follow along on their own laptops. |
| about 5 min | Smoke test passes (skills listed, a SYNTHETIC file read). The scribe pastes the capture-log instructions ([final-presentation-agent-instructions.md](final-presentation-agent-instructions.md)) into the conversation and starts [capture-log-template.md](capture-log-template.md). |

Setup prompt (paste into Grok Bot; replace the TA):

```
Use https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills
Read AGENTS.md. We are the Insights Engine team at AI in Action for Medical Affairs.
Load medical-affairs-foundations and these skills: field-insight-synthesis, insight-generation, evidence-gap-analysis, scientific-communication-strategy, medical-content-operations, mlr-review-readiness.
Use the practice data in https://github.com/Open-Medical-Affairs/Data-Sources: synthetic/[oncology-mm | immunology-ad | cardiometabolic-obesity]/ and synthetic/connected/ (the practice CRM). It is fictional (Nordvant Biopharma).
First, only: list the skills you loaded, then show the first 5 rows of field-observations.csv and confirm the file is labelled SYNTHETIC. Do not start a mission yet.
Do not ask me to connect company systems. Do not send, post or change anything outside this conversation.
```

**Done looks like:** all members have a working Grok Bot; the agent lists the loaded skills and shows a file marked SYNTHETIC; the capture log exists.

### Block 2 · Warm-up missions (about 40 min)

- **Pair A:** [`field-insights`](https://aiinaction.up.railway.app/missions/field-insights) · Level 2 Pair · "What should leadership know?". Field observations to insights. Watch for the safety finding the agent should raise before any analysis, then ask which insights point to a care or knowledge gap.
- **Pair B:** [`medical-information`](https://aiinaction.up.railway.app/missions/medical-information) · Level 1 Starter · "Handle the enquiry queue". The enquiry queue is a second gap signal: what HCPs keep asking tells you what they do not yet know.
- Simpler alternative: [`msl-post-call`](https://aiinaction.up.railway.app/missions/msl-post-call) · Level 1 Starter · "Turn the call notes into useful follow-up" (one MSL's notes to CRM draft). Background reading: [Team mission 2](https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills/blob/HEAD/workshop/missions/mission-2.md) ("Find what humans would miss").

| About | What happens (in order) |
|---|---|
| about 5 min | Split into two pairs. Pair A opens /missions/field-insights, Pair B opens /missions/medical-information. Same practice TA. |
| about 20 min | Run both missions in parallel. When the agent raises a safety finding, stop and read it aloud to the team. |
| about 10 min | Push on it: "Which of these is a knowledge gap, which is a care gap, and which is just noise?" then "Which HCPs have that gap, and what do they already know?" |
| about 5 min | Swap outputs. Scribe logs: did the safety scan happen first? Were source IDs kept? One gap both pairs found. |

**Done looks like:** at least one finished draft deliverable; the team saw where the agent stopped for a human (safety scan first, human is the final judge); three observations in the capture log ("it was good at…", "it missed…", "we had to decide…").

### Block 3 · Workflow ideation (about 45 min)

| About | What happens (in order) |
|---|---|
| about 15 min | **Map today's workflow** for one real gap-to-content cycle (from field insights to care and knowledge gaps to a curated, MLR-reviewed HCP content plan): steps, who does each, hand-offs, waiting time, hours. Sticky notes or a whiteboard; photograph it for the log. |
| about 10 min | **Spot the AI ideas.** Mark each step **E** (Efficiency AI: do today's work faster) or **O** (Opportunity AI: something not possible today). Use the examples in section 8 to spark ideas. Dot-vote. |
| about 10 min | **Pick one problem.** Write it as: "When [role] needs [outcome], today it takes [time] because [cause]." Fill the baseline column of the impact worksheet (section 12). |
| about 10 min | **Sketch the swarm** on paper: one lead agent, 3–5 sub-agents, the skill each loads, the hand-offs, and two human gates (section 9). Optional: the [Optimizer](https://aiinaction.up.railway.app/optimizer) "Agent swarm / coordinator" task. |

**Done looks like:** a photo of today's workflow; ideas marked E or O; one problem statement; baseline hours and frequency estimated; a swarm sketch with two gates. All in the capture log.

### Block 4 · The hack: build the swarm (about 80 min)

| About | What happens (in order) |
|---|---|
| about 10 min | Write the assignment (starter below, or the [Optimizer](https://aiinaction.up.railway.app/optimizer) in swarm mode). Missing a skill? Use the **Skill creator** on the Optimizer page; read every SKILL.md it produces and approve it before use. |
| about 35 min | **Run 1.** Lead agent plans, sub-agents work; stop at Gate 1 (the gap list, the persona × stage segmentation and the safety routing) and make the decision as a team. Note the minutes. |
| about 5 min | Optional stretch break. |
| about 20 min | **Run 2.** Fix the weakest hand-off (add a house rule, tighten a context packet), then run through Gate 2 (MLR approves each new or adapted item and the medical lead signs off the plan). Optional stress test with a change card. |
| about 10 min | **Capture.** Screenshots of the plan, a hand-off and each gate; timing notes; ask the agent to update the capture log and draft the slide outline from the template. Save everything. |

Reference missions: [`field-insights`](https://aiinaction.up.railway.app/missions/field-insights) · Level 2 Pair · "What should leadership know?" for the insight core, [`connected-planning`](https://aiinaction.up.railway.app/missions/connected-planning) · Level 3 Team · "Work across a practice CRM and content library" for working across the practice CRM and content library, [`launch-plan-swarm`](https://aiinaction.up.railway.app/missions/launch-plan-swarm) · Level 4 Swarm · "Build the whole medical launch plan" for the wave-and-gate pattern.

Assignment starter (paste into Grok Bot, then edit the [brackets]):

```
# Assignment: Insights Engine swarm
You are the Gap Lead, a lead agent coordinating a small team of digital workers for a Medical Affairs team. This is an assignment, not a question: plan, delegate, check and hand back finished drafts.

## Goal: what done looks like
[One sentence: the problem we picked in ideation, and the deliverable that solves it.]

## Context to use
- https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills : read AGENTS.md, load medical-affairs-foundations, your lead skill field-insight-synthesis, and the skills named below.
- Practice data (fictional): https://github.com/Open-Medical-Affairs/Data-Sources synthetic/[TA]/ and synthetic/connected/. Or our own non-confidential data: [describe].

## How to work
1. Show me a short plan and the org chart of workers first. Wait for my OK.
2. Scan human-sourced records for possible safety findings (adverse events, product complaints, off-label use) before anything else. List them verbatim and stop until I acknowledge.
3. Run these sub-agents, each with only the context it needs:
   - Safety Sentinel (skills: medical-affairs-foundations (safety scan)): Reads every record first; lists possible AEs, PQCs and off-label mentions verbatim and stops for routing. Hands off: Simulated safety escalation list.
   - Gap Analyst (skills: insight-generation + evidence-gap-analysis): Turns field insights, enquiries and the needs assessment into care and knowledge gaps with source IDs and confidence. Hands off: Gap table.
   - Segmenter (skills: spreadsheet-analysis + data-connection): Groups HCPs by persona and knowledge stage and maps each gap to the cells it affects. Hands off: Persona × stage matrix.
   - Content Curator (skills: scientific-communication-strategy + medical-content-operations): Matches each cell to the content library: reuse, adapt or create, with format and channel. Hands off: Draft HCP content plan.
   - MLR Prep (skills: mlr-review-readiness): Lists claims, references and fair-balance points for every new or adapted item; flags anything promotional. Hands off: MLR readiness pack.
4. STOP at Gate 1: After the Segmenter: the insights pillar leads approve the gaps, the persona × stage segments and the safety routing before content is curated. Show me the evidence pack and wait.
5. Continue, then have an independent checker (deliverable-quality-review (reports to the human, not the lead)) review the draft. Fix what it finds.
6. STOP at Gate 2: After MLR Prep: MLR reviewers approve each new or adapted item and the medical lead signs off the plan before anything reaches an HCP. Wait for my decision.
7. Keep a timing note: minutes per step, and minutes of human review at each gate.

## House rules
- Never invent a citation, number, quote or meeting fact. Unsupported claims are marked and left for a human.
- Keep source IDs on every claim. Keep public evidence separate from fictional practice data.
- Do not send, post, publish or change any external system. Drafts only. Mark every output DRAFT and the data FICTIONAL.
```

**Done looks like:** the swarm ran end to end at least once on practice data; it stopped at Gate 1 and Gate 2 and the team made both decisions; screenshots and minute-level timings are in the capture log; the agent has drafted a slide outline.

**End of the afternoon: no formal share-out.** Teams go to the cocktail reception. During the afternoon, facilitators walk around and ask the questions in section 10; near the end of the afternoon they check that every team has saved screenshots and its capture log.

## 4. Day 2 morning: final build and presentation (Wed Oct 14)

Context: Day 2 morning: breakfast · **hackathon final build and team presentations** · interactive demo by WPP · closing panel.

| About | What happens (in order) |
|---|---|
| about 5 min | Re-open yesterday's conversation. The agent re-reads the capture log. |
| about 20 min | One last build fix at most. The agent fills the [final presentation template](template/AI-in-Action-Final-Presentation-Template.pptx) using the [agent instructions](final-presentation-agent-instructions.md). |
| about 5 min | Team review: no [brackets] left, impact numbers are the team's own, practice data marked fictional, the LIVE DEMO slide left empty, backup screenshots in place. |
| about 5 min | Rehearse the demo and the first two slides. Hand the deck to the AV desk / presentation laptop. |
| a couple of minutes | MC opens the session. |
| **about 20 min** | **Insights Engine presents second (02 of 04)** (about 20 minutes, give or take, including a short live demo and a few questions). |

> **Timing.** The final build and rehearsal take about 30–40 min at the start of Day 2; then teams present in order 01→04, about 20 minutes each including a few questions, before the WPP demo. The morning build is short, so keep all decks on one laptop and treat the capture step near the end of Day 1 as essential. Watch the other teams; make final edits only in the minutes before your turn.

## 5. Recommended missions

| Mission (link) | Why |
|---|---|
| [`field-insights`](https://aiinaction.up.railway.app/missions/field-insights) · Level 2 Pair · "What should leadership know?" | Warm-up (Pair A). Field observations to insights. Watch for the safety finding the agent should raise before any analysis, then ask which insights point to a care or knowledge gap. |
| [`medical-information`](https://aiinaction.up.railway.app/missions/medical-information) · Level 1 Starter · "Handle the enquiry queue" | Warm-up (Pair B). The enquiry queue is a second gap signal: what HCPs keep asking tells you what they do not yet know. |
| [`connected-planning`](https://aiinaction.up.railway.app/missions/connected-planning) · Level 3 Team · "Work across a practice CRM and content library" | Hack reference: lead skill plus sub-workers across CRM tables (HCPs, interactions, content assets). |
| [`thirty-day-capstone`](https://aiinaction.up.railway.app/missions/thirty-day-capstone) · Level 3 Team · "Run the next 30 days of Medical Affairs" | Optional stretch: shows how a content plan feeds a 30-day action tracker. |
| [`launch-plan-swarm`](https://aiinaction.up.railway.app/missions/launch-plan-swarm) · Level 4 Swarm · "Build the whole medical launch plan" | The only Level 4 mission: waves of digital workers with human gates between waves. Use it as the model for your swarm. |
| [Team mission 2](https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills/blob/HEAD/workshop/missions/mission-2.md) | Background: the original team mission behind this vertical. |

Levels: 1 Starter = one skill · 2 Pair = lead + one sub-worker · 3 Team = lead + two or more sub-workers · 4 Swarm = waves with human gates. All missions: [https://aiinaction.up.railway.app/missions](https://aiinaction.up.railway.app/missions). Ready prompts: [https://aiinaction.up.railway.app/prompts](https://aiinaction.up.railway.app/prompts).

## 6. Recommended skills

| Skill (Medical-Affairs-Skills) | Use it for |
|---|---|
| [`field-insight-synthesis`](https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills/blob/HEAD/skills/field-insight-synthesis/SKILL.md) | Lead: field observations to insights |
| [`insight-generation`](https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills/blob/HEAD/skills/insight-generation/SKILL.md) | Observation vs insight: what changes a decision |
| [`evidence-gap-analysis`](https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills/blob/HEAD/skills/evidence-gap-analysis/SKILL.md) | Name the care or knowledge gap behind an insight |
| [`spreadsheet-analysis`](https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills/blob/HEAD/skills/spreadsheet-analysis/SKILL.md) | Segment HCPs and count the persona × stage cells |
| [`medical-information-response`](https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills/blob/HEAD/skills/medical-information-response/SKILL.md) | Read the enquiry queue as a gap signal |
| [`data-connection`](https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills/blob/HEAD/skills/data-connection/SKILL.md) | Work across the practice CRM tables and content library |
| [`scientific-communication-strategy`](https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills/blob/HEAD/skills/scientific-communication-strategy/SKILL.md) | Key messages by audience and knowledge stage |
| [`medical-content-operations`](https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills/blob/HEAD/skills/medical-content-operations/SKILL.md) | Reuse, adapt or create from the content library |
| [`medical-education-program`](https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills/blob/HEAD/skills/medical-education-program/SKILL.md) | Keep education independent and objectives non-promotional |
| [`mlr-review-readiness`](https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills/blob/HEAD/skills/mlr-review-readiness/SKILL.md) | Get every new or adapted item ready for MLR |
| [`deliverable-quality-review`](https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills/blob/HEAD/skills/deliverable-quality-review/SKILL.md) | Independent red-team of the draft plan |
| [`medical-affairs-foundations`](https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills/blob/HEAD/skills/medical-affairs-foundations/SKILL.md) | Safety-first rules (loaded with every mission) |

Every skill: [https://aiinaction.up.railway.app/skills](https://aiinaction.up.railway.app/skills) · library: [github.com/Open-Medical-Affairs/Medical-Affairs-Skills](https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills). Workflow not covered? Build a skill with the Skill creator on [https://aiinaction.up.railway.app/optimizer](https://aiinaction.up.railway.app/optimizer) and review it before use.

## 7. Practice data

All practice data are fictional (Nordvant Biopharma; NORVANTIB in multiple myeloma, DERMALYX in atopic dermatitis, ADIPOSYN in obesity; plus a practice CRM). Browse and copy links at [https://aiinaction.up.railway.app/data](https://aiinaction.up.railway.app/data). Teams may instead bring their own **non-confidential** data (no patient data, no confidential company data, no real HCP personal data).

**TA pack files** (pick one TA; links: MM · AD · Obesity), folder: [synthetic/](https://github.com/Open-Medical-Affairs/Data-Sources/tree/main/synthetic)

- `field-observations.csv` ([MM · NORVANTIB](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/oncology-mm/field-observations.csv) · [AD · DERMALYX](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/immunology-ad/field-observations.csv) · [Obesity · ADIPOSYN](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/cardiometabolic-obesity/field-observations.csv))
- `medical-plan.md` ([MM · NORVANTIB](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/oncology-mm/medical-plan.md) · [AD · DERMALYX](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/immunology-ad/medical-plan.md) · [Obesity · ADIPOSYN](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/cardiometabolic-obesity/medical-plan.md))
- `medical-education-needs.md` ([MM · NORVANTIB](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/oncology-mm/medical-education-needs.md) · [AD · DERMALYX](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/immunology-ad/medical-education-needs.md) · [Obesity · ADIPOSYN](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/cardiometabolic-obesity/medical-education-needs.md))
- `medical-information-enquiries.csv` ([MM · NORVANTIB](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/oncology-mm/medical-information-enquiries.csv) · [AD · DERMALYX](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/immunology-ad/medical-information-enquiries.csv) · [Obesity · ADIPOSYN](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/cardiometabolic-obesity/medical-information-enquiries.csv))
- `interaction-notes.md` ([MM · NORVANTIB](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/oncology-mm/interaction-notes.md) · [AD · DERMALYX](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/immunology-ad/interaction-notes.md) · [Obesity · ADIPOSYN](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/cardiometabolic-obesity/interaction-notes.md))
- `guideline-landscape.md` ([MM · NORVANTIB](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/oncology-mm/guideline-landscape.md) · [AD · DERMALYX](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/immunology-ad/guideline-landscape.md) · [Obesity · ADIPOSYN](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/cardiometabolic-obesity/guideline-landscape.md))
- `evidence-landscape.md` ([MM · NORVANTIB](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/oncology-mm/evidence-landscape.md) · [AD · DERMALYX](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/immunology-ad/evidence-landscape.md) · [Obesity · ADIPOSYN](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/cardiometabolic-obesity/evidence-landscape.md))
- `mlr-review-comments.md` ([MM · NORVANTIB](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/oncology-mm/mlr-review-comments.md) · [AD · DERMALYX](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/immunology-ad/mlr-review-comments.md) · [Obesity · ADIPOSYN](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/cardiometabolic-obesity/mlr-review-comments.md))

**Practice CRM** ([synthetic/connected/](https://github.com/Open-Medical-Affairs/Data-Sources/tree/main/synthetic/connected/))

- [`hcps.csv`](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/connected/hcps.csv)
- [`interactions.csv`](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/connected/interactions.csv)
- [`engagement.csv`](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/connected/engagement.csv)
- [`content_assets.csv`](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/connected/content_assets.csv)
- [`enquiries.csv`](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/connected/enquiries.csv)
- [`data-dictionary.json`](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/connected/data-dictionary.json)

Synthetic (fictional Nordvant Biopharma). hcps.csv gives setting and channel for personas; content_assets.csv is the library (audience, format, review status). Keep source IDs (e.g. OBS-001) on every gap.

## 8. Example AI ideas

**Efficiency AI** (today's work, faster)

1. Field observations, enquiries and the needs assessment coded into one gap list with source IDs, in minutes instead of weeks.
2. HCPs segmented by persona and knowledge stage automatically, with the reasons for each assignment visible.
3. A first-draft content plan that reuses what is already in the library before anything new is written, ready for MLR with the claims and references listed.

**Opportunity AI** (something that is not possible today)

1. Content that closes a named gap: every item in the plan traces back to the insights and records that justified it.
2. The right depth for the right HCP: a community specialist meeting the data for the first time gets a different piece than an academic expert.
3. A closed loop: next quarter's insights show whether the gap narrowed, so the content plan is measured on knowledge and care, not on volume.

## 9. Suggested swarm shape

```
Insights pillar lead (human) · final judge
   │   Gate 1 · Gate 2 (human decisions)
   └── Lead agent: Gap Lead  [field-insight-synthesis]
         ├── Safety Sentinel  [medical-affairs-foundations (safety scan)]  → Simulated safety escalation list
         ├── Gap Analyst  [insight-generation + evidence-gap-analysis]  → Gap table
         ├── Segmenter  [spreadsheet-analysis + data-connection]  → Persona × stage matrix
         ├── Content Curator  [scientific-communication-strategy + medical-content-operations]  → Draft HCP content plan
         └── MLR Prep  [mlr-review-readiness]  → MLR readiness pack
   Independent checker → reports to the human: deliverable-quality-review (reports to the human, not the lead)
```

| Worker | Skill(s) | Does | Hands off |
|---|---|---|---|
| **Lead: Gap Lead** | [`field-insight-synthesis`](https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills/blob/HEAD/skills/field-insight-synthesis/SKILL.md) | Plans, gives each worker its context packet, assembles, stops at the gates | Plan and final draft |
| Safety Sentinel | `medical-affairs-foundations (safety scan)` | Reads every record first; lists possible AEs, PQCs and off-label mentions verbatim and stops for routing | Simulated safety escalation list |
| Gap Analyst | `insight-generation + evidence-gap-analysis` | Turns field insights, enquiries and the needs assessment into care and knowledge gaps with source IDs and confidence | Gap table |
| Segmenter | `spreadsheet-analysis + data-connection` | Groups HCPs by persona and knowledge stage and maps each gap to the cells it affects | Persona × stage matrix |
| Content Curator | `scientific-communication-strategy + medical-content-operations` | Matches each cell to the content library: reuse, adapt or create, with format and channel | Draft HCP content plan |
| MLR Prep | `mlr-review-readiness` | Lists claims, references and fair-balance points for every new or adapted item; flags anything promotional | MLR readiness pack |

**Hand-offs:** Safety list (stop) → gap table → persona × stage matrix → (Gate 1) → content plan → MLR readiness pack → checker → (Gate 2: MLR)

**Gate 1:** After the Segmenter: the insights pillar leads approve the gaps, the persona × stage segments and the safety routing before content is curated. Why a human: what counts as a gap is a judgment; safety routing is regulated.

**Gate 2:** After MLR Prep: MLR reviewers approve each new or adapted item and the medical lead signs off the plan before anything reaches an HCP. Why a human: accountability for what HCPs are told; MLR is regulated.

**Always-on stop (not a gate, a rule):** any possible adverse event, product quality complaint or off-label signal in human-sourced records is listed verbatim and routed by a human before analysis continues.

## 10. Walk-around question bank

Facilitators: no share-out at the end of Day 1, so these questions are the feedback loop. Ask one or two per visit, then leave.

**During ideation (block 3)**

1. Where do care and knowledge gaps come from in your team today: field insights, medical information, needs assessments? Who joins them up?
2. How do you tell a knowledge gap (HCPs do not know) from a care gap (they know but practice differs)? Does the answer change the content?
3. Which HCP personas matter most for this TA, and how would you know what knowledge stage each one is at?
4. How much of your current content is reused, and how do you know which gap a piece was meant to close?

**During the hack (block 4)**

5. Did your swarm raise the seeded safety finding before anything else? Who receives it, and what does the agent stop doing?
6. Show me one gap and the record IDs behind it. Is it a care gap or a knowledge gap, and how confident is the swarm?
7. How did the swarm assign a knowledge stage to an HCP? What evidence did it use, and what would change the assignment?
8. Pick one persona × stage cell. Why that content, format and channel? Was existing content reused first?
9. Did the swarm catch the promotional learning objective in the needs assessment? Where does the medical vs promotional line sit in your plan?
10. How many hours does one gap-to-content cycle take today, across everyone involved? What does the AI-assisted cycle take, including review and MLR?

## 11. Common pitfalls and how to unblock

| Pitfall | Unblock |
|---|---|
| Insights, not gaps. | Ask: "What do HCPs not know or not do, which HCPs, and how do we know?" Load evidence-gap-analysis. |
| The safety scan is skipped or buried. | Make the Safety Sentinel the first worker and tell the lead to stop until a human acknowledges the list. |
| Personas made up rather than drawn from the data. | Build personas from hcps.csv (setting, channel); show the count in every cell. |
| Everything becomes new content. | Curator checks content_assets.csv first: reuse, adapt, then create. |
| Promotional drift. | Keep objectives about competence and practice, not product use; MLR Prep flags claims and builds a readiness pack per item. |
| Too much data to read in the time. | Start with one TA and two personas; add the CRM tables and the full matrix in the second run. |
| Grok Bot cannot open GitHub. | Upload the starter bundle for your TA from [https://aiinaction.up.railway.app/grokbot](https://aiinaction.up.railway.app/grokbot), or the repository ZIP. |
| The agent asks to connect company systems. | Say no: the workshop uses practice data. It is in every setup prompt. |
| A run is slow or wanders. | Ask for the plan first, then run one sub-agent at a time; cut the scope to one TA, one HCP, one output. |
| The output is generic. | Teach the agent: add 3–5 house rules (what good looks like, what must never appear) and run again. |

## 12. Impact worksheet

Teams supply their own estimates. Count every person involved and **include human review time** in the AI-assisted column.

| Line | Today (baseline) | AI-assisted | Notes |
|---|---|---|---|
| A. Hours per cycle (all people) | ____ h | ____ h | Cycle = one gap-to-content planning cycle |
| B. Cycles per year | ____ | ____ | How often it happens |
| C. Loaded hourly rate | $____ /h | $____ /h | Salary + benefits + overhead; agree one number as a team |
| D. Hours saved per year | | **(A today − A AI) × B = ____ h** | |
| E. Value per year | | **D × C = $____** | Estimate, not a measured result |
| F. Other benefits | | | Speed (days to decision), coverage (% of HCPs, sessions, records), quality (errors caught) |

> **ILLUSTRATIVE ONLY, not data:** 60 h → 12 h per cycle × 4 cycles/year = 192 h saved; × $150/h = $28,800 per year. Replace every number with the team's own estimate.

These numbers go on the Impact slide of the final template (slide 9: formula tiles and a bar chart built from the team's own estimates).

---

*All products, people and results in the practice data are fictional. Outputs are drafts that need qualified human review; this is not a clinical decision, GxP or pharmacovigilance system.*
