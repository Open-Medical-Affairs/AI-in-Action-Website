# 01 · Publications Brain: agenda and facilitator guide

**AI in Action for Medical Affairs** · October 13–14, 2026 · Convene (2nd floor), Two Commerce Square, 2001 Market St, Philadelphia · Host and keynote: Vivek Mukhatyar · Companion site: [aiinaction.up.railway.app](https://aiinaction.up.railway.app)

> **Assumption:** one team per vertical (four teams). The Day 1 afternoon agenda below is an optional suggestion; teams may move faster or slower. Times are ET.

## At a glance

| | |
|---|---|
| Vertical | 01 · Publications Brain: *What to publish, what to stop, and keeping every output consistent.* |
| Warm-up missions | [`medical-information`](https://aiinaction.up.railway.app/missions/medical-information) · Level 1 Starter · "Handle the enquiry queue"; [`patient-partnership`](https://aiinaction.up.railway.app/missions/patient-partnership) · Level 2 Pair · "Bring patient priorities into the plan" |
| Lead skill for the hack | [`scientific-communication-strategy`](https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills/blob/HEAD/skills/scientific-communication-strategy/SKILL.md) |
| Practice data | Oncology (NORVANTIB, multiple myeloma) is recommended because the Source-correction change card is written for it; any of the three works. |
| Day 2 presentation slot | 9:40–10:00 AM (about 20 minutes, including a few questions; teams present 01→04 from 9:40) |

## 1. Challenge statement

Our publication plan is sequenced by when data arrive, not by what clinicians and payers are trying to decide. And every new output (manuscript, congress abstract, poster, plain-language summary) re-states the same results by hand, so numbers and wording drift between them.

## 2. Sharpened problem prompt

> Build an AI workforce for the publications team that (1) works backwards from what each audience must decide and recommends what to publish, what to stop and what to research instead, keeping evidence gaps (nobody has answered the question: research) separate from communication gaps (it has been answered and nobody heard: publish); and (2) keeps every scientific output consistent with one source of truth, logging every discrepancy for the authors to resolve. Humans own authorship, priorities and sign-off.

Teams can keep this prompt or narrow it to one workflow they know. A good narrowed prompt names the role, the trigger, the deliverable and the decision it serves.

## 3. Day 1 afternoon: suggested agenda (Tue Oct 13, 1:45–5:00 PM)

Context: 7:45 registration · 8:30 opening keynote and sandbox intro · 11:15 team creation and function audit · lunch · **1:45 build block** · 5:00 cocktail reception.

| Time | Block | Done looks like |
|---|---|---|
| 1:45–2:15 (30 min) | 1 · Set up Grok Bot and load the skills | Every member signed in; the driver's conversation has the skills loaded and has read one practice file; capture log started |
| 2:15–2:55 (40 min) | 2 · Warm-up missions: `medical-information` + `patient-partnership` | Pair A has an enquiry triage register; Pair B has a lay summary with a list of simplifications; both seen in 2-minute swaps; 3 observations logged |
| 2:55–3:40 (45 min) | 3 · Workflow ideation: the publication cycle | The publication cycle mapped; one problem chosen (strategy or consistency); hours per cycle and outputs per year estimated; ideas marked Efficiency or Opportunity |
| 3:40–5:00 (80 min) | 4 · The hack: build the Publications Brain swarm | The swarm produced a gap table and at least one draft output plus a discrepancy log, stopping at both gates; screenshots and timings captured |

Suggested roles (rotate if you like): **driver** (types into Grok Bot), **navigator** (reads the mission and pushes back), **scribe** (owns the capture log), **timekeeper and presenter**.

### Block 1 · Set up Grok Bot and load the skills (1:45–2:15)

| Time | What happens |
|---|---|
| 1:45–1:50 | Huddle: agree roles and pick one practice therapeutic area (TA). |
| 1:50–2:02 | Everyone opens [https://aiinaction.up.railway.app/grokbot](https://aiinaction.up.railway.app/grokbot): event sign-up link, credits code (both shared at the conference), new conversation. Can't open GitHub? Upload the starter bundle linked on that page. |
| 2:02–2:10 | The driver pastes the setup prompt below. Others follow along on their own laptops. |
| 2:10–2:15 | Smoke test passes (skills listed, a SYNTHETIC file read). The scribe pastes the capture-log instructions ([final-presentation-agent-instructions.md](final-presentation-agent-instructions.md)) into the conversation and starts [capture-log-template.md](capture-log-template.md). |

Setup prompt (paste into Grok Bot; replace the TA):

```
Use https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills
Read AGENTS.md. We are the Publications Brain team at AI in Action for Medical Affairs.
Load medical-affairs-foundations and these skills: scientific-communication-strategy, evidence-gap-analysis, scientific-manuscript, congress-abstract-and-poster, plain-language-summary, citation-integrity, deliverable-quality-review.
Use the practice data in https://github.com/Open-Medical-Affairs/Data-Sources: synthetic/[oncology-mm | immunology-ad | cardiometabolic-obesity]/ and synthetic/connected/ (the practice CRM). It is fictional (Nordvant Biopharma).
First, only: list the skills you loaded, then show the first 5 rows of content_assets.csv and confirm the file is labelled SYNTHETIC. Do not start a mission yet.
Do not ask me to connect company systems. Do not send, post or change anything outside this conversation.
```

**Done looks like:** all members have a working Grok Bot; the agent lists the loaded skills and shows a file marked SYNTHETIC; the capture log exists.

### Block 2 · Warm-up missions (2:15–2:55)

- **Pair A:** [`medical-information`](https://aiinaction.up.railway.app/missions/medical-information) · Level 1 Starter · "Handle the enquiry queue". See what clinicians actually ask (the demand signal for publications) and how the agent ties every answer to the structured evidence table.
- **Pair B:** [`patient-partnership`](https://aiinaction.up.railway.app/missions/patient-partnership) · Level 2 Pair · "Bring patient priorities into the plan". Watch a lead skill hand off to plain-language-summary: the same evidence, rewritten for a lay audience without changing the numbers.
- If the team is fast: run the [`publication`](https://aiinaction.up.railway.app/missions/publication) · Level 3 Team · "Keep every scientific output consistent" mission (the vertical's "good place to start") on one output only, or read [Team mission 4](https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills/blob/HEAD/workshop/missions/mission-4.md) ("What should we be publishing, and what should we stop?").

| Time | What happens |
|---|---|
| 2:15–2:18 | Split into two pairs. Pair A opens /missions/medical-information, Pair B opens /missions/patient-partnership. Pick the same practice TA. Copy the prompt. |
| 2:18–2:40 | Both pairs run their mission in parallel (about 15–20 min each). Let it finish; do not steer. |
| 2:40–2:50 | Push on it: Pair A asks "Which of these questions do our planned publications fail to answer?"; Pair B asks "Show me every number you changed between the source and the lay summary." |
| 2:50–2:55 | Swap: each pair shows the other its output in 2 minutes. Scribe logs three observations in the capture log. |

**Done looks like:** at least one finished draft deliverable; the team saw where the agent stopped for a human (safety scan first, human is the final judge); three observations in the capture log ("it was good at…", "it missed…", "we had to decide…").

### Block 3 · Workflow ideation (2:55–3:40)

| Time | What happens |
|---|---|
| 2:55–3:10 | **Map today's workflow** for one real publication cycle (e.g. one result going from manuscript to congress abstract to plain-language summary): steps, who does each, hand-offs, waiting time, hours. Sticky notes or a whiteboard; photograph it for the log. |
| 3:10–3:22 | **Spot the AI ideas.** Mark each step **E** (Efficiency AI: do today's work faster) or **O** (Opportunity AI: something not possible today). Use the examples in section 8 to spark ideas. Dot-vote. |
| 3:22–3:32 | **Pick one problem.** Write it as: "When [role] needs [outcome], today it takes [time] because [cause]." Fill the baseline column of the impact worksheet (section 12). |
| 3:32–3:40 | **Sketch the swarm** on paper: one lead agent, 3–5 sub-agents, the skill each loads, the hand-offs, and two human gates (section 9). Optional: the [Optimizer](https://aiinaction.up.railway.app/optimizer) "Agent swarm / coordinator" task. |

**Done looks like:** a photo of today's workflow; ideas marked E or O; one problem statement; baseline hours and frequency estimated; a swarm sketch with two gates. All in the capture log.

### Block 4 · The hack: build the swarm (3:40–5:00)

| Time | What happens |
|---|---|
| 3:40–3:50 | Write the assignment (starter below, or the [Optimizer](https://aiinaction.up.railway.app/optimizer) in swarm mode). Missing a skill? Use the **Skill creator** on the Optimizer page; read every SKILL.md it produces and approve it before use. |
| 3:50–4:25 | **Run 1.** Lead agent plans, sub-agents work; stop at Gate 1 (the publish / stop / research list) and make the decision as a team. Note the minutes. |
| 4:25–4:30 | Optional stretch break. |
| 4:30–4:50 | **Run 2.** Fix the weakest hand-off (add a house rule, tighten a context packet), then run through Gate 2 (authors resolve the discrepancy log). Optional stress test with a change card. |
| 4:50–5:00 | **Capture.** Screenshots of the plan, a hand-off and each gate; timing notes; ask the agent to update the capture log and draft the slide outline from the template. Save everything. |

Reference missions: [`publication`](https://aiinaction.up.railway.app/missions/publication) · Level 3 Team · "Keep every scientific output consistent" for the consistency side, [Team mission 4](https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills/blob/HEAD/workshop/missions/mission-4.md) for the strategy side; [`launch-plan-swarm`](https://aiinaction.up.railway.app/missions/launch-plan-swarm) · Level 4 Swarm · "Build the whole medical launch plan" shows how a Level 4 swarm runs in waves with gates.

Assignment starter (paste into Grok Bot, then edit the [brackets]):

```
# Assignment: Publications Brain swarm
You are the Publications Strategist, a lead agent coordinating a small team of digital workers for a Medical Affairs team. This is an assignment, not a question: plan, delegate, check and hand back finished drafts.

## Goal: what done looks like
[One sentence: the problem we picked in ideation, and the deliverable that solves it.]

## Context to use
- https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills : read AGENTS.md, load medical-affairs-foundations, your lead skill scientific-communication-strategy, and the skills named below.
- Practice data (fictional): https://github.com/Open-Medical-Affairs/Data-Sources synthetic/[TA]/ and synthetic/connected/. Or our own non-confidential data: [describe].

## How to work
1. Show me a short plan and the org chart of workers first. Wait for my OK.
2. Scan human-sourced records for possible safety findings (adverse events, product complaints, off-label use) before anything else. List them verbatim and stop until I acknowledge.
3. Run these sub-agents, each with only the context it needs:
   - Demand Reader (skills: field-insight-synthesis): Reads field observations and MI enquiries; lists the questions each audience is trying to answer. Hands off: Audience-question list.
   - Evidence Mapper (skills: evidence-synthesis + evidence-gap-analysis): Maps each question to the evidence; labels evidence gap vs communication gap. Hands off: Gap table with sources.
   - Output Drafter (skills: scientific-manuscript / congress-abstract-and-poster / plain-language-summary): Drafts the chosen output(s) from the approved source. Hands off: Draft outputs.
   - Consistency Auditor (skills: citation-integrity + data-visualization-for-medical): Checks every number, figure and claim against the evidence table. Hands off: Discrepancy log.
4. STOP at Gate 1: After the Evidence Mapper: the publications lead (with the steering committee) approves the publish / stop / research list before any drafting starts. Show me the evidence pack and wait.
5. Continue, then have an independent checker (deliverable-quality-review (reports to the human, not the lead); add mlr-review-readiness for a pre-MLR pass) review the draft. Fix what it finds.
6. STOP at Gate 2: After the Consistency Auditor: authors and the medical reviewer resolve the discrepancy log and approve the drafts before anything goes to authors, MLR or a journal. Wait for my decision.
7. Keep a timing note: minutes per step, and minutes of human review at each gate.

## House rules
- Never invent a citation, number, quote or meeting fact. Unsupported claims are marked and left for a human.
- Keep source IDs on every claim. Keep public evidence separate from fictional practice data.
- Do not send, post, publish or change any external system. Drafts only. Mark every output DRAFT and the data FICTIONAL.
```

**Done looks like:** the swarm ran end to end at least once on practice data; it stopped at Gate 1 and Gate 2 and the team made both decisions; screenshots and minute-level timings are in the capture log; the agent has drafted a slide outline.

**5:00 PM: no formal share-out.** Teams go to the cocktail reception. During the afternoon, facilitators walk around and ask the questions in section 10; from 4:45 they check that every team has saved screenshots and its capture log.

## 4. Day 2: final build and presentation (Wed Oct 14, 9:00–11:00 AM)

Context: 8:00 breakfast · **9:00 hackathon + demo presentations** · 11:00 interactive demo by WPP · 11:50 closing panel · 1:30 end.

| Time | What happens |
|---|---|
| 9:00–9:05 | Re-open yesterday's conversation. The agent re-reads the capture log. |
| 9:05–9:25 | One last build fix at most. The agent fills the [final presentation template](template/AI-in-Action-Final-Presentation-Template.pptx) using the [agent instructions](final-presentation-agent-instructions.md). |
| 9:25–9:32 | Team review: no [brackets] left, impact numbers are the team's own, practice data marked fictional, demo screenshots in place. |
| 9:32–9:38 | Rehearse the demo and the first two slides. Hand the deck to the AV desk / presentation laptop. |
| 9:38–9:40 | MC opens the session. |
| **9:40–10:00 AM** | **Publications Brain presents** (about 20 minutes, give or take, including a short live demo and a few questions). |

> **Timing.** Teams present 01→04 from 9:40, about 20 minutes each including a few questions, before the 11:00 WPP demo. The morning build is short, so keep all decks on one laptop and treat the Day 1 4:50–5:00 capture as essential. Team 01 presents first and has the least Day 2 time, so its deck draft should be done on Day 1.

## 5. Recommended missions

| Mission (link) | Why |
|---|---|
| [`medical-information`](https://aiinaction.up.railway.app/missions/medical-information) · Level 1 Starter · "Handle the enquiry queue" | Warm-up (Pair A). See what clinicians actually ask (the demand signal for publications) and how the agent ties every answer to the structured evidence table. |
| [`patient-partnership`](https://aiinaction.up.railway.app/missions/patient-partnership) · Level 2 Pair · "Bring patient priorities into the plan" | Warm-up (Pair B). Watch a lead skill hand off to plain-language-summary: the same evidence, rewritten for a lay audience without changing the numbers. |
| [`publication`](https://aiinaction.up.railway.app/missions/publication) · Level 3 Team · "Keep every scientific output consistent" | Hack reference: the four-output consistency task (manuscript, abstract and figure, lay summary, discrepancy log). |
| [`evidence-investment`](https://aiinaction.up.railway.app/missions/evidence-investment) · Level 3 Team · "Choose what to fund" | Optional: if the team chooses "what to research instead", this mission shows the evidence-plan logic. |
| [`launch-plan-swarm`](https://aiinaction.up.railway.app/missions/launch-plan-swarm) · Level 4 Swarm · "Build the whole medical launch plan" | The only Level 4 mission: waves of digital workers with human gates between waves. Use it as the model for your swarm. |
| [Team mission 4](https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills/blob/HEAD/workshop/missions/mission-4.md) | Background: the original team mission behind this vertical. |

Levels: 1 Starter = one skill · 2 Pair = lead + one sub-worker · 3 Team = lead + two or more sub-workers · 4 Swarm = waves with human gates. All missions: [https://aiinaction.up.railway.app/missions](https://aiinaction.up.railway.app/missions). Ready prompts: [https://aiinaction.up.railway.app/prompts](https://aiinaction.up.railway.app/prompts).

## 6. Recommended skills

| Skill (Medical-Affairs-Skills) | Use it for |
|---|---|
| [`scientific-communication-strategy`](https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills/blob/HEAD/skills/scientific-communication-strategy/SKILL.md) | Lead: what to publish, for whom, and what to stop |
| [`evidence-gap-analysis`](https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills/blob/HEAD/skills/evidence-gap-analysis/SKILL.md) | Separates evidence gaps from communication gaps |
| [`evidence-synthesis`](https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills/blob/HEAD/skills/evidence-synthesis/SKILL.md) | One defensible narrative from the evidence |
| [`literature-surveillance`](https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills/blob/HEAD/skills/literature-surveillance/SKILL.md) | Repeatable watch on new publications |
| [`pubmed-search`](https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills/blob/HEAD/skills/pubmed-search/SKILL.md) | Real, verifiable literature (public sources only) |
| [`scientific-manuscript`](https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills/blob/HEAD/skills/scientific-manuscript/SKILL.md) | Manuscript drafting and structure |
| [`congress-abstract-and-poster`](https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills/blob/HEAD/skills/congress-abstract-and-poster/SKILL.md) | Abstracts that fit the submission rules |
| [`plain-language-summary`](https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills/blob/HEAD/skills/plain-language-summary/SKILL.md) | Lay summaries |
| [`data-visualization-for-medical`](https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills/blob/HEAD/skills/data-visualization-for-medical/SKILL.md) | Honest figures |
| [`citation-integrity`](https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills/blob/HEAD/skills/citation-integrity/SKILL.md) | Every claim traces to a source |
| [`mlr-review-readiness`](https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills/blob/HEAD/skills/mlr-review-readiness/SKILL.md) | Pre-check before MLR |
| [`deliverable-quality-review`](https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills/blob/HEAD/skills/deliverable-quality-review/SKILL.md) | Independent red-team of the draft |

Every skill: [https://aiinaction.up.railway.app/skills](https://aiinaction.up.railway.app/skills) · library: [github.com/Open-Medical-Affairs/Medical-Affairs-Skills](https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills). Workflow not covered? Build a skill with the Skill creator on [https://aiinaction.up.railway.app/optimizer](https://aiinaction.up.railway.app/optimizer) and review it before use.

## 7. Practice data

All practice data are fictional (Nordvant Biopharma; NORVANTIB in multiple myeloma, DERMALYX in atopic dermatitis, ADIPOSYN in obesity; plus a practice CRM). Browse and copy links at [https://aiinaction.up.railway.app/data](https://aiinaction.up.railway.app/data). Teams may instead bring their own **non-confidential** data (no patient data, no confidential company data, no real HCP personal data).

**TA pack files** (pick one TA; links: MM · AD · Obesity), folder: [synthetic/](https://github.com/Open-Medical-Affairs/Data-Sources/tree/main/synthetic)

- `publication-plan.md` ([MM · NORVANTIB](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/oncology-mm/publication-plan.md) · [AD · DERMALYX](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/immunology-ad/publication-plan.md) · [Obesity · ADIPOSYN](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/cardiometabolic-obesity/publication-plan.md))
- `evidence-landscape.md` ([MM · NORVANTIB](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/oncology-mm/evidence-landscape.md) · [AD · DERMALYX](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/immunology-ad/evidence-landscape.md) · [Obesity · ADIPOSYN](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/cardiometabolic-obesity/evidence-landscape.md))
- `field-observations.csv` ([MM · NORVANTIB](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/oncology-mm/field-observations.csv) · [AD · DERMALYX](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/immunology-ad/field-observations.csv) · [Obesity · ADIPOSYN](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/cardiometabolic-obesity/field-observations.csv))
- `medical-plan.md` ([MM · NORVANTIB](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/oncology-mm/medical-plan.md) · [AD · DERMALYX](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/immunology-ad/medical-plan.md) · [Obesity · ADIPOSYN](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/cardiometabolic-obesity/medical-plan.md))
- `product-profile.md` ([MM · NORVANTIB](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/oncology-mm/product-profile.md) · [AD · DERMALYX](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/immunology-ad/product-profile.md) · [Obesity · ADIPOSYN](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/cardiometabolic-obesity/product-profile.md))
- `manuscript-draft.md` ([MM · NORVANTIB](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/oncology-mm/manuscript-draft.md) · [AD · DERMALYX](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/immunology-ad/manuscript-draft.md) · [Obesity · ADIPOSYN](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/cardiometabolic-obesity/manuscript-draft.md))
- `structured-evidence-table.csv` ([MM · NORVANTIB](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/oncology-mm/structured-evidence-table.csv) · [AD · DERMALYX](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/immunology-ad/structured-evidence-table.csv) · [Obesity · ADIPOSYN](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/cardiometabolic-obesity/structured-evidence-table.csv))
- `patient-level-analysis.csv` ([MM · NORVANTIB](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/oncology-mm/patient-level-analysis.csv) · [AD · DERMALYX](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/immunology-ad/patient-level-analysis.csv) · [Obesity · ADIPOSYN](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/cardiometabolic-obesity/patient-level-analysis.csv))
- `abstract-poster-brief.md` ([MM · NORVANTIB](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/oncology-mm/abstract-poster-brief.md) · [AD · DERMALYX](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/immunology-ad/abstract-poster-brief.md) · [Obesity · ADIPOSYN](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/cardiometabolic-obesity/abstract-poster-brief.md))
- `plain-language-source.md` ([MM · NORVANTIB](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/oncology-mm/plain-language-source.md) · [AD · DERMALYX](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/immunology-ad/plain-language-source.md) · [Obesity · ADIPOSYN](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/cardiometabolic-obesity/plain-language-source.md))
- `guideline-landscape.md` ([MM · NORVANTIB](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/oncology-mm/guideline-landscape.md) · [AD · DERMALYX](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/immunology-ad/guideline-landscape.md) · [Obesity · ADIPOSYN](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/cardiometabolic-obesity/guideline-landscape.md))

**Practice CRM** ([synthetic/connected/](https://github.com/Open-Medical-Affairs/Data-Sources/tree/main/synthetic/connected/))

- [`content_assets.csv`](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/connected/content_assets.csv)
- [`enquiries.csv`](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/connected/enquiries.csv)

Stress test: the [Source correction change card](https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills/blob/HEAD/workshop/change-cards/source-correction-oncology.md) (oncology) corrects a fictional study result: ask the swarm to trace it into every affected draft.

## 8. Example AI ideas

**Efficiency AI** (today's work, faster)

1. Consistency check across outputs: every number and claim in the manuscript, abstract, poster and lay summary is traced to the structured evidence table, with a discrepancy log for authors.
2. Encore and adaptation drafts: turn one approved source into abstracts that meet each congress's word limits and submission rules.
3. Plain-language summary first draft from the approved manuscript, with a readability check and a list of every simplification made.

**Opportunity AI** (something that is not possible today)

1. A publication plan driven by what audiences must decide: map field questions and MI enquiries against the plan to show, every month, where we are silent and where we over-communicate.
2. Correction ripple: when one result changes, find and redline every affected draft, slide and published asset within minutes, instead of discovering it at MLR.
3. A living gap register that routes each gap to "research it" or "publish it", refreshed every month rather than at the annual planning cycle.

## 9. Suggested swarm shape

```
Publications lead (human) · final judge
   │   Gate 1 · Gate 2 (human decisions)
   └── Lead agent: Publications Strategist  [scientific-communication-strategy]
         ├── Demand Reader  [field-insight-synthesis]  → Audience-question list
         ├── Evidence Mapper  [evidence-synthesis + evidence-gap-analysis]  → Gap table with sources
         ├── Output Drafter  [scientific-manuscript / congress-abstract-and-poster / plain-language-summary]  → Draft outputs
         └── Consistency Auditor  [citation-integrity + data-visualization-for-medical]  → Discrepancy log
   Independent checker → reports to the human: deliverable-quality-review (reports to the human, not the lead); add mlr-review-readiness for a pre-MLR pass
```

| Worker | Skill(s) | Does | Hands off |
|---|---|---|---|
| **Lead: Publications Strategist** | [`scientific-communication-strategy`](https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills/blob/HEAD/skills/scientific-communication-strategy/SKILL.md) | Plans, gives each worker its context packet, assembles, stops at the gates | Plan and final draft |
| Demand Reader | `field-insight-synthesis` | Reads field observations and MI enquiries; lists the questions each audience is trying to answer | Audience-question list |
| Evidence Mapper | `evidence-synthesis + evidence-gap-analysis` | Maps each question to the evidence; labels evidence gap vs communication gap | Gap table with sources |
| Output Drafter | `scientific-manuscript / congress-abstract-and-poster / plain-language-summary` | Drafts the chosen output(s) from the approved source | Draft outputs |
| Consistency Auditor | `citation-integrity + data-visualization-for-medical` | Checks every number, figure and claim against the evidence table | Discrepancy log |

**Hand-offs:** Audience questions → gap table → (Gate 1) → drafts → discrepancy log → (Gate 2) → approved drafts

**Gate 1:** After the Evidence Mapper: the publications lead (with the steering committee) approves the publish / stop / research list before any drafting starts. Why a human: publication priorities are a strategic and ethical decision (negative results, balance, timing).

**Gate 2:** After the Consistency Auditor: authors and the medical reviewer resolve the discrepancy log and approve the drafts before anything goes to authors, MLR or a journal. Why a human: authorship and accountability (ICMJE), scientific judgment, no ghost-writing.

**Always-on stop (not a gate, a rule):** any possible adverse event, product quality complaint or off-label signal in human-sourced records is listed verbatim and routed by a human before analysis continues.

## 10. Walk-around question bank

Facilitators: no share-out at the end of Day 1, so these questions are the feedback loop. Ask one or two per visit, then leave.

**During ideation (2:55–3:40)**

1. Who is the audience for this publication, and what decision are they trying to make with it?
2. Is this an evidence gap or a communication gap? How would you prove which one it is?
3. Which step of today's workflow takes longest, and is the delay people or approvals?
4. What are you publishing that nobody asked for? How would the agent know?

**During the hack (3:40–5:00)**

5. Where exactly does a human approve the priority list? What does the agent show them at that moment?
6. Which file is your single source of truth for the numbers? What happens when the agent finds a mismatch?
7. How does your swarm handle a negative or inconvenient result?
8. Show me one claim in the draft and the source row it came from.
9. If the source-correction card landed now, how many drafts would change, and how would you know?
10. What would your hours-per-cycle number be for one manuscript-to-PLS cycle today? Who would sign off that estimate?

## 11. Common pitfalls and how to unblock

| Pitfall | Unblock |
|---|---|
| The agent lists papers in the order data arrive. | Re-ask: "Work backwards from what each audience must decide. Start with the decision, then the evidence." |
| Evidence gaps and communication gaps get mixed up. | Make the Evidence Mapper label every row "evidence gap" or "communication gap" with one line of reasoning. |
| Numbers drift in the lay summary. | Tell the Consistency Auditor to compare every number with structured-evidence-table.csv and list every difference, even rounding. |
| Trying to write a full manuscript in 80 minutes. | Scope to one output plus the discrepancy log. A short, correct draft beats a long, unchecked one. |
| Invented references. | Load citation-integrity; any claim without a source is marked "unsupported" and left for the author. |
| Authorship or ghost-writing worries in the room. | Good: make it Gate 2. The agent drafts; named authors decide, edit and own. |
| Grok Bot cannot open GitHub. | Upload the starter bundle for your TA from [https://aiinaction.up.railway.app/grokbot](https://aiinaction.up.railway.app/grokbot), or the repository ZIP. |
| The agent asks to connect company systems. | Say no: the workshop uses practice data. It is in every setup prompt. |
| A run is slow or wanders. | Ask for the plan first, then run one sub-agent at a time; cut the scope to one TA, one HCP, one output. |
| The output is generic. | Teach the agent: add 3–5 house rules (what good looks like, what must never appear) and run again. |

## 12. Impact worksheet

Teams supply their own estimates. Count every person involved and **include human review time** in the AI-assisted column.

| Line | Today (baseline) | AI-assisted | Notes |
|---|---|---|---|
| A. Hours per cycle (all people) | ____ h | ____ h | Cycle = one manuscript-to-abstract-to-lay-summary consistency cycle |
| B. Cycles per year | ____ | ____ | How often it happens |
| C. Loaded hourly rate | $____ /h | $____ /h | Salary + benefits + overhead; agree one number as a team |
| D. Hours saved per year | | **(A today − A AI) × B = ____ h** | |
| E. Value per year | | **D × C = $____** | Estimate, not a measured result |
| F. Other benefits | | | Speed (days to decision), coverage (% of HCPs, sessions, records), quality (errors caught) |

> **ILLUSTRATIVE ONLY, not data:** 24 h → 6 h per cycle × 10 cycles/year = 180 h saved; × $150/h = $27,000 per year. Replace every number with the team's own estimate.

These numbers go on slide 8 of the final template (formula tiles and bar chart).

---

*All products, people and results in the practice data are fictional. Outputs are drafts that need qualified human review; this is not a clinical decision, GxP or pharmacovigilance system.*
