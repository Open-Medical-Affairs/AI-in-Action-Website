# 04 · Field Intelligence Engine: agenda and facilitator guide

**AI in Action for Medical Affairs** · October 13–14, 2026 · Convene (2nd floor), Two Commerce Square, 2001 Market St, Philadelphia · Host and keynote: Vivek Mukhatyar · Companion site: [aiinaction.up.railway.app](https://aiinaction.up.railway.app)

> **Assumption:** one team per vertical (four teams). The Day 1 afternoon agenda below is an optional suggestion; teams may move faster or slower. Times are ET.

## At a glance

| | |
|---|---|
| Vertical | 04 · Field Intelligence Engine: *Walk into every HCP conversation prepared, and close the loop after.* |
| Warm-up missions | [`msl-pre-call`](https://aiinaction.up.railway.app/missions/msl-pre-call) · Level 1 Starter · "Prepare the MSL pre-call brief"; [`msl-post-call`](https://aiinaction.up.railway.app/missions/msl-post-call) · Level 1 Starter · "Turn the call notes into useful follow-up" |
| Lead skill for the hack | [`field-medical-planning`](https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills/blob/HEAD/skills/field-medical-planning/SKILL.md) |
| Practice data | Any TA. The practice CRM (connected) spans all three TAs; pick HCPs from one TA to keep it focused. |
| Day 2 presentation slot | 10:40–11:00 AM (about 20 minutes, including a few questions; teams present 01→04 from 9:40) |

## 1. Challenge statement

MSLs spend hours before each scientific exchange stitching together CRM history, open enquiries and evidence, and hours afterwards writing CRM notes and follow-ups. Preparation quality varies, and commitments made in the meeting slip.

## 2. Sharpened problem prompt

> Build an AI workforce that, for any HCP on an MSL's list, prepares a one-page pre-call brief from verified professional context, prior interactions, open questions and permitted materials; and after the call turns the notes into a factual CRM draft, a commitment register and a follow-up draft, routing any safety finding or unsolicited off-label request to the right human. The MSL approves everything; nothing is sent or logged by the agent.

Teams can keep this prompt or narrow it to one workflow they know. A good narrowed prompt names the role, the trigger, the deliverable and the decision it serves.

## 3. Day 1 afternoon: suggested agenda (Tue Oct 13, 1:45–5:00 PM)

Context: 7:45 registration · 8:30 opening keynote and sandbox intro · 11:15 team creation and function audit · lunch · **1:45 build block** · 5:00 cocktail reception.

| Time | Block | Done looks like |
|---|---|---|
| 1:45–2:15 (30 min) | 1 · Set up Grok Bot and load the skills | Every member signed in; the driver's conversation has the skills loaded and has read one practice file; capture log started |
| 2:15–2:55 (40 min) | 2 · Warm-up missions: `msl-pre-call` + `msl-post-call` | Pair A has a pre-call brief; Pair B has a CRM draft and commitment register; the team saw how one could feed the other; 3 observations logged |
| 2:55–3:40 (45 min) | 3 · Workflow ideation: the HCP engagement | One HCP engagement mapped end to end; one problem chosen; prep and write-up hours per call and calls per week estimated; ideas marked Efficiency or Opportunity |
| 3:40–5:00 (80 min) | 4 · The hack: build the Field Intelligence Engine swarm | The swarm ran one HCP end to end (brief, notes, CRM draft, follow-up), stopping at both gates; screenshots and timings captured |

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
Read AGENTS.md. We are the Field Intelligence Engine team at AI in Action for Medical Affairs.
Load medical-affairs-foundations and these skills: field-medical-planning, msl-pre-call-planning, kol-engagement-brief, msl-post-call-follow-up, hcp-discovery-and-access, msl-administrative-operations, deliverable-quality-review.
Use the practice data in https://github.com/Open-Medical-Affairs/Data-Sources: synthetic/[oncology-mm | immunology-ad | cardiometabolic-obesity]/ and synthetic/connected/ (the practice CRM). It is fictional (Nordvant Biopharma).
First, only: list the skills you loaded, then show the first 5 rows of hcps.csv and confirm the file is labelled SYNTHETIC. Do not start a mission yet.
Do not ask me to connect company systems. Do not send, post or change anything outside this conversation.
```

**Done looks like:** all members have a working Grok Bot; the agent lists the loaded skills and shows a file marked SYNTHETIC; the capture log exists.

### Block 2 · Warm-up missions (2:15–2:55)

- **Pair A:** [`msl-pre-call`](https://aiinaction.up.railway.app/missions/msl-pre-call) · Level 1 Starter · "Prepare the MSL pre-call brief". Before the call: a one-page brief from CRM history, open tasks and access context, with no invented meeting facts.
- **Pair B:** [`msl-post-call`](https://aiinaction.up.railway.app/missions/msl-post-call) · Level 1 Starter · "Turn the call notes into useful follow-up". After the call: notes to a CRM draft, a commitment and gap register, and a follow-up draft.
- Alternatives at the same level: [`msl-admin`](https://aiinaction.up.railway.app/missions/msl-admin) · Level 1 Starter · "Clear the administrative queue", [`kol-meeting`](https://aiinaction.up.railway.app/missions/kol-meeting) · Level 1 Starter · "Prepare for the difficult meeting"; one level up: [`hcp-access`](https://aiinaction.up.railway.app/missions/hcp-access) · Level 2 Pair · "Identify scientific coverage and access gaps". Background reading: [Team mission 1](https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills/blob/HEAD/workshop/missions/mission-1.md) ("Prepare me for a difficult conversation").

| Time | What happens |
|---|---|
| 2:15–2:18 | Split into two pairs. Pair A opens /missions/msl-pre-call, Pair B opens /missions/msl-post-call. Same practice TA. |
| 2:18–2:36 | Run both Level 1 missions in parallel (about 15–20 min each). |
| 2:36–2:48 | Push on it: Pair A asks "What did you not know about this HCP, and what did you refuse to guess?"; Pair B asks "Which commitments did the MSL make, and which need medical information or safety?" |
| 2:48–2:55 | Connect the two: could Pair B's output feed Pair A's next brief? That loop is your hack. Scribe logs it. |

**Done looks like:** at least one finished draft deliverable; the team saw where the agent stopped for a human (safety scan first, human is the final judge); three observations in the capture log ("it was good at…", "it missed…", "we had to decide…").

### Block 3 · Workflow ideation (2:55–3:40)

| Time | What happens |
|---|---|
| 2:55–3:10 | **Map today's workflow** for one real HCP engagement (prep, the call, the CRM note, the follow-up): steps, who does each, hand-offs, waiting time, hours. Sticky notes or a whiteboard; photograph it for the log. |
| 3:10–3:22 | **Spot the AI ideas.** Mark each step **E** (Efficiency AI: do today's work faster) or **O** (Opportunity AI: something not possible today). Use the examples in section 8 to spark ideas. Dot-vote. |
| 3:22–3:32 | **Pick one problem.** Write it as: "When [role] needs [outcome], today it takes [time] because [cause]." Fill the baseline column of the impact worksheet (section 12). |
| 3:32–3:40 | **Sketch the swarm** on paper: one lead agent, 3–5 sub-agents, the skill each loads, the hand-offs, and two human gates (section 9). Optional: the [Optimizer](https://aiinaction.up.railway.app/optimizer) "Agent swarm / coordinator" task. |

**Done looks like:** a photo of today's workflow; ideas marked E or O; one problem statement; baseline hours and frequency estimated; a swarm sketch with two gates. All in the capture log.

### Block 4 · The hack: build the swarm (3:40–5:00)

| Time | What happens |
|---|---|
| 3:40–3:50 | Write the assignment (starter below, or the [Optimizer](https://aiinaction.up.railway.app/optimizer) in swarm mode). Missing a skill? Use the **Skill creator** on the Optimizer page; read every SKILL.md it produces and approve it before use. |
| 3:50–4:25 | **Run 1.** Lead agent plans, sub-agents work; stop at Gate 1 (the MSL approves the brief and questions) and make the decision as a team. Note the minutes. |
| 4:25–4:30 | Optional stretch break. |
| 4:30–4:50 | **Run 2.** Fix the weakest hand-off (add a house rule, tighten a context packet), then run through Gate 2 (the MSL verifies the CRM note and follow-ups). Optional stress test with a change card. |
| 4:50–5:00 | **Capture.** Screenshots of the plan, a hand-off and each gate; timing notes; ask the agent to update the capture log and draft the slide outline from the template. Save everything. |

Reference missions: [`hcp-access`](https://aiinaction.up.railway.app/missions/hcp-access) · Level 2 Pair · "Identify scientific coverage and access gaps" and [`connected-planning`](https://aiinaction.up.railway.app/missions/connected-planning) · Level 3 Team · "Work across a practice CRM and content library" for working across the CRM; [`launch-plan-swarm`](https://aiinaction.up.railway.app/missions/launch-plan-swarm) · Level 4 Swarm · "Build the whole medical launch plan" for the wave-and-gate pattern.

Assignment starter (paste into Grok Bot, then edit the [brackets]):

```
# Assignment: Field Intelligence Engine swarm
You are the Field Copilot, a lead agent coordinating a small team of digital workers for a Medical Affairs team. This is an assignment, not a question: plan, delegate, check and hand back finished drafts.

## Goal: what done looks like
[One sentence: the problem we picked in ideation, and the deliverable that solves it.]

## Context to use
- https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills : read AGENTS.md, load medical-affairs-foundations, your lead skill field-medical-planning, and the skills named below.
- Practice data (fictional): https://github.com/Open-Medical-Affairs/Data-Sources synthetic/[TA]/ and synthetic/connected/. Or our own non-confidential data: [describe].

## How to work
1. Show me a short plan and the org chart of workers first. Wait for my OK.
2. Scan human-sourced records for possible safety findings (adverse events, product complaints, off-label use) before anything else. List them verbatim and stop until I acknowledge.
3. Run these sub-agents, each with only the context it needs:
   - Pre-call Briefer (skills: msl-pre-call-planning + kol-engagement-brief): Builds the one-page brief from CRM history and permitted materials. Hands off: Pre-call brief.
   - Coverage Mapper (skills: hcp-discovery-and-access): Finds coverage gaps and ethical access routes. Hands off: Coverage register.
   - Post-call Scribe (skills: msl-post-call-follow-up): Turns call notes into a CRM draft and a commitment register. Hands off: CRM draft + commitments.
   - Follow-up Drafter (skills: medical-information-response + medical-correspondence): Drafts answers to unsolicited questions and the follow-up letter. Hands off: Follow-up drafts.
   - Admin Clerk (skills: msl-administrative-operations): Updates the task queue and the weekly status brief. Hands off: Task queue.
4. STOP at Gate 1: Before the call: the MSL approves the brief and the planned questions (non-promotional, scientifically balanced, within permitted materials). Show me the evidence pack and wait.
5. Continue, then have an independent checker (deliverable-quality-review (reports to the MSL, not the lead)) review the draft. Fix what it finds.
6. STOP at Gate 2: After the call: the MSL verifies the CRM note, the commitments and the follow-up drafts before anything is logged or sent; safety findings and off-label requests go to the right function. Wait for my decision.
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
| **10:40–11:00 AM** | **Field Intelligence Engine presents** (about 20 minutes, give or take, including a short live demo and a few questions). |

> **Timing.** Teams present 01→04 from 9:40, about 20 minutes each including a few questions, before the 11:00 WPP demo. The morning build is short, so keep all decks on one laptop and treat the Day 1 4:50–5:00 capture as essential. Watch the other teams; make final edits only in the minutes before your slot.

## 5. Recommended missions

| Mission (link) | Why |
|---|---|
| [`msl-pre-call`](https://aiinaction.up.railway.app/missions/msl-pre-call) · Level 1 Starter · "Prepare the MSL pre-call brief" | Warm-up (Pair A). Before the call: a one-page brief from CRM history, open tasks and access context, with no invented meeting facts. |
| [`msl-post-call`](https://aiinaction.up.railway.app/missions/msl-post-call) · Level 1 Starter · "Turn the call notes into useful follow-up" | Warm-up (Pair B). After the call: notes to a CRM draft, a commitment and gap register, and a follow-up draft. |
| [`hcp-access`](https://aiinaction.up.railway.app/missions/hcp-access) · Level 2 Pair · "Identify scientific coverage and access gaps" | Hack reference: coverage and access gaps, institution-aware access plan. |
| [`connected-planning`](https://aiinaction.up.railway.app/missions/connected-planning) · Level 3 Team · "Work across a practice CRM and content library" | Hack reference: account priorities across the practice CRM and content library. |
| [`msl-admin`](https://aiinaction.up.railway.app/missions/msl-admin) · Level 1 Starter · "Clear the administrative queue" | Optional sub-agent: prioritized task queue and weekly status brief. |
| [`launch-plan-swarm`](https://aiinaction.up.railway.app/missions/launch-plan-swarm) · Level 4 Swarm · "Build the whole medical launch plan" | The only Level 4 mission: waves of digital workers with human gates between waves. Use it as the model for your swarm. |
| [Team mission 1](https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills/blob/HEAD/workshop/missions/mission-1.md) | Background: the original team mission behind this vertical. |

Levels: 1 Starter = one skill · 2 Pair = lead + one sub-worker · 3 Team = lead + two or more sub-workers · 4 Swarm = waves with human gates. All missions: [https://aiinaction.up.railway.app/missions](https://aiinaction.up.railway.app/missions). Ready prompts: [https://aiinaction.up.railway.app/prompts](https://aiinaction.up.railway.app/prompts).

## 6. Recommended skills

| Skill (Medical-Affairs-Skills) | Use it for |
|---|---|
| [`field-medical-planning`](https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills/blob/HEAD/skills/field-medical-planning/SKILL.md) | Lead: territory and account priorities, MSL objectives |
| [`msl-pre-call-planning`](https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills/blob/HEAD/skills/msl-pre-call-planning/SKILL.md) | One-page pre-call brief |
| [`kol-engagement-brief`](https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills/blob/HEAD/skills/kol-engagement-brief/SKILL.md) | Deeper brief for a named expert |
| [`hcp-discovery-and-access`](https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills/blob/HEAD/skills/hcp-discovery-and-access/SKILL.md) | Coverage gaps and ethical access routes |
| [`msl-post-call-follow-up`](https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills/blob/HEAD/skills/msl-post-call-follow-up/SKILL.md) | Notes to CRM draft and follow-up |
| [`meeting-transcription`](https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills/blob/HEAD/skills/meeting-transcription/SKILL.md) | Optional: from a recorded or typed transcript |
| [`msl-administrative-operations`](https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills/blob/HEAD/skills/msl-administrative-operations/SKILL.md) | Task queues, meeting packs, status brief |
| [`medical-information-response`](https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills/blob/HEAD/skills/medical-information-response/SKILL.md) | Unsolicited questions routed and drafted |
| [`medical-correspondence`](https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills/blob/HEAD/skills/medical-correspondence/SKILL.md) | Formal follow-up letters (drafts) |
| [`data-connection`](https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills/blob/HEAD/skills/data-connection/SKILL.md) | Read the practice CRM tables |
| [`deliverable-quality-review`](https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills/blob/HEAD/skills/deliverable-quality-review/SKILL.md) | Independent red-team of the draft |

Every skill: [https://aiinaction.up.railway.app/skills](https://aiinaction.up.railway.app/skills) · library: [github.com/Open-Medical-Affairs/Medical-Affairs-Skills](https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills). Workflow not covered? Build a skill with the Skill creator on [https://aiinaction.up.railway.app/optimizer](https://aiinaction.up.railway.app/optimizer) and review it before use.

## 7. Practice data

All practice data are fictional (Nordvant Biopharma; NORVANTIB in multiple myeloma, DERMALYX in atopic dermatitis, ADIPOSYN in obesity; plus a practice CRM). Browse and copy links at [https://aiinaction.up.railway.app/data](https://aiinaction.up.railway.app/data). Teams may instead bring their own **non-confidential** data (no patient data, no confidential company data, no real HCP personal data).

**TA pack files** (pick one TA; links: MM · AD · Obesity), folder: [synthetic/](https://github.com/Open-Medical-Affairs/Data-Sources/tree/main/synthetic)

- `kol-dossiers.md` ([MM · NORVANTIB](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/oncology-mm/kol-dossiers.md) · [AD · DERMALYX](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/immunology-ad/kol-dossiers.md) · [Obesity · ADIPOSYN](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/cardiometabolic-obesity/kol-dossiers.md))
- `interaction-notes.md` ([MM · NORVANTIB](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/oncology-mm/interaction-notes.md) · [AD · DERMALYX](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/immunology-ad/interaction-notes.md) · [Obesity · ADIPOSYN](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/cardiometabolic-obesity/interaction-notes.md))
- `field-account-plan.csv` ([MM · NORVANTIB](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/oncology-mm/field-account-plan.csv) · [AD · DERMALYX](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/immunology-ad/field-account-plan.csv) · [Obesity · ADIPOSYN](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/cardiometabolic-obesity/field-account-plan.csv))
- `product-profile.md` ([MM · NORVANTIB](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/oncology-mm/product-profile.md) · [AD · DERMALYX](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/immunology-ad/product-profile.md) · [Obesity · ADIPOSYN](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/cardiometabolic-obesity/product-profile.md))
- `evidence-landscape.md` ([MM · NORVANTIB](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/oncology-mm/evidence-landscape.md) · [AD · DERMALYX](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/immunology-ad/evidence-landscape.md) · [Obesity · ADIPOSYN](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/cardiometabolic-obesity/evidence-landscape.md))
- `medical-plan.md` ([MM · NORVANTIB](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/oncology-mm/medical-plan.md) · [AD · DERMALYX](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/immunology-ad/medical-plan.md) · [Obesity · ADIPOSYN](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/cardiometabolic-obesity/medical-plan.md))

**Practice CRM** ([synthetic/connected/](https://github.com/Open-Medical-Affairs/Data-Sources/tree/main/synthetic/connected/))

- [`hcps.csv`](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/connected/hcps.csv)
- [`interactions.csv`](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/connected/interactions.csv)
- [`accounts.csv`](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/connected/accounts.csv)
- [`access_log.csv`](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/connected/access_log.csv)
- [`msl_tasks.csv`](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/connected/msl_tasks.csv)
- [`enquiries.csv`](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/connected/enquiries.csv)
- [`content_assets.csv`](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/connected/content_assets.csv)
- [`data-dictionary.json`](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/connected/data-dictionary.json)

The practice CRM also ships as one SQLite file ([`medical-affairs.sqlite`](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/connected/medical-affairs.sqlite)) if the agent prefers to query it. All HCPs, accounts and MSLs are fictional; never paste real HCP names.

## 8. Example AI ideas

**Efficiency AI** (today's work, faster)

1. Pre-call brief in five minutes: prior interactions, open enquiries, open tasks, permitted materials and suggested questions on one page.
2. Post-call CRM note, commitment register and follow-up draft from the MSL's notes, ready for the MSL to verify.
3. Weekly admin queue cleared: overdue tasks, missing records and the status brief assembled from the CRM.

**Opportunity AI** (something that is not possible today)

1. A brief before every HCP interaction, not only the top KOLs: preparation quality becomes the same across the whole team.
2. Coverage-gap radar: HCPs with unanswered scientific questions, or no scientific contact this quarter, surfaced weekly with an ethical access route.
3. Closed loop: every call automatically feeds insights to the Insights team and unsolicited questions to Medical Information, so nothing said in the field is lost.

## 9. Suggested swarm shape

```
MSL (human) · final judge, with the field medical director
   │   Gate 1 · Gate 2 (human decisions)
   └── Lead agent: Field Copilot  [field-medical-planning]
         ├── Pre-call Briefer  [msl-pre-call-planning + kol-engagement-brief]  → Pre-call brief
         ├── Coverage Mapper  [hcp-discovery-and-access]  → Coverage register
         ├── Post-call Scribe  [msl-post-call-follow-up]  → CRM draft + commitments
         ├── Follow-up Drafter  [medical-information-response + medical-correspondence]  → Follow-up drafts
         └── Admin Clerk  [msl-administrative-operations]  → Task queue
   Independent checker → reports to the human: deliverable-quality-review (reports to the MSL, not the lead)
```

| Worker | Skill(s) | Does | Hands off |
|---|---|---|---|
| **Lead: Field Copilot** | [`field-medical-planning`](https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills/blob/HEAD/skills/field-medical-planning/SKILL.md) | Plans, gives each worker its context packet, assembles, stops at the gates | Plan and final draft |
| Pre-call Briefer | `msl-pre-call-planning + kol-engagement-brief` | Builds the one-page brief from CRM history and permitted materials | Pre-call brief |
| Coverage Mapper | `hcp-discovery-and-access` | Finds coverage gaps and ethical access routes | Coverage register |
| Post-call Scribe | `msl-post-call-follow-up` | Turns call notes into a CRM draft and a commitment register | CRM draft + commitments |
| Follow-up Drafter | `medical-information-response + medical-correspondence` | Drafts answers to unsolicited questions and the follow-up letter | Follow-up drafts |
| Admin Clerk | `msl-administrative-operations` | Updates the task queue and the weekly status brief | Task queue |

**Hand-offs:** Coverage register → pre-call brief → (Gate 1) → call happens (human) → CRM draft + commitments → follow-up drafts → (Gate 2) → task queue

**Gate 1:** Before the call: the MSL approves the brief and the planned questions (non-promotional, scientifically balanced, within permitted materials). Why a human: the MSL is accountable for the scientific exchange and for compliance.

**Gate 2:** After the call: the MSL verifies the CRM note, the commitments and the follow-up drafts before anything is logged or sent; safety findings and off-label requests go to the right function. Why a human: CRM records are official records and correspondence leaves the company.

**Always-on stop (not a gate, a rule):** any possible adverse event, product quality complaint or off-label signal in human-sourced records is listed verbatim and routed by a human before analysis continues.

## 10. Walk-around question bank

Facilitators: no share-out at the end of Day 1, so these questions are the feedback loop. Ask one or two per visit, then leave.

**During ideation (2:55–3:40)**

1. How long does an MSL spend preparing for one scientific exchange today? For which HCPs do they skip it?
2. Where does the information for a brief live today, and which source is least trusted?
3. What happens today to a commitment an MSL makes in a meeting? How often does it slip?
4. Which part of the call itself must always stay human?

**During the hack (3:40–5:00)**

5. Show me a fact in the brief and the CRM row it came from. What did the agent refuse to guess?
6. Is anything in the brief promotional or off-label? How would the swarm catch it?
7. What happens when the call notes contain a possible adverse event? Who gets it, and how fast?
8. Where are Gate 1 and Gate 2, and what does the MSL see at each?
9. What personal information about the HCP is the agent allowed to use? Professional context only?
10. How many calls per MSL per week? How long do prep and write-up take today versus with the swarm, including the MSL's review?

## 11. Common pitfalls and how to unblock

| Pitfall | Unblock |
|---|---|
| The agent invents meeting facts or HCP details. | Rule: every fact in the brief cites a CRM row; unknowns go to "open questions". |
| Promotional tone in briefs or follow-ups. | Load kol-engagement-brief and the checker; Gate 1 includes a non-promotional check. |
| Sending or logging without review. | The agent drafts only. "Do not send, post or change any system" goes in the assignment. |
| Real HCP names typed in from memory. | Practice data only, or your own non-confidential, de-identified data. |
| Trying to cover the whole territory at once. | Start with one HCP end to end (brief, call notes, follow-up), then scale to five. |
| Access data used unethically. | hcp-discovery-and-access proposes institution-aware routes; humans decide on any outreach. |
| Grok Bot cannot open GitHub. | Upload the starter bundle for your TA from [https://aiinaction.up.railway.app/grokbot](https://aiinaction.up.railway.app/grokbot), or the repository ZIP. |
| The agent asks to connect company systems. | Say no: the workshop uses practice data. It is in every setup prompt. |
| A run is slow or wanders. | Ask for the plan first, then run one sub-agent at a time; cut the scope to one TA, one HCP, one output. |
| The output is generic. | Teach the agent: add 3–5 house rules (what good looks like, what must never appear) and run again. |

## 12. Impact worksheet

Teams supply their own estimates. Count every person involved and **include human review time** in the AI-assisted column.

| Line | Today (baseline) | AI-assisted | Notes |
|---|---|---|---|
| A. Hours per cycle (all people) | ____ h | ____ h | Cycle = one HCP call (prep + CRM note + follow-up), per MSL |
| B. Cycles per year | ____ | ____ | How often it happens |
| C. Loaded hourly rate | $____ /h | $____ /h | Salary + benefits + overhead; agree one number as a team |
| D. Hours saved per year | | **(A today − A AI) × B = ____ h** | |
| E. Value per year | | **D × C = $____** | Estimate, not a measured result |
| F. Other benefits | | | Speed (days to decision), coverage (% of HCPs, sessions, records), quality (errors caught) |

> **ILLUSTRATIVE ONLY, not data:** 2.5 h → 0.75 h per cycle × 200 cycles/year = 350 h saved; × $120/h = $42,000 per year. Replace every number with the team's own estimate.

These numbers go on slide 8 of the final template (formula tiles and bar chart).

---

*All products, people and results in the practice data are fictional. Outputs are drafts that need qualified human review; this is not a clinical decision, GxP or pharmacovigilance system.*
