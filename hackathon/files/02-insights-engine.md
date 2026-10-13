# 02 · Insights Engine: agenda and facilitator guide

**AI in Action for Medical Affairs** · October 13–14, 2026 · Convene (2nd floor), Two Commerce Square, 2001 Market St, Philadelphia · Host and keynote: Vivek Mukhatyar · Companion site: [aiinaction.up.railway.app](https://aiinaction.up.railway.app)

> **Assumption:** one team per vertical (four teams). The Day 1 afternoon agenda below is an optional suggestion; teams may move faster or slower.

## At a glance

| | |
|---|---|
| Vertical | 02 · Insights Engine: *Trace every care gap to the HCP knowledge or belief gap behind it, then match education to each HCP segment and stage.* |
| Warm-up missions | [`field-insights`](https://aiinaction.up.railway.app/missions/field-insights) · Level 2 Pair · "What should leadership know?"; [`medical-information`](https://aiinaction.up.railway.app/missions/medical-information) · Level 1 Starter · "Handle the enquiry queue" |
| Facilitators | John and Anjali (insights pillar leads; they lead the education route: medical content and medical education) |
| Lead skill for the hack | [`field-insight-synthesis`](https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills/blob/HEAD/skills/field-insight-synthesis/SKILL.md) |
| Practice data | Any TA; synthetic data (fictional Nordvant Biopharma) with seeded safety findings and a promotional objective to catch. |
| Day 2 presentation | This team presents second (02 of 04): teams present in order 01→04 after the final build, about 20 minutes each including a few questions |

## 1. Challenge statement

Field insights, advisory boards and enquiries keep pointing at the same care gaps, but the HCP knowledge or belief gap behind each one is rarely named, so the content plan cannot target it. A community specialist new to the data and an academic expert get the same deck.

## 2. Sharpened problem prompt

> Build an AI workforce that reads field observations, advisory-board notes and enquiries, raises safety findings first, and traces each care gap to the HCP knowledge or belief gap behind it (source IDs, confidence). If evidence exists, it matches approved content to each HCP segment and stage (not aware, aware, learning, applying); if not, it hands the evidence gap off. Humans approve the gaps and sign off the brief. Stretch: a dashboard of Next Best Action by segment and gap closure over time.

Teams can keep this prompt or narrow it to one workflow they know. A good narrowed prompt names the role, the trigger, the deliverable and the decision it serves.

## 3. Day 1 afternoon: suggested agenda (Tue Oct 13)

Context: Day 1 morning: registration, opening keynote and sandbox intro, team creation and function audit; lunch; then **the build afternoon** (four blocks, about 3¼ hours in all); evening cocktail reception. All durations below are approximate.

| About | Block (in order) | Done looks like |
|---|---|---|
| about 30 min | 1 · Set up Grok Bot and load the skills | Every member signed in; the driver's conversation has the skills loaded and has read one practice file; capture log started |
| about 40 min | 2 · Warm-up missions: `field-insights` + `medical-information` | Field insights (safety finding raised first) and an enquiry register exist; the team agreed one shared gap; 3 observations logged |
| about 45 min | 3 · Workflow ideation: the gap-to-content cycle | The gap-to-content cycle mapped; one problem chosen; hours per cycle and number of people involved estimated; ideas marked Efficiency or Opportunity |
| about 80 min (about 1½ hours) | 4 · The hack: build the Insights Engine swarm | Gap list (knowledge or belief → behaviour → care) with source IDs and an evidence route; segment × stage content picks and a brief, stopping at both gates; safety list first; screenshots and timings captured |

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
Load medical-affairs-foundations and these skills: field-insight-synthesis, insight-generation, strategic-analysis, evidence-gap-analysis, meeting-transcription, medical-terminology-mapping, executive-briefing, deliverable-quality-review.
Use the practice data in https://github.com/Open-Medical-Affairs/Data-Sources: synthetic/[oncology-mm | immunology-ad | cardiometabolic-obesity]/ and synthetic/connected/ (the practice CRM). It is fictional (Nordvant Biopharma).
First, only: list the skills you loaded, then show the first 5 rows of field-observations.csv and confirm the file is labelled SYNTHETIC. Do not start a mission yet.
Do not ask me to connect company systems. Do not send, post or change anything outside this conversation.
```

**Done looks like:** all members have a working Grok Bot; the agent lists the loaded skills and shows a file marked SYNTHETIC; the capture log exists.

### Block 2 · Warm-up missions (about 40 min)

- **Pair A:** [`field-insights`](https://aiinaction.up.railway.app/missions/field-insights) · Level 2 Pair · "What should leadership know?". Field observations to insights. Watch for the safety finding first, then ask which HCP knowledge or belief gap sits behind each care gap.
- **Pair B:** [`medical-information`](https://aiinaction.up.railway.app/missions/medical-information) · Level 1 Starter · "Handle the enquiry queue". The enquiry queue is a second gap signal: what HCPs keep asking tells you what they do not yet know.
- Simpler alternative: [`msl-post-call`](https://aiinaction.up.railway.app/missions/msl-post-call) · Level 1 Starter · "Turn the call notes into useful follow-up" (one MSL's notes to CRM draft). Background reading: [Team mission 2](https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills/blob/HEAD/workshop/missions/mission-2.md) ("Find what humans would miss").

| About | What happens (in order) |
|---|---|
| about 5 min | Split into two pairs. Pair A opens /missions/field-insights, Pair B opens /missions/medical-information. Same practice TA. |
| about 20 min | Run both missions in parallel. When the agent raises a safety finding, stop and read it aloud to the team. |
| about 10 min | Push on it: "Which care gaps do you see, and which HCP knowledge or belief gap sits behind each one?" then "Is there evidence for it, or is it an evidence gap?" |
| about 5 min | Swap outputs. Scribe logs: did the safety scan happen first? Were source IDs kept? One gap both pairs found. |

**Done looks like:** at least one finished draft deliverable; the team saw where the agent stopped for a human (safety scan first, human is the final judge); three observations in the capture log ("it was good at…", "it missed…", "we had to decide…").

### Block 3 · Workflow ideation (about 45 min)

| About | What happens (in order) |
|---|---|
| about 15 min | **Map today's workflow** for one real gap-to-content cycle (from field insights to the HCP knowledge or belief gap behind a care gap, to approved content for each HCP segment and stage): steps, who does each, hand-offs, waiting time, hours. Sticky notes or a whiteboard; photograph it for the log. |
| about 10 min | **Spot the AI ideas.** Mark each step **E** (Efficiency AI: do today's work faster) or **O** (Opportunity AI: something not possible today). Use the examples in section 8 to spark ideas. Dot-vote. |
| about 10 min | **Pick one problem.** Write it as: "When [role] needs [outcome], today it takes [time] because [cause]." Fill the baseline column of the impact worksheet (section 13). |
| about 10 min | **Sketch the swarm** on paper: one lead agent, 3–5 sub-agents, the skill each loads, the hand-offs, and two human gates (section 9). Optional: the [Optimizer](https://aiinaction.up.railway.app/optimizer) "Agent swarm / coordinator" task. |

**Done looks like:** a photo of today's workflow; ideas marked E or O; one problem statement; baseline hours and frequency estimated; a swarm sketch with two gates. All in the capture log.

### Block 4 · The hack: build the swarm (about 80 min)

| About | What happens (in order) |
|---|---|
| about 10 min | Write the assignment (starter below, or the [Optimizer](https://aiinaction.up.railway.app/optimizer) in swarm mode). Missing a skill? Use the **Skill creator** on the Optimizer page; read every SKILL.md it produces and approve it before use. |
| about 35 min | **Run 1.** Lead agent plans, sub-agents work (steps 1–2 of the insight plan, section 10); stop at Gate 1 (the top 3–5 gaps, their evidence route and the safety routing) and make the decision as a team. Note the minutes. |
| about 5 min | Optional stretch break. |
| about 20 min | **Run 2.** Fix the weakest hand-off (add a house rule, tighten a context packet), then run steps 3–5 through Gate 2 (the head of medical signs off the brief). Stretch goal: add the Dashboard Builder (section 10). |
| about 10 min | **Capture.** Screenshots of the plan, a hand-off and each gate; timing notes; ask the agent to update the capture log and draft the slide outline from the template. Save everything. |

Reference missions: [`field-insights`](https://aiinaction.up.railway.app/missions/field-insights) · Level 2 Pair · "What should leadership know?" for the insight core, [`connected-planning`](https://aiinaction.up.railway.app/missions/connected-planning) · Level 3 Team · "Work across a practice CRM and content library" for working across the practice CRM and content library, [`launch-plan-swarm`](https://aiinaction.up.railway.app/missions/launch-plan-swarm) · Level 4 Swarm · "Build the whole medical launch plan" for the wave-and-gate pattern.

Assignment starter (paste into Grok Bot, then edit the [brackets]):

```
# Assignment: Insights Engine swarm
You are the Insights Lead, coordinating digital workers for a Medical Affairs team. This is an assignment: plan, delegate, check, hand back drafts.

## Goal: what done looks like
[One sentence: our problem and the deliverable.]

## Context to use
- https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills : read AGENTS.md; load medical-affairs-foundations, field-insight-synthesis and the skills below.
- Practice data (fictional Nordvant Biopharma): https://github.com/Open-Medical-Affairs/Data-Sources synthetic/[TA]/ and synthetic/connected/. Or our own non-confidential data: [describe].
- Our HCP segments: [3-5]. Our content list, one line each: Title | type | stage | proactive or reactive only | status: [paste].

## How to work
1. Show me a short plan and the org chart first. Wait for my OK.
2. Safety first: list possible AEs, product complaints and off-label use verbatim; stop until I acknowledge.
3. Run these sub-agents, each with only the context it needs:
   - Safety Sentinel (medical-affairs-foundations): the step-2 scan. Hands off: Simulated safety escalation list.
   - Coder (medical-terminology-mapping + spreadsheet-analysis): codes observations, keeps source IDs. Hands off: Coded observation table.
   - Transcript Analyst (meeting-transcription): HCP questions and doubts, quoted with speaker. Hands off: Decision log + HCP questions.
   - Insight Analyst (insight-generation + strategic-analysis): name each chain: HCP knowledge/belief gap -> behaviour gap -> patient care gap (suspected if only from field reports), judged by what HCPs know and believe, even if a guideline covers it. Record and source counts; flag weak signals (1-2 records or one source); top 3-5. Hands off: Gap list.
   - Gap Classifier (evidence-gap-analysis): evidence exists (guidelines, publications)? Yes: education. No: evidence gap, hand-off to evidence generation (study or RWD); stop there. Hands off: Evidence route per gap.
   - Persona Mapper (no extra skill): segment (from our list, or unknown) and stage (not aware, aware, learning, applying; if two, the earlier) per education gap, with record counts. Hands off: Segment x stage map.
   - Content Curator (no extra skill): per cell, type, channel and titles only from our list, else "to match"; copy use and status (missing: "check before use"). Off-label: reactive only, via medical information. Never write new content. Hands off: Content picks + content gap list.
   - Briefer (executive-briefing): owner and next action per gap; evidence gaps listed separately. Hands off: Brief with owners and next actions.
4. STOP at Gate 1: After the Gap Classifier: the insights lead approves the top 3-5 gaps, their evidence route and the safety routing before any content is matched. Wait.
5. An independent checker (deliverable-quality-review, reporting to me) reviews the draft; fix what it finds.
6. STOP at Gate 2: After the Briefer: the head of medical signs off the brief, owners and next actions. Wait.
7. Stretch, only after Gate 2: Dashboard Builder (data-visualization-for-medical + medical-affairs-metrics): Next Best Action by HCP segment and/or knowledge-gap closure over time. Label it FICTIONAL. Hands off: Dashboard.
8. Keep a timing note: minutes per step and per gate.

## House rules
- Never invent a citation, number or quote; mark unsupported claims. Keep source IDs; keep public evidence separate.
- Do not send, post, publish or change any external system. Drafts only. Mark every output DRAFT and the data FICTIONAL.
```

**Done looks like:** the swarm ran end to end at least once on practice data; it stopped at Gate 1 and Gate 2 and the team made both decisions; screenshots and minute-level timings are in the capture log; the agent has drafted a slide outline. Stretch: a first dashboard, if time allows.

**End of the afternoon: no formal share-out.** Teams go to the cocktail reception. During the afternoon, facilitators walk around and ask the questions in section 11; near the end of the afternoon they check that every team has saved screenshots and its capture log.

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
| [`field-insights`](https://aiinaction.up.railway.app/missions/field-insights) · Level 2 Pair · "What should leadership know?" | Warm-up (Pair A). Field observations to insights. Watch for the safety finding first, then ask which HCP knowledge or belief gap sits behind each care gap. |
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
| [`insight-generation`](https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills/blob/HEAD/skills/insight-generation/SKILL.md) | Insight Analyst: trace each care gap to the HCP knowledge or belief gap behind it |
| [`evidence-gap-analysis`](https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills/blob/HEAD/skills/evidence-gap-analysis/SKILL.md) | Gap Classifier: is there evidence? Education route or evidence-gap hand-off |
| [`meeting-transcription`](https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills/blob/HEAD/skills/meeting-transcription/SKILL.md) | Transcript Analyst: the questions and doubts HCPs raised at the advisory board |
| [`medical-terminology-mapping`](https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills/blob/HEAD/skills/medical-terminology-mapping/SKILL.md) | Coder: code observations to themes and controlled terms |
| [`strategic-analysis`](https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills/blob/HEAD/skills/strategic-analysis/SKILL.md) | Insight Analyst: signal strength, contradictions and weak signals |
| [`executive-briefing`](https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills/blob/HEAD/skills/executive-briefing/SKILL.md) | Briefer: owners and next actions for each gap |
| [`medical-information-response`](https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills/blob/HEAD/skills/medical-information-response/SKILL.md) | Read the enquiry queue as a gap signal (warm-up) |
| [`medical-education-program`](https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills/blob/HEAD/skills/medical-education-program/SKILL.md) | Education route: objectives about knowledge and practice, never product use |
| [`data-visualization-for-medical`](https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills/blob/HEAD/skills/data-visualization-for-medical/SKILL.md) | Stretch: the Next Best Action and gap-closure dashboard |
| [`medical-affairs-metrics`](https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills/blob/HEAD/skills/medical-affairs-metrics/SKILL.md) | Stretch: measure knowledge-gap closure over time, without causal claims |
| [`spreadsheet-analysis`](https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills/blob/HEAD/skills/spreadsheet-analysis/SKILL.md) | Count records per segment × stage cell |
| [`deliverable-quality-review`](https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills/blob/HEAD/skills/deliverable-quality-review/SKILL.md) | Independent red-team of the draft brief |
| [`medical-affairs-foundations`](https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills/blob/HEAD/skills/medical-affairs-foundations/SKILL.md) | Safety-first rules (loaded with every mission) |

Every skill: [https://aiinaction.up.railway.app/skills](https://aiinaction.up.railway.app/skills) · library: [github.com/Open-Medical-Affairs/Medical-Affairs-Skills](https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills). Workflow not covered? Build a skill with the Skill creator on [https://aiinaction.up.railway.app/optimizer](https://aiinaction.up.railway.app/optimizer) and review it before use.

## 7. Practice data

All practice data are fictional (Nordvant Biopharma; NORVANTIB in multiple myeloma, DERMALYX in atopic dermatitis, ADIPOSYN in obesity; plus a practice CRM). Browse and copy links at [https://aiinaction.up.railway.app/data](https://aiinaction.up.railway.app/data). Teams may instead bring their own **non-confidential** data (no patient data, no confidential company data, no real HCP personal data).

**TA pack files** (pick one TA; links: MM · AD · Obesity), folder: [synthetic/](https://github.com/Open-Medical-Affairs/Data-Sources/tree/main/synthetic)

- `field-observations.csv` ([MM · NORVANTIB](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/oncology-mm/field-observations.csv) · [AD · DERMALYX](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/immunology-ad/field-observations.csv) · [Obesity · ADIPOSYN](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/cardiometabolic-obesity/field-observations.csv))
- `interaction-notes.md` ([MM · NORVANTIB](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/oncology-mm/interaction-notes.md) · [AD · DERMALYX](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/immunology-ad/interaction-notes.md) · [Obesity · ADIPOSYN](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/cardiometabolic-obesity/interaction-notes.md))
- `advisory-board-transcript.md` ([MM · NORVANTIB](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/oncology-mm/advisory-board-transcript.md) · [AD · DERMALYX](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/immunology-ad/advisory-board-transcript.md) · [Obesity · ADIPOSYN](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/cardiometabolic-obesity/advisory-board-transcript.md))
- `guideline-landscape.md` ([MM · NORVANTIB](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/oncology-mm/guideline-landscape.md) · [AD · DERMALYX](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/immunology-ad/guideline-landscape.md) · [Obesity · ADIPOSYN](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/cardiometabolic-obesity/guideline-landscape.md))
- `medical-information-enquiries.csv` ([MM · NORVANTIB](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/oncology-mm/medical-information-enquiries.csv) · [AD · DERMALYX](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/immunology-ad/medical-information-enquiries.csv) · [Obesity · ADIPOSYN](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/cardiometabolic-obesity/medical-information-enquiries.csv))
- `evidence-landscape.md` ([MM · NORVANTIB](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/oncology-mm/evidence-landscape.md) · [AD · DERMALYX](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/immunology-ad/evidence-landscape.md) · [Obesity · ADIPOSYN](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/cardiometabolic-obesity/evidence-landscape.md))
- `medical-education-needs.md` ([MM · NORVANTIB](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/oncology-mm/medical-education-needs.md) · [AD · DERMALYX](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/immunology-ad/medical-education-needs.md) · [Obesity · ADIPOSYN](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/cardiometabolic-obesity/medical-education-needs.md))
- `medical-plan.md` ([MM · NORVANTIB](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/oncology-mm/medical-plan.md) · [AD · DERMALYX](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/immunology-ad/medical-plan.md) · [Obesity · ADIPOSYN](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/cardiometabolic-obesity/medical-plan.md))
- `mlr-review-comments.md` ([MM · NORVANTIB](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/oncology-mm/mlr-review-comments.md) · [AD · DERMALYX](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/immunology-ad/mlr-review-comments.md) · [Obesity · ADIPOSYN](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/cardiometabolic-obesity/mlr-review-comments.md))

**Practice CRM** ([synthetic/connected/](https://github.com/Open-Medical-Affairs/Data-Sources/tree/main/synthetic/connected/))

- [`hcps.csv`](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/connected/hcps.csv)
- [`interactions.csv`](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/connected/interactions.csv)
- [`engagement.csv`](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/connected/engagement.csv)
- [`content_assets.csv`](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/connected/content_assets.csv)
- [`enquiries.csv`](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/connected/enquiries.csv)
- [`data-dictionary.json`](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/connected/data-dictionary.json)

Fictional Nordvant data: hcps.csv for segments, content_assets.csv as the content list, interactions.csv and engagement.csv for the dashboard. Keep source IDs on every gap.

## 8. Example AI ideas

**Efficiency AI** (today's work, faster)

1. Gap tracing: every coded observation traced from HCP knowledge or belief gap to behaviour and care gap, with its source ID and quoted words.
2. First draft of a gap list (gap, chain, evidence route, source IDs, signal strength, segment, stage) ready for the insights lead to edit.
3. Advisory-board transcript to a list of the questions and doubts HCPs raised, each quoted with the speaker, the same afternoon.

**Opportunity AI** (something that is not possible today)

1. Content matched to each HCP: for every gap, a short list of approved content for each segment and stage (not aware to applying).
2. Gaps with no content: a running list of gaps that nothing in the library covers yet, passed to the medical content and education team.
3. One gap, every source: the same gap in MSL notes, advisory boards and congress side by side, plus what the field did not raise.

## 9. Suggested swarm shape

```
Insights lead (human) · final judge
   │   Gate 1 · Gate 2 (human decisions)
   └── Lead agent: Insights Lead  [field-insight-synthesis]
         ├── Safety Sentinel  [medical-affairs-foundations (safety scan)]  → Simulated safety escalation list
         ├── Coder  [medical-terminology-mapping + spreadsheet-analysis]  → Coded observation table
         ├── Transcript Analyst  [meeting-transcription]  → Decision log + HCP questions
         ├── Insight Analyst  [insight-generation + strategic-analysis]  → Gap list
         ├── Gap Classifier  [evidence-gap-analysis]  → Evidence route per gap
         ├── Persona Mapper  [no extra skill; uses the stage rules in section 10]  → Segment × stage map
         ├── Content Curator  [no extra skill; matches only titles on the team's list]  → Content picks + content gaps
         ├── Briefer  [executive-briefing]  → Brief with owners and next actions
         └── Dashboard Builder, optional stretch  [data-visualization-for-medical + medical-affairs-metrics]  → Dashboard (fictional data)
   Independent checker → reports to the human: deliverable-quality-review (reports to the human, not the lead)
```

| Worker | Skill(s) | Does | Hands off |
|---|---|---|---|
| **Lead: Insights Lead** | [`field-insight-synthesis`](https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills/blob/HEAD/skills/field-insight-synthesis/SKILL.md) | Plans, gives each worker its context packet, assembles, stops at the gates | Plan and final draft |
| Safety Sentinel | `medical-affairs-foundations (safety scan)` | Reads every record first; lists possible AEs, PQCs and off-label mentions verbatim and stops for routing | Simulated safety escalation list |
| Coder | `medical-terminology-mapping + spreadsheet-analysis` | De-duplicates contacts, codes observations, keeps source IDs | Coded observation table |
| Transcript Analyst | `meeting-transcription` | Turns the advisory-board transcript into decisions and the questions and doubts HCPs raised, quoted with the speaker | Decision log + HCP questions |
| Insight Analyst | `insight-generation + strategic-analysis` | Traces each care gap to the HCP knowledge or belief gap behind it; signal strength; keeps the top 3–5 | Gap list |
| Gap Classifier | `evidence-gap-analysis` | Asks "is there evidence?" (guidelines, publications): yes = education route; no = evidence gap, handed off | Evidence route per gap |
| Persona Mapper | `no extra skill; uses the stage rules` | Names the segment and the stage (not aware, aware, learning, applying) for each education gap | Segment × stage map |
| Content Curator | `no extra skill; matches only titles on the team's list` | Picks approved content for each cell from the team's list; never writes new content | Content picks + content gaps |
| Briefer | `executive-briefing` | Gives each gap an owner and a next action; lists evidence gaps for hand-off | Brief with owners and next actions |
| Dashboard Builder (stretch) | `data-visualization-for-medical + medical-affairs-metrics` | Optional: Next Best Action by HCP segment and/or knowledge-gap closure over time | Dashboard (fictional data) |

**Hand-offs:** safety list (stop) → coded table + decision log → gap list → evidence route → (Gate 1) → segment × stage map → content picks → brief → checker → (Gate 2) → dashboard (stretch)

**Gate 1:** After the Gap Classifier: the insights lead approves the top 3–5 gaps, their evidence route and the safety routing before any content is matched. Why a human: what counts as a gap is a judgment, and safety routing is a regulated obligation.

**Gate 2:** After the Briefer: the head of medical signs off the brief, the owners and the next actions before it is shared beyond the team. Why a human: accountability for decisions and for what HCPs are told.

**Always-on stop (not a gate, a rule):** any possible adverse event, product quality complaint or off-label signal in human-sourced records is listed verbatim and routed by a human before analysis continues.

## 10. The insight plan: from gap to content

Five steps for the hack (Block 4, about 80 min). Work on the **top 3–5 gaps** only. The agent drafts; the insights lead decides what counts as a gap.

### Step 1 · Gather the insights (Safety Sentinel, Coder, Transcript Analyst)

- **MSL field insights:** `field-observations.csv`, `interaction-notes.md`. **Enquiries:** `medical-information-enquiries.csv`.
- **Advisory boards:** `advisory-board-transcript.md`.
- **Congress:** the team's own non-confidential notes; `evidence-landscape.md` for published work, kept in its own section.
- **Safety scan first.** Possible AEs, product complaints and off-label mentions are listed verbatim and routed before any gap work.

Output: coded table with source IDs.

### Step 2 · Name the gap, then ask: is there evidence? (Insight Analyst, Gap Classifier)

**One chain.** A care gap always stems from an HCP knowledge or belief gap:

**HCP knowledge or belief gap → HCP behaviour gap → patient care gap**

- **Knowledge gap:** does not know or misreads the evidence. **Belief gap:** knows the evidence but doubts it, or doubts it applies to their patients.
- The gap is defined by what HCPs know and believe, **irrespective of guidelines**: even when it is in the guideline, knowledge and perception may not have shifted.
- **Suspected care gap:** every care gap from field reports is "suspected": an MSL's account is not practice data, so name the data that would confirm it.

**The fork: is there evidence (guidelines, publications)?**

- **Yes → education.** Medical content creation and medical education: steps 3–5. This is this vertical's focus, led by John and Anjali.
- **No → evidence gap.** Evidence generation (a study or a real-world data analysis). A hand-off to the evidence-generation team, out of scope for this hack: list it and stop.

**Signal strength, then pick the top 3–5.** Every gap carries its source IDs, the quoted words, the record count, the number of sources (MSLs, advisory board, enquiries, congress) and a confidence. Flag **weak signal** when a gap rests on one or two records or a single source. Weak signals stay in their own section; they are not dropped and not ranked with the rest.

**Gate 1:** the insights lead approves the top 3–5 gaps, their evidence route and the safety routing. Evidence gaps for hand-off are approved here too, so Step 5 can list them.

Example rows (illustrative only, not from the data pack):

| Record (source) | Chain: knowledge or belief → behaviour → care | Evidence? | Signal | Segment · stage · route |
|---|---|---|---|---|
| "Asked how often to check labs after switching therapy." (MSL note) | knowledge gap → labs not checked on schedule → suspected care gap | yes: label, guideline | [n] records, [n] sources | community specialist · applying · education, Step 3 |
| "Most patients here start treatment without the recommended test; I'm not sure the result changes my choice." (MSL note) | belief gap → test skipped → suspected care gap | yes: guideline | 1 record, 1 source · weak signal | community specialist · learning · education, Step 3 |
| "Is there anything on patients over 75? I have nothing to go on." (advisory board) | knowledge gap → no clear practice → suspected care gap | no | [n] records, [n] sources | academic physician · evidence gap, hand-off |

Output of steps 1–2, the gap list, one row per gap: `Gap | Chain (knowledge or belief → behaviour → care) | Suspected? | Evidence? | Route (education / evidence gap) | Source IDs | Records | Sources | Weak signal? | Confidence`

Facilitators: if a team names a care gap, ask which knowledge or belief gap sits behind it and which record shows it. If it is in the guideline but HCPs still do not act, it is an education gap, not an evidence gap. If a care gap has no data that could confirm it, it stays "suspected".

### Step 3 · Map to segment and stage (Persona Mapper)

Before the run, the Scribe pastes the team's content list, one line per piece: `Title | type | stage | proactive or reactive only | status`. Personas are **segments**, not profiles of named HCPs. The team names three to five for its TA, for example: community specialist · academic or specialist-centre physician · primary care or referring physician · nurse practitioner or PA · pharmacist. If the record does not show role or setting, the segment is **unknown**; do not guess.

| Stage | Signs in the record |
|---|---|
| Not aware | Does not mention the evidence or topic at all; describes practice without it; is surprised when the MSL raises it |
| Aware | Has heard of it but has no detail. Asks "what is it?" or "does this apply to my patients?" |
| Learning | Weighing the data: asks about study design, comparisons, subgroups, which patients fit |
| Applying | Has used it or plans to: asks about dosing, monitoring, side effects, switching, hard cases |

**Two-stage rule:** if a record shows signs of two stages, tag the earlier one and note the other. Give a **record count** for every segment × stage cell.

### Step 4 · Pick content for each cell (Content Curator)

Types and channels are examples. Title, use and status come from the team's content list.

| Stage | Content type | Channel |
|---|---|---|
| Not aware | short evidence summary, one-page explainer | MSL visit; congress medical booth |
| Aware | plain-language overview, key data summary | MSL visit; MSL follow-up email |
| Learning | publication summary, data slides, congress highlights | MSL scientific exchange; webinar or peer meeting |
| Applying | practical guide or checklist, case discussion | MSL follow-up; medical information response |

- Use and status are copied from the content list. The Curator does not judge whether a piece is approved; missing status means **check before use**.
- Off-label questions: reactive only, routed to **medical information**; never part of a proactive pick.
- No title on the list fits: write **to match** and add it to the content gap list for the medical content and medical education team. Never write new content.

### Step 5 · Brief and sign-off (Briefer, checker)

Each gap gets an **owner** and a **next action**; evidence gaps for hand-off get their own list. **Gate 2:** the head of medical signs off.

**Outputs at the end of the hack:** gap list with evidence routes · segment × stage map with counts · content picks + content gap list · evidence gaps for hand-off · draft brief · capture log.

**Roles: one extra task each.** Scribe pastes the content list · Navigator questions each gap and its route before Gate 1 · Driver pastes the assignment starter · Presenter tells one gap's story, from knowledge gap to content.

### Stretch goal · the dashboard (Dashboard Builder, optional)

Only after Gate 2. Build a simple dashboard that tracks **Next Best Action by HCP segment**, or **knowledge-gap closure among HCPs over time**, or both; see how far you get.

- **Next Best Action by segment:** for each segment × stage cell, the next piece of content and channel, and how many HCPs it applies to.
- **Gap closure over time:** for each approved gap, the share of HCPs at each stage (not aware → applying) by month, from the dated records in `interactions.csv` and the pre/post scores in `engagement.csv`.
- Synthetic data only, labelled **FICTIONAL (Nordvant Biopharma)** on the dashboard. Show counts, not causal claims.

## 11. Walk-around question bank

Facilitators: no share-out at the end of Day 1, so these questions are the feedback loop. Ask one or two per visit, then leave.

**During ideation (block 3)**

1. Where do care gaps surface in your team today: field insights, advisory boards, medical information? Who traces them back to what HCPs know or believe?
2. Pick one care gap. Which HCP knowledge or belief gap sits behind it, and which HCP behaviour does it drive?
3. When is a gap an education gap, and when is it an evidence gap? Who owns each one today?
4. Which HCP segments matter most for this TA, and how would you tell which stage (not aware to applying) each one is at?

**During the hack (block 4)**

5. Did your swarm raise the seeded safety finding before anything else? Who receives it, and what does the agent stop doing?
6. Show me one gap and the record IDs behind it. Can you read the chain from knowledge or belief gap to behaviour to care gap?
7. This gap is in the guideline, yet HCPs still do not act. Did the Gap Classifier send it to education rather than evidence generation? Why?
8. Pick one segment × stage cell. Why that content and channel? Is every title from your list, with its status copied rather than judged?
9. Did you try the stretch dashboard? What is the Next Best Action for one segment, and what would show a gap closing over time?
10. How many hours does one gap-to-content cycle take today, across everyone involved? What does the AI-assisted cycle take, including review?

## 12. Common pitfalls and how to unblock

| Pitfall | Unblock |
|---|---|
| Care gaps with no cause named. | Ask: "Which HCP knowledge or belief gap sits behind it, and which behaviour does it drive?" Trace the chain first. |
| "It is in the guideline, so it is not a gap." | Gaps are defined by what HCPs know and believe, irrespective of guidelines: guidance alone does not shift perception. |
| Every gap becomes an evidence gap. | The Gap Classifier checks guideline-landscape.md and evidence-landscape.md first; real evidence gaps are a hand-off, out of scope today. |
| The safety scan is skipped or buried. | Make the Safety Sentinel the first worker and tell the lead to stop until a human acknowledges the list. |
| Segments made up rather than drawn from the data. | Build segments from hcps.csv (setting); if role or setting is missing, the segment is unknown. |
| The Curator writes new content or judges approval. | Titles only from the pasted list, status copied; no fit = "to match" on the content gap list. |
| Promotional drift. | Keep objectives about knowledge and practice, not product use; off-label stays reactive, routed to medical information. |
| A run is slow or wanders. | Plan first, one sub-agent at a time; top 3–5 gaps, one TA, two segments; the dashboard only in the second run. |
| Grok Bot cannot open GitHub. | Upload the starter bundle for your TA from [https://aiinaction.up.railway.app/grokbot](https://aiinaction.up.railway.app/grokbot), or the repository ZIP. |
| The output is generic. | Teach the agent: add 3–5 house rules (what good looks like, what must never appear) and run again. |

## 13. Impact worksheet

Teams supply their own estimates. Count every person involved and **include human review time** in the AI-assisted column.

| Line | Today (baseline) | AI-assisted | Notes |
|---|---|---|---|
| A. Hours per cycle (all people) | ____ h | ____ h | Cycle = one gap-to-content cycle (gaps found, routed and matched to content for each segment and stage) |
| B. Cycles per year | ____ | ____ | How often it happens |
| C. Loaded hourly rate | $____ /h | $____ /h | Salary + benefits + overhead; agree one number as a team |
| D. Hours saved per year | | **(A today − A AI) × B = ____ h** | |
| E. Value per year | | **D × C = $____** | Estimate, not a measured result |
| F. Other benefits | | | Speed (days to decision), coverage (% of HCPs, sessions, records), quality (errors caught) |

> **ILLUSTRATIVE ONLY, not data:** 60 h → 12 h per cycle × 4 cycles/year = 192 h saved; × $150/h = $28,800 per year. Replace every number with the team's own estimate.

These numbers go on the Impact slide of the final template (slide 9: formula tiles and a bar chart built from the team's own estimates).

---

*All products, people and results in the practice data are fictional. Outputs are drafts that need qualified human review; this is not a clinical decision, GxP or pharmacovigilance system.*
