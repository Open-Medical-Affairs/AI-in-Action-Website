# 03 · Congress Monitor: agenda and facilitator guide

**AI in Action for Medical Affairs** · October 13–14, 2026 · Convene (2nd floor), Two Commerce Square, 2001 Market St, Philadelphia · Host and keynote: Vivek Mukhatyar · Companion site: [aiinaction.up.railway.app](https://aiinaction.up.railway.app)

> **Assumption:** one team per vertical (four teams). The Day 1 afternoon agenda below is an optional suggestion; teams may move faster or slower. Times are ET.

## At a glance

| | |
|---|---|
| Vertical | 03 · Congress Monitor: *The congress just ended. What changed, and what do we do about it?* |
| Warm-up missions | [`congress`](https://aiinaction.up.railway.app/missions/congress) · Level 2 Pair · "What changed after congress?"; [`kol-meeting`](https://aiinaction.up.railway.app/missions/kol-meeting) · Level 1 Starter · "Prepare for the difficult meeting" |
| Lead skill for the hack | [`congress-intelligence`](https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills/blob/HEAD/skills/congress-intelligence/SKILL.md) |
| Practice data | Any TA. Each pack has congress-abstracts.md and competitor-announcements.md written for it. |
| Day 2 presentation | This team presents third (03 of 04): teams present in order 01→04 after the final build, about 20 minutes each including a few questions |

## 1. Challenge statement

Three days, sixty presentations, two competitor announcements, and leadership has four minutes. Today the readout lands a week later as a summary of what was presented, after people have already formed their impressions.

## 2. Sharpened problem prompt

> Build an AI workforce that, within hours of a congress closing, compares what was presented against what we expected and what our medical plan currently claims, applies the same scepticism to our data as to competitors', and tells leadership on one page what changed, why it matters, what to watch and what we should do, with every claim traced to an abstract or announcement. Humans approve the expectations and any recommended change.

Teams can keep this prompt or narrow it to one workflow they know. A good narrowed prompt names the role, the trigger, the deliverable and the decision it serves.

## 3. Day 1 afternoon: suggested agenda (Tue Oct 13)

Context: Day 1 morning: registration, opening keynote and sandbox intro, team creation and function audit; lunch; then **the build afternoon** (four blocks, about 3¼ hours in all); evening cocktail reception. All durations below are approximate.

| About | Block (in order) | Done looks like |
|---|---|---|
| about 30 min | 1 · Set up Grok Bot and load the skills | Every member signed in; the driver's conversation has the skills loaded and has read one practice file; capture log started |
| about 40 min | 2 · Warm-up missions: `congress` + `kol-meeting` | A four-section congress readout exists; the team checked the agent applied the same scepticism to both sides; 3 observations logged |
| about 45 min | 3 · Workflow ideation: the post-congress readout | The congress readout cycle mapped; one problem chosen; hours per congress and congresses per year estimated; ideas marked Efficiency or Opportunity |
| about 80 min (about 1½ hours) | 4 · The hack: build the Congress Monitor swarm | The swarm produced graded abstracts, a what-changed list and a one-page readout, stopping at both gates; screenshots and timings captured |

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
Read AGENTS.md. We are the Congress Monitor team at AI in Action for Medical Affairs.
Load medical-affairs-foundations and these skills: congress-intelligence, competitive-intelligence, evidence-appraisal, strategic-analysis, executive-briefing, citation-integrity, deliverable-quality-review.
Use the practice data in https://github.com/Open-Medical-Affairs/Data-Sources: synthetic/[oncology-mm | immunology-ad | cardiometabolic-obesity]/ and synthetic/connected/ (the practice CRM). It is fictional (Nordvant Biopharma).
First, only: list the skills you loaded, then show the first 5 rows of interactions.csv and confirm the file is labelled SYNTHETIC. Do not start a mission yet.
Do not ask me to connect company systems. Do not send, post or change anything outside this conversation.
```

**Done looks like:** all members have a working Grok Bot; the agent lists the loaded skills and shows a file marked SYNTHETIC; the capture log exists.

### Block 2 · Warm-up missions (about 40 min)

- **Whole team (one driver):** [`congress`](https://aiinaction.up.railway.app/missions/congress) · Level 2 Pair · "What changed after congress?". The core task: congress findings compared with the existing medical plan; what changes, what does not, and why.
- **Pair B (optional, in parallel):** [`kol-meeting`](https://aiinaction.up.railway.app/missions/kol-meeting) · Level 1 Starter · "Prepare for the difficult meeting". Prepare a post-congress conversation with a sceptical expert: what will she ask about the new data?
- Simpler alternative: [`field-insights`](https://aiinaction.up.railway.app/missions/field-insights) · Level 2 Pair · "What should leadership know?" (the site lists it as the step below congress). Background reading: [Team mission 3](https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills/blob/HEAD/workshop/missions/mission-3.md) ("The congress just ended. Tell leadership what changed.").

| About | What happens (in order) |
|---|---|
| about 5 min | Open /missions/congress, pick the TA, copy the prompt. Optional: Pair B opens /missions/kol-meeting. |
| about 20 min | Run the congress mission (about 15–20 min). Pair B runs kol-meeting in parallel. |
| about 10 min | Push on it: "What did you expect before the congress? Show me where reality differed." then "What was presented that contradicts something we currently claim?" |
| about 5 min | Check symmetry: was the agent as tough on our data as on the competitor's? Scribe logs three observations. |

**Done looks like:** at least one finished draft deliverable; the team saw where the agent stopped for a human (safety scan first, human is the final judge); three observations in the capture log ("it was good at…", "it missed…", "we had to decide…").

### Block 3 · Workflow ideation (about 45 min)

| About | What happens (in order) |
|---|---|
| about 15 min | **Map today's workflow** for one real post-congress readout (from session coverage to the leadership update and field materials): steps, who does each, hand-offs, waiting time, hours. Sticky notes or a whiteboard; photograph it for the log. |
| about 10 min | **Spot the AI ideas.** Mark each step **E** (Efficiency AI: do today's work faster) or **O** (Opportunity AI: something not possible today). Use the examples in section 8 to spark ideas. Dot-vote. |
| about 10 min | **Pick one problem.** Write it as: "When [role] needs [outcome], today it takes [time] because [cause]." Fill the baseline column of the impact worksheet (section 12). |
| about 10 min | **Sketch the swarm** on paper: one lead agent, 3–5 sub-agents, the skill each loads, the hand-offs, and two human gates (section 9). Optional: the [Optimizer](https://aiinaction.up.railway.app/optimizer) "Agent swarm / coordinator" task. |

**Done looks like:** a photo of today's workflow; ideas marked E or O; one problem statement; baseline hours and frequency estimated; a swarm sketch with two gates. All in the capture log.

### Block 4 · The hack: build the swarm (about 80 min)

| About | What happens (in order) |
|---|---|
| about 10 min | Write the assignment (starter below, or the [Optimizer](https://aiinaction.up.railway.app/optimizer) in swarm mode). Missing a skill? Use the **Skill creator** on the Optimizer page; read every SKILL.md it produces and approve it before use. |
| about 35 min | **Run 1.** Lead agent plans, sub-agents work; stop at Gate 1 (the expectations register and the shortlist that matters) and make the decision as a team. Note the minutes. |
| about 5 min | Optional stretch break. |
| about 20 min | **Run 2.** Fix the weakest hand-off (add a house rule, tighten a context packet), then run through Gate 2 (the medical director approves the recommendations). Optional stress test with a change card. |
| about 10 min | **Capture.** Screenshots of the plan, a hand-off and each gate; timing notes; ask the agent to update the capture log and draft the slide outline from the template. Save everything. |

Reference missions: [`congress`](https://aiinaction.up.railway.app/missions/congress) · Level 2 Pair · "What changed after congress?" as the core; [`connected-planning`](https://aiinaction.up.railway.app/missions/connected-planning) · Level 3 Team · "Work across a practice CRM and content library" if you want to find affected content in the practice CRM; [`launch-plan-swarm`](https://aiinaction.up.railway.app/missions/launch-plan-swarm) · Level 4 Swarm · "Build the whole medical launch plan" for the wave-and-gate pattern.

Assignment starter (paste into Grok Bot, then edit the [brackets]):

```
# Assignment: Congress Monitor swarm
You are the Congress Lead, a lead agent coordinating a small team of digital workers for a Medical Affairs team. This is an assignment, not a question: plan, delegate, check and hand back finished drafts.

## Goal: what done looks like
[One sentence: the problem we picked in ideation, and the deliverable that solves it.]

## Context to use
- https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills : read AGENTS.md, load medical-affairs-foundations, your lead skill congress-intelligence, and the skills named below.
- Practice data (fictional): https://github.com/Open-Medical-Affairs/Data-Sources synthetic/[TA]/ and synthetic/connected/. Or our own non-confidential data: [describe].

## How to work
1. Show me a short plan and the org chart of workers first. Wait for my OK.
2. Scan human-sourced records for possible safety findings (adverse events, product complaints, off-label use) before anything else. List them verbatim and stop until I acknowledge.
3. Run these sub-agents, each with only the context it needs:
   - Abstract Triage (skills: evidence-appraisal): Reads and grades every abstract; tags relevance to our plan. Hands off: Graded abstract table.
   - Competitor Watch (skills: competitive-intelligence (+ clinical-trials-search)): Separates data from spin in competitor announcements. Hands off: Competitor moves table.
   - Plan Comparator (skills: strategic-analysis + medical-strategy-plan): Compares findings with our expectations and current claims. Hands off: What-changed list.
   - Field Pulse (skills: field-insight-synthesis): Reads Congress-channel CRM interactions for HCP reactions. Hands off: HCP reaction summary.
   - Briefer (skills: executive-briefing): Writes the one-page, four-section readout. Hands off: Leadership readout.
4. STOP at Gate 1: Before the Plan Comparator runs: the congress lead approves the expectations register and the shortlist of findings that matter. Show me the evidence pack and wait.
5. Continue, then have an independent checker (citation-integrity + deliverable-quality-review (report to the human, not the lead)) review the draft. Fix what it finds.
6. STOP at Gate 2: After the Briefer: the medical director approves the recommendations before any plan, claim, material or field communication changes. Wait for my decision.
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
| **about 20 min** | **Congress Monitor presents third (03 of 04)** (about 20 minutes, give or take, including a short live demo and a few questions). |

> **Timing.** The final build and rehearsal take about 30–40 min at the start of Day 2; then teams present in order 01→04, about 20 minutes each including a few questions, before the WPP demo. The morning build is short, so keep all decks on one laptop and treat the capture step near the end of Day 1 as essential. Watch the other teams; make final edits only in the minutes before your turn.

## 5. Recommended missions

| Mission (link) | Why |
|---|---|
| [`congress`](https://aiinaction.up.railway.app/missions/congress) · Level 2 Pair · "What changed after congress?" | Warm-up (Whole team (one driver)). The core task: congress findings compared with the existing medical plan; what changes, what does not, and why. |
| [`kol-meeting`](https://aiinaction.up.railway.app/missions/kol-meeting) · Level 1 Starter · "Prepare for the difficult meeting" | Warm-up (Pair B (optional, in parallel)). Prepare a post-congress conversation with a sceptical expert: what will she ask about the new data? |
| [`connected-planning`](https://aiinaction.up.railway.app/missions/connected-planning) · Level 3 Team · "Work across a practice CRM and content library" | Hack reference: find which content assets and field materials the congress makes out of date. |
| [`advisory-board`](https://aiinaction.up.railway.app/missions/advisory-board) · Level 3 Team · "Design an advisory board worth holding" | Optional: if the team wants a post-congress expert input loop. |
| [`launch-plan-swarm`](https://aiinaction.up.railway.app/missions/launch-plan-swarm) · Level 4 Swarm · "Build the whole medical launch plan" | The only Level 4 mission: waves of digital workers with human gates between waves. Use it as the model for your swarm. |
| [Team mission 3](https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills/blob/HEAD/workshop/missions/mission-3.md) | Background: the original team mission behind this vertical. |

Levels: 1 Starter = one skill · 2 Pair = lead + one sub-worker · 3 Team = lead + two or more sub-workers · 4 Swarm = waves with human gates. All missions: [https://aiinaction.up.railway.app/missions](https://aiinaction.up.railway.app/missions). Ready prompts: [https://aiinaction.up.railway.app/prompts](https://aiinaction.up.railway.app/prompts).

## 6. Recommended skills

| Skill (Medical-Affairs-Skills) | Use it for |
|---|---|
| [`congress-intelligence`](https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills/blob/HEAD/skills/congress-intelligence/SKILL.md) | Lead: what changed and what to do, not a summary |
| [`competitive-intelligence`](https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills/blob/HEAD/skills/competitive-intelligence/SKILL.md) | Competitor moves and what they signal |
| [`evidence-appraisal`](https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills/blob/HEAD/skills/evidence-appraisal/SKILL.md) | Grade each abstract before using it |
| [`strategic-analysis`](https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills/blob/HEAD/skills/strategic-analysis/SKILL.md) | Implications for our plan |
| [`medical-strategy-plan`](https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills/blob/HEAD/skills/medical-strategy-plan/SKILL.md) | Challenge the current plan |
| [`clinical-trials-search`](https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills/blob/HEAD/skills/clinical-trials-search/SKILL.md) | ClinicalTrials.gov landscape (public, optional) |
| [`pubmed-search`](https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills/blob/HEAD/skills/pubmed-search/SKILL.md) | Published context (public, optional) |
| [`literature-surveillance`](https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills/blob/HEAD/skills/literature-surveillance/SKILL.md) | Keep watching after the congress |
| [`executive-briefing`](https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills/blob/HEAD/skills/executive-briefing/SKILL.md) | The one-page, four-minute readout |
| [`medical-slide-deck`](https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills/blob/HEAD/skills/medical-slide-deck/SKILL.md) | Optional readout deck |
| [`citation-integrity`](https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills/blob/HEAD/skills/citation-integrity/SKILL.md) | Every claim traced to an abstract |
| [`deliverable-quality-review`](https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills/blob/HEAD/skills/deliverable-quality-review/SKILL.md) | Independent red-team of the draft |

Every skill: [https://aiinaction.up.railway.app/skills](https://aiinaction.up.railway.app/skills) · library: [github.com/Open-Medical-Affairs/Medical-Affairs-Skills](https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills). Workflow not covered? Build a skill with the Skill creator on [https://aiinaction.up.railway.app/optimizer](https://aiinaction.up.railway.app/optimizer) and review it before use.

## 7. Practice data

All practice data are fictional (Nordvant Biopharma; NORVANTIB in multiple myeloma, DERMALYX in atopic dermatitis, ADIPOSYN in obesity; plus a practice CRM). Browse and copy links at [https://aiinaction.up.railway.app/data](https://aiinaction.up.railway.app/data). Teams may instead bring their own **non-confidential** data (no patient data, no confidential company data, no real HCP personal data).

**TA pack files** (pick one TA; links: MM · AD · Obesity), folder: [synthetic/](https://github.com/Open-Medical-Affairs/Data-Sources/tree/main/synthetic)

- `congress-abstracts.md` ([MM · NORVANTIB](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/oncology-mm/congress-abstracts.md) · [AD · DERMALYX](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/immunology-ad/congress-abstracts.md) · [Obesity · ADIPOSYN](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/cardiometabolic-obesity/congress-abstracts.md))
- `competitor-announcements.md` ([MM · NORVANTIB](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/oncology-mm/competitor-announcements.md) · [AD · DERMALYX](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/immunology-ad/competitor-announcements.md) · [Obesity · ADIPOSYN](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/cardiometabolic-obesity/competitor-announcements.md))
- `evidence-landscape.md` ([MM · NORVANTIB](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/oncology-mm/evidence-landscape.md) · [AD · DERMALYX](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/immunology-ad/evidence-landscape.md) · [Obesity · ADIPOSYN](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/cardiometabolic-obesity/evidence-landscape.md))
- `medical-plan.md` ([MM · NORVANTIB](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/oncology-mm/medical-plan.md) · [AD · DERMALYX](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/immunology-ad/medical-plan.md) · [Obesity · ADIPOSYN](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/cardiometabolic-obesity/medical-plan.md))
- `product-profile.md` ([MM · NORVANTIB](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/oncology-mm/product-profile.md) · [AD · DERMALYX](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/immunology-ad/product-profile.md) · [Obesity · ADIPOSYN](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/cardiometabolic-obesity/product-profile.md))
- `guideline-landscape.md` ([MM · NORVANTIB](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/oncology-mm/guideline-landscape.md) · [AD · DERMALYX](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/immunology-ad/guideline-landscape.md) · [Obesity · ADIPOSYN](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/cardiometabolic-obesity/guideline-landscape.md))
- `kol-dossiers.md` ([MM · NORVANTIB](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/oncology-mm/kol-dossiers.md) · [AD · DERMALYX](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/immunology-ad/kol-dossiers.md) · [Obesity · ADIPOSYN](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/cardiometabolic-obesity/kol-dossiers.md))
- `field-observations.csv` ([MM · NORVANTIB](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/oncology-mm/field-observations.csv) · [AD · DERMALYX](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/immunology-ad/field-observations.csv) · [Obesity · ADIPOSYN](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/cardiometabolic-obesity/field-observations.csv))

**Practice CRM** ([synthetic/connected/](https://github.com/Open-Medical-Affairs/Data-Sources/tree/main/synthetic/connected/))

- [`interactions.csv`](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/connected/interactions.csv)
- [`content_assets.csv`](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/connected/content_assets.csv)
- [`hcps.csv`](https://github.com/Open-Medical-Affairs/Data-Sources/blob/main/synthetic/connected/hcps.csv)

The practice CRM interactions table has a Congress channel: filter it to see what HCPs said at the congress. content_assets.csv shows which materials may now be out of date.

## 8. Example AI ideas

**Efficiency AI** (today's work, faster)

1. Abstract triage: every abstract tagged by relevance to our plan, with an evidence-quality grade, in the first hour after the congress.
2. Competitor announcement digest that separates what the data show from what the press release claims.
3. Same-day first draft of the four-section leadership readout (what changed, why it matters, what to watch, what to do).

**Opportunity AI** (something that is not possible today)

1. Expectation-vs-reality diff: log our expectations before the congress, then get an automatic "where reality differed" analysis when it closes.
2. Cover every session and poster, not only the top ten, so weak signals and small studies are not missed.
3. Downstream impact in 24 hours: which of our claims, slides, FAQs and MSL materials are now outdated, plus draft field talking points for human approval.

## 9. Suggested swarm shape

```
Congress lead / medical director (human) · final judge
   │   Gate 1 · Gate 2 (human decisions)
   └── Lead agent: Congress Lead  [congress-intelligence]
         ├── Abstract Triage  [evidence-appraisal]  → Graded abstract table
         ├── Competitor Watch  [competitive-intelligence (+ clinical-trials-search)]  → Competitor moves table
         ├── Plan Comparator  [strategic-analysis + medical-strategy-plan]  → What-changed list
         ├── Field Pulse  [field-insight-synthesis]  → HCP reaction summary
         └── Briefer  [executive-briefing]  → Leadership readout
   Independent checker → reports to the human: citation-integrity + deliverable-quality-review (report to the human, not the lead)
```

| Worker | Skill(s) | Does | Hands off |
|---|---|---|---|
| **Lead: Congress Lead** | [`congress-intelligence`](https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills/blob/HEAD/skills/congress-intelligence/SKILL.md) | Plans, gives each worker its context packet, assembles, stops at the gates | Plan and final draft |
| Abstract Triage | `evidence-appraisal` | Reads and grades every abstract; tags relevance to our plan | Graded abstract table |
| Competitor Watch | `competitive-intelligence (+ clinical-trials-search)` | Separates data from spin in competitor announcements | Competitor moves table |
| Plan Comparator | `strategic-analysis + medical-strategy-plan` | Compares findings with our expectations and current claims | What-changed list |
| Field Pulse | `field-insight-synthesis` | Reads Congress-channel CRM interactions for HCP reactions | HCP reaction summary |
| Briefer | `executive-briefing` | Writes the one-page, four-section readout | Leadership readout |

**Hand-offs:** Graded abstracts + competitor moves → (Gate 1) → what-changed list + HCP reactions → readout → checker → (Gate 2)

**Gate 1:** Before the Plan Comparator runs: the congress lead approves the expectations register and the shortlist of findings that matter. Why a human: deciding what "matters" for the strategy is judgment, and it stops the agent anchoring on the wrong comparison.

**Gate 2:** After the Briefer: the medical director approves the recommendations before any plan, claim, material or field communication changes. Why a human: changing scientific positions and field messaging needs accountable sign-off and compliance review.

**Always-on stop (not a gate, a rule):** any possible adverse event, product quality complaint or off-label signal in human-sourced records is listed verbatim and routed by a human before analysis continues.

## 10. Walk-around question bank

Facilitators: no share-out at the end of Day 1, so these questions are the feedback loop. Ask one or two per visit, then leave.

**During ideation (block 3)**

1. How long after the congress does leadership get the readout today? What decisions are made before it arrives?
2. What did your team expect before this congress? Where is that written down today?
3. Who decides which sessions to cover today, and what gets missed?
4. Which downstream materials (slides, FAQs, MSL decks) usually go out of date after a congress?

**During the hack (block 4)**

5. Show me the "expected vs what happened" comparison. Where did reality differ?
6. Is the swarm as sceptical about our data as about the competitor's? Show me one example of each.
7. What does the agent do with a single-arm study or a press-release claim with no data?
8. Where is Gate 1, and what does the congress lead approve there?
9. Which recommendation would change something external, and who signs that off?
10. How many people-hours does a congress readout take today, from session coverage to leadership deck? Per congress, how many congresses a year?

## 11. Common pitfalls and how to unblock

| Pitfall | Unblock |
|---|---|
| A summary of what was presented, not analysis. | Ask for the comparison against prior expectations and the current plan; load strategic-analysis. |
| Asymmetric scepticism (tough on them, generous on us). | Give the same evidence-appraisal checklist to both; the checker compares the two. |
| Abstracts cited as if they were published evidence. | Mark abstract-level data as preliminary; citation-integrity flags every overreach. |
| Press-release language copied into the readout. | Competitor Watch separates "what the data show" from "what they claim". |
| Sixty abstracts is a lot for 80 minutes. | Start with the ten most relevant (the triage worker picks, a human confirms), then widen. |
| Talking points drift into promotion. | Field talking points are drafts for medical and compliance review only (Gate 2). |
| Grok Bot cannot open GitHub. | Upload the starter bundle for your TA from [https://aiinaction.up.railway.app/grokbot](https://aiinaction.up.railway.app/grokbot), or the repository ZIP. |
| The agent asks to connect company systems. | Say no: the workshop uses practice data. It is in every setup prompt. |
| A run is slow or wanders. | Ask for the plan first, then run one sub-agent at a time; cut the scope to one TA, one HCP, one output. |
| The output is generic. | Teach the agent: add 3–5 house rules (what good looks like, what must never appear) and run again. |

## 12. Impact worksheet

Teams supply their own estimates. Count every person involved and **include human review time** in the AI-assisted column.

| Line | Today (baseline) | AI-assisted | Notes |
|---|---|---|---|
| A. Hours per cycle (all people) | ____ h | ____ h | Cycle = one major congress readout (coverage, analysis, leadership deck, field update) |
| B. Cycles per year | ____ | ____ | How often it happens |
| C. Loaded hourly rate | $____ /h | $____ /h | Salary + benefits + overhead; agree one number as a team |
| D. Hours saved per year | | **(A today − A AI) × B = ____ h** | |
| E. Value per year | | **D × C = $____** | Estimate, not a measured result |
| F. Other benefits | | | Speed (days to decision), coverage (% of HCPs, sessions, records), quality (errors caught) |

> **ILLUSTRATIVE ONLY, not data:** 60 h → 15 h per cycle × 4 cycles/year = 180 h saved; × $150/h = $27,000 per year. Replace every number with the team's own estimate.

These numbers go on the Impact slide of the final template (slide 9: formula tiles and a bar chart built from the team's own estimates).

---

*All products, people and results in the practice data are fictional. Outputs are drafts that need qualified human review; this is not a clinical decision, GxP or pharmacovigilance system.*
