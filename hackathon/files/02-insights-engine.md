# 02 · Insights Engine: agenda and facilitator guide

**AI in Action for Medical Affairs** · October 13–14, 2026 · Convene (2nd floor), Two Commerce Square, 2001 Market St, Philadelphia · Host and keynote: Vivek Mukhatyar · Companion site: [aiinaction.up.railway.app](https://aiinaction.up.railway.app)

> **Assumption:** one team per vertical (four teams). The Day 1 afternoon agenda below is an optional suggestion; teams may move faster or slower. Times are ET.

## At a glance

| | |
|---|---|
| Vertical | 02 · Insights Engine: *Turn a quarter of field records into decisions leadership can act on.* |
| Warm-up missions | [`field-insights`](https://aiinaction.up.railway.app/missions/field-insights) · Level 2 Pair · "What should leadership know?"; [`transcript`](https://aiinaction.up.railway.app/missions/transcript) · Level 2 Pair · "Turn a meeting transcript into action" |
| Lead skill for the hack | [`field-insight-synthesis`](https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills/blob/HEAD/skills/field-insight-synthesis/SKILL.md) |
| Practice data | Any TA. Each field-observations.csv contains deliberately seeded adverse events, a product quality complaint and an off-label use: the safety-first stop will trigger. |
| Day 2 presentation | This team presents second (02 of 04): teams present in order 01→04 after the final build, about 20 minutes each including a few questions |

## 1. Challenge statement

Every quarter MSLs log hundreds of field observations and sit in advisory boards. By the time someone codes, themes and writes them up, the quarter is over, and leadership gets theme counts instead of insights it can act on.

## 2. Sharpened problem prompt

> Build an AI workforce that reads a quarter of field records (and a meeting transcript), surfaces possible safety findings first, and turns the rest into the three insights leadership most needs: what is happening, why it matters, what it changes, with source record IDs, a stated confidence, an owner and a next action for each, while keeping disagreements, weak signals and what the field did not say. Humans approve the insights and the brief.

Teams can keep this prompt or narrow it to one workflow they know. A good narrowed prompt names the role, the trigger, the deliverable and the decision it serves.

## 3. Day 1 afternoon: suggested agenda (Tue Oct 13)

Context: Day 1 morning: registration, opening keynote and sandbox intro, team creation and function audit; lunch; then **the build afternoon** (four blocks, about 3¼ hours in all); evening cocktail reception. All durations below are approximate.

| About | Block (in order) | Done looks like |
|---|---|---|
| about 30 min | 1 · Set up Grok Bot and load the skills | Every member signed in; the driver's conversation has the skills loaded and has read one practice file; capture log started |
| about 40 min | 2 · Warm-up missions: `field-insights` + `transcript` | A leadership brief and a decision log exist; the seeded safety finding was raised first and read aloud; 3 observations logged |
| about 45 min | 3 · Workflow ideation: the quarterly field-insight report | The quarterly insight cycle mapped; one problem chosen; hours per quarter and number of people involved estimated; ideas marked Efficiency or Opportunity |
| about 80 min (about 1½ hours) | 4 · The hack: build the Insights Engine swarm | The swarm produced an insight table with source IDs and confidence, then a brief, stopping at both gates; the safety list came first; screenshots and timings captured |

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
Load medical-affairs-foundations and these skills: field-insight-synthesis, insight-generation, meeting-transcription, medical-terminology-mapping, executive-briefing, deliverable-quality-review.
Use the practice data in https://github.com/Open-Medical-Affairs/Data-Sources: synthetic/[oncology-mm | immunology-ad | cardiometabolic-obesity]/ and synthetic/connected/ (the practice CRM). It is fictional (Nordvant Biopharma).
First, only: list the skills you loaded, then show the first 5 rows of field-observations.csv and confirm the file is labelled SYNTHETIC. Do not start a mission yet.
Do not ask me to connect company systems. Do not send, post or change anything outside this conversation.
```

**Done looks like:** all members have a working Grok Bot; the agent lists the loaded skills and shows a file marked SYNTHETIC; the capture log exists.

### Block 2 · Warm-up missions (about 40 min)

- **Pair A:** [`field-insights`](https://aiinaction.up.railway.app/missions/field-insights) · Level 2 Pair · "What should leadership know?". The core insight task. Watch for the safety finding the agent should raise before any analysis.
- **Pair B:** [`transcript`](https://aiinaction.up.railway.app/missions/transcript) · Level 2 Pair · "Turn a meeting transcript into action". Advisory-board transcript to reviewed transcript, correction queue and decision log: a second insight source.
- Simpler alternative: [`msl-post-call`](https://aiinaction.up.railway.app/missions/msl-post-call) · Level 1 Starter · "Turn the call notes into useful follow-up" (one MSL's notes to CRM draft). Background reading: [Team mission 2](https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills/blob/HEAD/workshop/missions/mission-2.md) ("Find what humans would miss").

| About | What happens (in order) |
|---|---|
| about 5 min | Split into two pairs. Pair A opens /missions/field-insights, Pair B opens /missions/transcript. Same practice TA. |
| about 20 min | Run both missions in parallel. When the agent raises a safety finding, stop and read it aloud to the team. |
| about 10 min | Push on it: "Which three should leadership care about most, and why those three?" then "What would change your mind about the first one?" |
| about 5 min | Swap outputs. Scribe logs: did the safety scan happen first? Were source IDs kept? One surprise. |

**Done looks like:** at least one finished draft deliverable; the team saw where the agent stopped for a human (safety scan first, human is the final judge); three observations in the capture log ("it was good at…", "it missed…", "we had to decide…").

### Block 3 · Workflow ideation (about 45 min)

| About | What happens (in order) |
|---|---|
| about 15 min | **Map today's workflow** for one real quarterly field-insight report (from MSL notes to the leadership readout): steps, who does each, hand-offs, waiting time, hours. Sticky notes or a whiteboard; photograph it for the log. |
| about 10 min | **Spot the AI ideas.** Mark each step **E** (Efficiency AI: do today's work faster) or **O** (Opportunity AI: something not possible today). Use the examples in section 8 to spark ideas. Dot-vote. |
| about 10 min | **Pick one problem.** Write it as: "When [role] needs [outcome], today it takes [time] because [cause]." Fill the baseline column of the impact worksheet (section 12). |
| about 10 min | **Sketch the swarm** on paper: one lead agent, 3–5 sub-agents, the skill each loads, the hand-offs, and two human gates (section 9). Optional: the [Optimizer](https://aiinaction.up.railway.app/optimizer) "Agent swarm / coordinator" task. |

**Done looks like:** a photo of today's workflow; ideas marked E or O; one problem statement; baseline hours and frequency estimated; a swarm sketch with two gates. All in the capture log.

### Block 4 · The hack: build the swarm (about 80 min)

| About | What happens (in order) |
|---|---|
| about 10 min | Write the assignment (starter below, or the [Optimizer](https://aiinaction.up.railway.app/optimizer) in swarm mode). Missing a skill? Use the **Skill creator** on the Optimizer page; read every SKILL.md it produces and approve it before use. |
| about 35 min | **Run 1.** Lead agent plans, sub-agents work; stop at Gate 1 (the top three insights and the safety routing) and make the decision as a team. Note the minutes. |
| about 5 min | Optional stretch break. |
| about 20 min | **Run 2.** Fix the weakest hand-off (add a house rule, tighten a context packet), then run through Gate 2 (the head of medical signs off the brief). Optional stress test with a change card. |
| about 10 min | **Capture.** Screenshots of the plan, a hand-off and each gate; timing notes; ask the agent to update the capture log and draft the slide outline from the template. Save everything. |

Reference missions: [`field-insights`](https://aiinaction.up.railway.app/missions/field-insights) · Level 2 Pair · "What should leadership know?" as the core, [`connected-planning`](https://aiinaction.up.railway.app/missions/connected-planning) · Level 3 Team · "Work across a practice CRM and content library" for working across the practice CRM, [`launch-plan-swarm`](https://aiinaction.up.railway.app/missions/launch-plan-swarm) · Level 4 Swarm · "Build the whole medical launch plan" for the wave-and-gate pattern.

Assignment starter (paste into Grok Bot, then edit the [brackets]):

```
# Assignment: Insights Engine swarm
You are the Insights Lead, a lead agent coordinating a small team of digital workers for a Medical Affairs team. This is an assignment, not a question: plan, delegate, check and hand back finished drafts.

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
   - Coder (skills: medical-terminology-mapping + spreadsheet-analysis): De-duplicates contacts, codes observations, keeps source IDs. Hands off: Coded observation table.
   - Transcript Analyst (skills: meeting-transcription): Turns the advisory-board transcript into decisions and quotes with speakers. Hands off: Decision log.
   - Insight Analyst (skills: insight-generation + strategic-analysis): Finds the top insights, contradictions and weak signals; states confidence. Hands off: Insight table.
   - Briefer (skills: executive-briefing): Writes the two-page brief with owners and next actions. Hands off: Leadership brief.
4. STOP at Gate 1: After the Insight Analyst: the insights lead approves the top three insights, their confidence and the safety routing before the brief is written. Show me the evidence pack and wait.
5. Continue, then have an independent checker (deliverable-quality-review (reports to the human, not the lead)) review the draft. Fix what it finds.
6. STOP at Gate 2: After the Briefer: the head of medical signs off the brief, the owners and the actions before it is shared beyond the team. Wait for my decision.
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
| [`field-insights`](https://aiinaction.up.railway.app/missions/field-insights) · Level 2 Pair · "What should leadership know?" | Warm-up (Pair A). The core insight task. Watch for the safety finding the agent should raise before any analysis. |
| [`transcript`](https://aiinaction.up.railway.app/missions/transcript) · Level 2 Pair · "Turn a meeting transcript into action" | Warm-up (Pair B). Advisory-board transcript to reviewed transcript, correction queue and decision log: a second insight source. |
| [`connected-planning`](https://aiinaction.up.railway.app/missions/connected-planning) · Level 3 Team · "Work across a practice CRM and content library" | Hack reference: lead skill plus sub-workers across CRM tables (accounts, interactions, content). |
| [`thirty-day-capstone`](https://aiinaction.up.railway.app/missions/thirty-day-capstone) · Level 3 Team · "Run the next 30 days of Medical Affairs" | Optional stretch: shows how insights feed a 30-day action tracker. |
| [`launch-plan-swarm`](https://aiinaction.up.railway.app/missions/launch-plan-swarm) · Level 4 Swarm · "Build the whole medical launch plan" | The only Level 4 mission: waves of digital workers with human gates between waves. Use it as the model for your swarm. |
| [Team mission 2](https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills/blob/HEAD/workshop/missions/mission-2.md) | Background: the original team mission behind this vertical. |

Levels: 1 Starter = one skill · 2 Pair = lead + one sub-worker · 3 Team = lead + two or more sub-workers · 4 Swarm = waves with human gates. All missions: [https://aiinaction.up.railway.app/missions](https://aiinaction.up.railway.app/missions). Ready prompts: [https://aiinaction.up.railway.app/prompts](https://aiinaction.up.railway.app/prompts).

## 6. Recommended skills

| Skill (Medical-Affairs-Skills) | Use it for |
|---|---|
| [`field-insight-synthesis`](https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills/blob/HEAD/skills/field-insight-synthesis/SKILL.md) | Lead: field observations to insights leadership can act on |
| [`insight-generation`](https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills/blob/HEAD/skills/insight-generation/SKILL.md) | Observation vs insight: what changes a decision |
| [`strategic-analysis`](https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills/blob/HEAD/skills/strategic-analysis/SKILL.md) | So-what and implications |
| [`meeting-transcription`](https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills/blob/HEAD/skills/meeting-transcription/SKILL.md) | Transcripts to reviewable meeting material |
| [`medical-terminology-mapping`](https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills/blob/HEAD/skills/medical-terminology-mapping/SKILL.md) | Free text to controlled vocabulary (coding) |
| [`spreadsheet-analysis`](https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills/blob/HEAD/skills/spreadsheet-analysis/SKILL.md) | CSV analysis and tables |
| [`data-connection`](https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills/blob/HEAD/skills/data-connection/SKILL.md) | Work across the practice CRM tables |
| [`executive-briefing`](https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills/blob/HEAD/skills/executive-briefing/SKILL.md) | Two-page leadership brief |
| [`interactive-html-report`](https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills/blob/HEAD/skills/interactive-html-report/SKILL.md) | Optional insight dashboard |
| [`medical-affairs-metrics`](https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills/blob/HEAD/skills/medical-affairs-metrics/SKILL.md) | Measure whether insights changed anything |
| [`deliverable-quality-review`](https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills/blob/HEAD/skills/deliverable-quality-review/SKILL.md) | Independent red-team of the draft |
| [`medical-affairs-foundations`](https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills/blob/HEAD/skills/medical-affairs-foundations/SKILL.md) | Safety-first rules (loaded with every mission) |

Every skill: [https://aiinaction.up.railway.app/skills](https://aiinaction.up.railway.app/skills) · library: [github.com/Open-Medical-Affairs/Medical-Affairs-Skills](https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills). Workflow not covered? Build a skill with the Skill creator on [https://aiinaction.up.railway.app/optimizer](https://aiinaction.up.railway.app/optimizer) and review it before use.

## 7. Practice data

All practice data are fictional (Nordvant Biopharma; NORVANTIB in multiple myeloma, DERMALYX in atopic dermatitis, ADIPOSYN in obesity; plus a practice CRM). Browse and copy links at [https://aiinaction.up.railway.app/data](https://aiinaction.up.railway.app/data). Teams may instead bring their own **non-confidential** data (no patient data, no confidential company data, no real HCP personal data).

**TA pack files** (pick one TA; links: MM · AD · Obesity), folder: [synthetic/](https://github.com/Open-Medical-Affairs/Data-Sources/tree/main/synthetic)

- `field-observations.csv` ([MM · NORVANTIB](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/oncology-mm/field-observations.csv) · [AD · DERMALYX](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/immunology-ad/field-observations.csv) · [Obesity · ADIPOSYN](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/cardiometabolic-obesity/field-observations.csv))
- `advisory-board-transcript.md` ([MM · NORVANTIB](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/oncology-mm/advisory-board-transcript.md) · [AD · DERMALYX](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/immunology-ad/advisory-board-transcript.md) · [Obesity · ADIPOSYN](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/cardiometabolic-obesity/advisory-board-transcript.md))
- `interaction-notes.md` ([MM · NORVANTIB](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/oncology-mm/interaction-notes.md) · [AD · DERMALYX](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/immunology-ad/interaction-notes.md) · [Obesity · ADIPOSYN](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/cardiometabolic-obesity/interaction-notes.md))
- `medical-plan.md` ([MM · NORVANTIB](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/oncology-mm/medical-plan.md) · [AD · DERMALYX](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/immunology-ad/medical-plan.md) · [Obesity · ADIPOSYN](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/cardiometabolic-obesity/medical-plan.md))
- `evidence-landscape.md` ([MM · NORVANTIB](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/oncology-mm/evidence-landscape.md) · [AD · DERMALYX](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/immunology-ad/evidence-landscape.md) · [Obesity · ADIPOSYN](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/cardiometabolic-obesity/evidence-landscape.md))
- `product-profile.md` ([MM · NORVANTIB](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/oncology-mm/product-profile.md) · [AD · DERMALYX](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/immunology-ad/product-profile.md) · [Obesity · ADIPOSYN](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/cardiometabolic-obesity/product-profile.md))
- `terminology-coding-queue.csv` ([MM · NORVANTIB](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/oncology-mm/terminology-coding-queue.csv) · [AD · DERMALYX](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/immunology-ad/terminology-coding-queue.csv) · [Obesity · ADIPOSYN](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/cardiometabolic-obesity/terminology-coding-queue.csv))
- `medical-impact-metrics.csv` ([MM · NORVANTIB](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/oncology-mm/medical-impact-metrics.csv) · [AD · DERMALYX](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/immunology-ad/medical-impact-metrics.csv) · [Obesity · ADIPOSYN](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/cardiometabolic-obesity/medical-impact-metrics.csv))

**Practice CRM** ([synthetic/connected/](https://github.com/Open-Medical-Affairs/Data-Sources/tree/main/synthetic/connected/))

- [`interactions.csv`](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/connected/interactions.csv)
- [`hcps.csv`](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/connected/hcps.csv)
- [`accounts.csv`](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/connected/accounts.csv)
- [`engagement.csv`](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/connected/engagement.csv)
- [`data-dictionary.json`](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/connected/data-dictionary.json)

The CRM interactions table links every row back to its source file and record ID (e.g. field-observations.csv, OBS-001): ask the swarm to keep those IDs in every insight.

## 8. Example AI ideas

**Efficiency AI** (today's work, faster)

1. Auto-coding: every observation coded to themes and controlled terms, de-duplicated, with source IDs, in minutes instead of days.
2. First draft of the quarterly insight report (insight, evidence, confidence, owner, action) ready for the insights lead to edit.
3. Advisory-board transcript to a decision and follow-up log the same afternoon.

**Opportunity AI** (something that is not possible today)

1. A weekly insight pulse instead of a quarterly report: leadership hears about a shift while it can still act.
2. Plan-assumption watch: link every insight to the medical plan objective it supports or contradicts, and flag the assumptions the field is challenging.
3. Weak-signal and silence detection across all three TAs: the things only one or two MSLs mentioned, and the topics the field conspicuously did not raise.

## 9. Suggested swarm shape

```
Insights lead (human) · final judge
   │   Gate 1 · Gate 2 (human decisions)
   └── Lead agent: Insights Lead  [field-insight-synthesis]
         ├── Safety Sentinel  [medical-affairs-foundations (safety scan)]  → Simulated safety escalation list
         ├── Coder  [medical-terminology-mapping + spreadsheet-analysis]  → Coded observation table
         ├── Transcript Analyst  [meeting-transcription]  → Decision log
         ├── Insight Analyst  [insight-generation + strategic-analysis]  → Insight table
         └── Briefer  [executive-briefing]  → Leadership brief
   Independent checker → reports to the human: deliverable-quality-review (reports to the human, not the lead)
```

| Worker | Skill(s) | Does | Hands off |
|---|---|---|---|
| **Lead: Insights Lead** | [`field-insight-synthesis`](https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills/blob/HEAD/skills/field-insight-synthesis/SKILL.md) | Plans, gives each worker its context packet, assembles, stops at the gates | Plan and final draft |
| Safety Sentinel | `medical-affairs-foundations (safety scan)` | Reads every record first; lists possible AEs, PQCs and off-label mentions verbatim and stops for routing | Simulated safety escalation list |
| Coder | `medical-terminology-mapping + spreadsheet-analysis` | De-duplicates contacts, codes observations, keeps source IDs | Coded observation table |
| Transcript Analyst | `meeting-transcription` | Turns the advisory-board transcript into decisions and quotes with speakers | Decision log |
| Insight Analyst | `insight-generation + strategic-analysis` | Finds the top insights, contradictions and weak signals; states confidence | Insight table |
| Briefer | `executive-briefing` | Writes the two-page brief with owners and next actions | Leadership brief |

**Hand-offs:** Safety list (stop) → coded table + decision log → insight table → (Gate 1) → brief → checker → (Gate 2)

**Gate 1:** After the Insight Analyst: the insights lead approves the top three insights, their confidence and the safety routing before the brief is written. Why a human: what counts as an insight is a judgment, and safety routing is a regulated obligation.

**Gate 2:** After the Briefer: the head of medical signs off the brief, the owners and the actions before it is shared beyond the team. Why a human: accountability for decisions and for what leadership is told.

**Always-on stop (not a gate, a rule):** any possible adverse event, product quality complaint or off-label signal in human-sourced records is listed verbatim and routed by a human before analysis continues.

## 10. Walk-around question bank

Facilitators: no share-out at the end of Day 1, so these questions are the feedback loop. Ask one or two per visit, then leave.

**During ideation (block 3)**

1. What is the difference between an observation and an insight in your team today? Who decides?
2. How long after the quarter ends does leadership see the insights today? What decision is late as a result?
3. Which data would you need from the CRM that the field notes do not have?
4. What would leadership do differently with a weekly pulse instead of a quarterly report?

**During the hack (block 4)**

5. Did your swarm raise the seeded safety finding before anything else? Who receives it, and what does the agent stop doing?
6. Show me one insight and the record IDs behind it. How many records support it?
7. How does the swarm state confidence, and what would lower it?
8. Where do disagreements between MSLs end up? Did any get smoothed over?
9. Where is Gate 1, and what exactly does the insights lead see there?
10. How many hours does one quarterly cycle take today, across everyone involved? What does the AI-assisted cycle take, including review?

## 11. Common pitfalls and how to unblock

| Pitfall | Unblock |
|---|---|
| Themes with counts, not insights. | Ask: "For each, what is happening, why it matters, what it changes and who should act?" Load insight-generation. |
| The safety scan is skipped or buried. | Make the Safety Sentinel the first worker and tell the lead to stop until a human acknowledges the list. |
| Over-confident insights from one or two records. | Require a confidence level and the record count for every insight; weak signals go in their own section. |
| Source IDs disappear in the brief. | Tell the Briefer to keep IDs in an appendix table; the checker fails any insight without them. |
| Public literature mixed into fictional data. | Keep public evidence in a separate, labelled section, or leave it out. |
| Too much data to read in the time. | Start with one TA and one quarter; add the CRM tables in the second run. |
| Grok Bot cannot open GitHub. | Upload the starter bundle for your TA from [https://aiinaction.up.railway.app/grokbot](https://aiinaction.up.railway.app/grokbot), or the repository ZIP. |
| The agent asks to connect company systems. | Say no: the workshop uses practice data. It is in every setup prompt. |
| A run is slow or wanders. | Ask for the plan first, then run one sub-agent at a time; cut the scope to one TA, one HCP, one output. |
| The output is generic. | Teach the agent: add 3–5 house rules (what good looks like, what must never appear) and run again. |

## 12. Impact worksheet

Teams supply their own estimates. Count every person involved and **include human review time** in the AI-assisted column.

| Line | Today (baseline) | AI-assisted | Notes |
|---|---|---|---|
| A. Hours per cycle (all people) | ____ h | ____ h | Cycle = one quarterly field-insight report |
| B. Cycles per year | ____ | ____ | How often it happens |
| C. Loaded hourly rate | $____ /h | $____ /h | Salary + benefits + overhead; agree one number as a team |
| D. Hours saved per year | | **(A today − A AI) × B = ____ h** | |
| E. Value per year | | **D × C = $____** | Estimate, not a measured result |
| F. Other benefits | | | Speed (days to decision), coverage (% of HCPs, sessions, records), quality (errors caught) |

> **ILLUSTRATIVE ONLY, not data:** 40 h → 8 h per cycle × 4 cycles/year = 128 h saved; × $150/h = $19,200 per year. Replace every number with the team's own estimate.

These numbers go on the Impact slide of the final template (slide 9: formula tiles and a bar chart built from the team's own estimates).

---

*All products, people and results in the practice data are fictional. Outputs are drafts that need qualified human review; this is not a clinical decision, GxP or pharmacovigilance system.*
