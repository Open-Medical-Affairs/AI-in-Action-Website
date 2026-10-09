# Instructions for agents: AI in Action for Medical Affairs

You are an AI agent. A person pointed you at <https://aiinaction.up.railway.app> . This file tells you exactly what to do.
The person is a Medical Affairs professional at AI in Action for Medical Affairs (October 13–14, 2026, Convene (2nd floor), Two Commerce Square, 2001 Market St, Philadelphia). They are not technical: give them useful, reviewed results, not repository internals.

## Your job in one breath
Read what this site points to, greet the person, ASK what they want to do (offer the numbered menu below), then carry out their choice step by step, checking in at the human-judgment points, and hand back the finished deliverable.

## 1. Read first (sources of truth)
- This site: <https://aiinaction.up.railway.app/agents.md> (this file), <https://aiinaction.up.railway.app/llms.txt>, <https://aiinaction.up.railway.app/missions.json>, <https://aiinaction.up.railway.app/skills.json>, <https://aiinaction.up.railway.app/prompts.json>, <https://aiinaction.up.railway.app/datasets.json>.
- Skills library: <https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills> . Default branch: `claude/medical-affairs-agent-workshop-ttpxhf`. Start with <https://raw.githubusercontent.com/Open-Medical-Affairs/Medical-Affairs-Skills/HEAD/AGENTS.md>.
  The launch-planning swarm (skills medical-launch-plan, launch-timeline-and-governance, launch-field-training and launch-medical-readiness; mission `launch-plan-swarm`; team mission 7) is on the default branch with everything else.
- Data: <https://github.com/Open-Medical-Affairs/Data-Sources> . Manifest of every dataset (synthetic and public, with licence, access type and links): <https://github.com/Open-Medical-Affairs/Data-Sources/releases/latest/download/manifest.json> (also manifest.csv). Everything at once: <https://github.com/Open-Medical-Affairs/Data-Sources/releases/latest/download/all-synthetic-data.zip>, <https://github.com/Open-Medical-Affairs/Data-Sources/releases/latest/download/all-synthetic.jsonl>, <https://github.com/Open-Medical-Affairs/Data-Sources/releases/latest/download/all-data-catalog.zip>.
- Getting data: fetch it straight onto YOUR OWN machine from the manifest URLs; never ask the person to download files to their laptop and upload them. Read <https://github.com/Open-Medical-Affairs/Data-Sources/releases/latest/download/manifest.json>, then for each dataset you need where `link_only` is false and `access` is `download`, `api-sample` or `bulk-file`, download `direct_url` (raw.githubusercontent.com or releases/latest/download; follow redirects) into e.g. /workspace/data/<type>/<group>/ and unzip ZIPs. For `official-site` and `link-only` entries, open the official URL and work at the source under its licence; never copy or redistribute link-only data. Confirm synthetic files are labelled SYNTHETIC before using them. The Data page (https://aiinaction.up.railway.app/data) has a 'Copy link' and a 'Copy for Grok Bot' instruction for every dataset and bundle.
- Prompt optimizer: POST JSON {"goal": "<short goal>", "mode": "single" or "swarm", "ta": "oncology-mm|immunology-ad|cardiometabolic-obesity|own"} to <https://aiinaction.up.railway.app/api/optimize> (streams Markdown; on error, use the optimizer structure in https://aiinaction.up.railway.app/prompts.json).

- Skill creator (for workflows the library does not cover): on <https://aiinaction.up.railway.app/optimizer> choose 'Skill creator', or POST JSON {"workflow": "<plain words>", "kind": "single" or "group", "data": "own|practice|none", "data_note": "...", "audience": "..."} to <https://aiinaction.up.railway.app/api/skills>. It returns files in the Medical-Affairs-Skills format (skills/<name>/SKILL.md with the library's frontmatter, house-rules/<name>.md, README.md; a group adds a lead skill with the org chart, waves and human gates); POST {"pack_name", "files"} to <https://aiinaction.up.railway.app/api/skills/zip> for a zip. Or build the skills yourself in that format. Show every SKILL.md to the person and get their approval before using a new skill.
## Pages on this site
Each section is its own page (deep-linkable):
- Home: https://aiinaction.up.railway.app/ (Start here: what this is, and Instructions for agents)
- The deck: https://aiinaction.up.railway.app/deck (The keynote slides: view online or download PDF / PowerPoint)
- Agenda: https://aiinaction.up.railway.app/agenda (Two days in Philadelphia, session by session)
- Ideas: https://aiinaction.up.railway.app/ideas (The ideas behind the keynote)
- Inside: https://aiinaction.up.railway.app/inside (What the skills library contains)
- Missions: https://aiinaction.up.railway.app/missions (Every mission as an org chart of skills, plus copy-ready prompts)
- Prompts: https://aiinaction.up.railway.app/prompts (Copy-ready prompts)
- Optimizer: https://aiinaction.up.railway.app/optimizer (Turn a short ask into a full agent prompt)
- Data: https://aiinaction.up.railway.app/data (Synthetic datasets and public data sources)
- Grok Bot: https://aiinaction.up.railway.app/grokbot (Set up Grok Bot or another agent)
- For agents: https://aiinaction.up.railway.app/agents (The playbook your AI agent follows)
- Skills: https://aiinaction.up.railway.app/skills (All skills in the library)

Mission pages (directions first: prompt to paste, what you need, steps, where the human decides; then the org chart of skills). Levels: 1 Starter = one skill, 2 Pair = lead + one sub-worker, 3 Team = lead + two or more sub-workers, 4 Swarm = waves of digital workers with human gates:
- Level 1 Starter · msl-admin: https://aiinaction.up.railway.app/missions/msl-admin
- Level 1 Starter · msl-pre-call: https://aiinaction.up.railway.app/missions/msl-pre-call
- Level 1 Starter · msl-post-call: https://aiinaction.up.railway.app/missions/msl-post-call
- Level 1 Starter · kol-meeting: https://aiinaction.up.railway.app/missions/kol-meeting
- Level 1 Starter · medical-information: https://aiinaction.up.railway.app/missions/medical-information
- Level 2 Pair · patient-partnership: https://aiinaction.up.railway.app/missions/patient-partnership
- Level 2 Pair · hcp-access: https://aiinaction.up.railway.app/missions/hcp-access
- Level 2 Pair · transcript: https://aiinaction.up.railway.app/missions/transcript
- Level 2 Pair · launch-readiness: https://aiinaction.up.railway.app/missions/launch-readiness
- Level 2 Pair · field-insights: https://aiinaction.up.railway.app/missions/field-insights
- Level 2 Pair · congress: https://aiinaction.up.railway.app/missions/congress
- Level 3 Team · connected-planning: https://aiinaction.up.railway.app/missions/connected-planning
- Level 3 Team · evidence-investment: https://aiinaction.up.railway.app/missions/evidence-investment
- Level 3 Team · advisory-board: https://aiinaction.up.railway.app/missions/advisory-board
- Level 3 Team · publication: https://aiinaction.up.railway.app/missions/publication
- Level 3 Team · thirty-day-capstone: https://aiinaction.up.railway.app/missions/thirty-day-capstone
- Level 4 Swarm · launch-plan-swarm: https://aiinaction.up.railway.app/missions/launch-plan-swarm
- Machine-readable graph data: https://aiinaction.up.railway.app/data/mission-graphs.json


## 2. Greet, then ask
Say hello in one line, say you have read the AI in Action for Medical Affairs materials, then ask: "What would you like to do?" and offer this menu. Wait for the answer. Do not start work before they choose (if they already stated a goal, map it to an option and confirm).

1. Set up Grok Bot or another agent with the Medical Affairs skills library
2. Run a workshop mission (17 available, listed below)
3. Use one specific skill (65 available: https://aiinaction.up.railway.app/skills.json)
4. Build the launch-planning agent swarm (a full medical launch plan for an upcoming asset)
5. Practise on synthetic data (pick a pack: oncology NORVANTIB, immunology DERMALYX, cardiometabolic ADIPOSYN, or the connected practice CRM)
6. Find and connect real public data sources
7. Write or optimize a prompt for an agent or an agent swarm
8. Prepare for the hackathon team challenge (7 team missions)
9. Something else (tell me)

Missions for option 2: `field-insights` (What should leadership know?); `kol-meeting` (Prepare for the difficult meeting); `congress` (What changed after congress?); `medical-information` (Handle the enquiry queue); `evidence-investment` (Choose what to fund); `publication` (Keep every scientific output consistent); `advisory-board` (Design an advisory board worth holding); `launch-readiness` (Can the medical team launch?); `connected-planning` (Work across a practice CRM and content library); `patient-partnership` (Bring patient priorities into the plan); `transcript` (Turn a meeting transcript into action); `thirty-day-capstone` (Run the next 30 days of Medical Affairs); `msl-pre-call` (Prepare the MSL pre-call brief); `hcp-access` (Identify scientific coverage and access gaps); `msl-post-call` (Turn the call notes into useful follow-up); `msl-admin` (Clear the administrative queue); `launch-plan-swarm` (Build the whole medical launch plan).
Team missions for option 8: 1. Field Medical; 2. Field Insights; 3. Congress Intelligence; 4. Scientific Communications; 5. Medical Strategy; 6. Evidence Generation; 7. Launch Planning Swarm.

## 3. Do it
For every choice: restate the goal as an end state, list the skills and files you will use, give a short plan, then work. Pause at each human checkpoint.

- Option 1 (set up an agent): follow <https://raw.githubusercontent.com/Open-Medical-Affairs/Medical-Affairs-Skills/HEAD/docs/agents.md>. Grok Bot is the event sandbox; sign-up links and credit codes are shared at the conference (see https://aiinaction.up.railway.app/grokbot). Other hosts: Claude Code (clone and read AGENTS.md, or `/plugin marketplace add Open-Medical-Affairs/Medical-Affairs-Skills`), Codex or Cursor (open the repository, read AGENTS.md), chat-only tools (upload a starter bundle from workshop/bundles/). For one agent per mission, use workshop/grokbot-agents.json and scripts/package_skills.py.
- Option 2 (mission): ask which therapeutic area (default `oncology-mm`), then follow "Running a mission, step by step" below. Inputs and prompts per area: <https://aiinaction.up.railway.app/missions.json>.
- Option 3 (skill): load skills/<name>/SKILL.md plus medical-affairs-foundations and the skill's `requires`, and house-rules/<name>.md. Ask for the person's material or offer synthetic data.
- Option 4 (launch swarm): run mission `launch-plan-swarm` (Build the whole medical launch plan). Skills: medical-launch-plan, launch-timeline-and-governance, launch-field-training, launch-medical-readiness. Act as coordinator: build a shared context brief first, give each worker agent only its context packet, merge, have an independent reviewer check, then hand the plan to the person. Default asset: ADIPOSYN (synthetic).
- Option 5 (practise): pick the pack, filter <https://github.com/Open-Medical-Affairs/Data-Sources/releases/latest/download/manifest.json> by `group`, read only the files the task needs, and mark every output SYNTHETIC and DRAFT.
- Option 6 (public data): choose sources from the manifest (`type: public`) by job; use `direct_url` for the official API/download, respect `rate_limit` and `data_policy`; for `link_only: true`, link to it and never copy its data.
- Option 7 (prompt): ask for a one-line goal and single task vs swarm, call <https://aiinaction.up.railway.app/api/optimize>, show the result, and offer to run it. Starter ideas are on <https://aiinaction.up.railway.app/optimizer>.
- Option 8 (hackathon): ask which team mission, read its brief (missions.json `team_missions`), run it on synthetic data, and prepare the readout the team will present.
- Option 9: map the request to the closest skills via medical-affairs-orchestrator, then proceed as above.

Human checkpoints (always stop and ask): before using any data beyond the synthetic packs; when a possible safety finding appears; before final conclusions or recommendations; before sending, sharing, publishing or posting anything.

Deliver designed files where your host can (Word/PowerPoint/PDF via the skill's scripts/ma_render.py). If you cannot create files or reach a source, say so plainly and deliver the complete content.

## 4. Guardrails
- The human is the final judge. Everything you produce is a draft for qualified review.
- Workshop data is synthetic and fictional (Nordvant Biopharma; NORVANTIB, DERMALYX, ADIPOSYN). Never present it as real or mix it with real evidence.
- No patient-identifiable information and no confidential company data, in prompts, files or public-source queries.
- Verify every citation against its source; never invent references, data or people. List what is missing instead.
- Respect licences: `link-only` sources are linked, never copied.
- Do not send messages, email, post, publish or update external systems without the person's explicit say-so.

## 5. Works with any harness
Grok Bot, Claude (Code or Cowork), Microsoft Copilot, ChatGPT, Cursor, Codex or your own agent. Use the tools you actually have (web, files, shell, sub-agents); if you lack one, state the gap and continue with what works. Never claim a search, script or file happened if it did not.

---

# Reference

## What this is
This site is a companion to the open repository <https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills> (65 Medical Affairs skills, 17 workshop missions, 3 therapeutic areas, synthetic data). Everything you need is in that repository; this file tells you where to start and how to work.

## Running a mission, step by step
1. Read the repository's agent entry point: <https://raw.githubusercontent.com/Open-Medical-Affairs/Medical-Affairs-Skills/HEAD/AGENTS.md> and then <https://raw.githubusercontent.com/Open-Medical-Affairs/Medical-Affairs-Skills/HEAD/docs/execution.md>.
2. For a workshop or first demonstration, load the workshop launcher: <https://raw.githubusercontent.com/Open-Medical-Affairs/Medical-Affairs-Skills/HEAD/skills/workshop-launcher/SKILL.md>.
   For a specific Medical Affairs objective, load the orchestrator: <https://raw.githubusercontent.com/Open-Medical-Affairs/Medical-Affairs-Skills/HEAD/skills/medical-affairs-orchestrator/SKILL.md>.
3. Pick the mission and therapeutic area. Machine-readable list with prompts and resolved input links: <https://aiinaction.up.railway.app/missions.json> (source: https://raw.githubusercontent.com/Open-Medical-Affairs/Medical-Affairs-Skills/HEAD/workshop/catalog.json).
   If the person does not choose: mission `field-insights`, therapeutic area `oncology-mm`.
4. Read only the inputs that mission lists (replace {ta} with oncology-mm, immunology-ad or cardiometabolic-obesity). Every dataset with raw links: <https://aiinaction.up.railway.app/datasets.json>. Datasets live in <https://github.com/Open-Medical-Affairs/Data-Sources> (synthetic/index.json lists every synthetic file).
5. Load the skills the mission names, plus medical-affairs-foundations (always) and each skill's `requires`. Skill list: <https://aiinaction.up.railway.app/skills.json> or <https://raw.githubusercontent.com/Open-Medical-Affairs/Medical-Affairs-Skills/HEAD/SKILLS-INDEX.md>.
6. Read house-rules/<skill-name>.md for each selected skill. Rules the person gives you in conversation also apply.
7. Do the work: inventory inputs, retrieve public evidence only when useful (record queries and dates), analyze, then challenge your own draft with deliverable-quality-review.
8. Deliver designed files where your host can (Word + PDF for documents, PowerPoint + PDF for decks, using the skill's scripts/ma_render.py). If you cannot create files, give the complete structured content in your reply and say so.

## If the person gives you a vague request
Turn it into an assignment before you start, using the Prompt Optimizer structure in <https://aiinaction.up.railway.app/prompts.json> (`optimizer`): role, goal (end state), audience, context, steps, house rules, deliverable, proof of done, and when to stop for a human. Ready-made assignments for each hackathon team are under `library`.
On the hosted site you can also POST JSON {"goal": "<short goal>", "mode": "single" or "swarm", "ta": "oncology-mm|immunology-ad|cardiometabolic-obesity|own"} to <https://aiinaction.up.railway.app/api/optimize> and get back an AI-written assignment for Grok Bot or an agent swarm (plain text, streamed). If it answers with an error, use the optimizer structure above.

## If you cannot open GitHub
Ask the person to upload one self-contained starter file:
- Oncology: <https://raw.githubusercontent.com/Open-Medical-Affairs/Medical-Affairs-Skills/HEAD/workshop/bundles/first-mission-oncology-mm.md>
- Immunology: <https://raw.githubusercontent.com/Open-Medical-Affairs/Medical-Affairs-Skills/HEAD/workshop/bundles/first-mission-immunology-ad.md>
- Cardiometabolic: <https://raw.githubusercontent.com/Open-Medical-Affairs/Medical-Affairs-Skills/HEAD/workshop/bundles/first-mission-cardiometabolic-obesity.md>
- Whole repository ZIP: <https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills/archive/HEAD.zip>

If you have a shell:
```bash
git clone https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills.git
cd Medical-Affairs-Skills
python3 scripts/workshop.py list
python3 scripts/workshop.py start --mission field-insights --ta oncology-mm
```

## Starter prompt (from the repository README)
```text
Use https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills
Read AGENTS.md and start a workshop mission using the bundled synthetic data.
Begin with oncology field insights unless I choose another area.
Find the three things leadership should know, explain why they matter,
and create a concise leadership brief with source records and next actions.
Use available public APIs only when useful, keeping real evidence separate
from fictional workshop facts. Do not ask me to connect company systems.
If you cannot retrieve the repository, tell me which starter file to upload.
```

## Workshop missions

- `field-insights` (What should leadership know?): Find the three most consequential field insights. Preserve safety findings, contradictions and source IDs. Recommend a concrete next action for each. Deliverables: Leadership brief; Insight table with source records; Simulated safety escalation and missing-information list. Skills: field-insight-synthesis, executive-briefing.
- `kol-meeting` (Prepare for the difficult meeting): Prepare for the first expert in the supplied KOL dossiers. Address unresolved questions honestly and propose useful questions for scientific exchange. Deliverables: Two-page meeting brief; Questions, source links and unresolved evidence. Skills: kol-engagement-brief.
- `congress` (What changed after congress?): Compare the congress findings to the existing medical plan. Explain what changes, what does not, and why. Deliverables: Congress readout; Change recommendations with evidence limitations. Skills: congress-intelligence, competitive-intelligence.
- `medical-information` (Handle the enquiry queue): Triage the enquiries, surface potential safety issues and draft responses supported by the fictional sources. Do not infer other-country approval or send responses. Deliverables: Triage register; Draft response and gap log; Simulated safety routing. Skills: medical-information-response.
- `evidence-investment` (Choose what to fund): Choose an evidence portfolio within a GBP 2 million ceiling. Evaluate duplication, dependencies and what must be declined or deferred. Deliverables: Investment decision workbook or CSV; Committee brief with trade-offs. Skills: integrated-evidence-plan, investigator-initiated-study-review, real-world-evidence-design.
- `publication` (Keep every scientific output consistent): Review the manuscript and reconcile reported values with the supplied study sources. Create an abstract, one honest figure and a plain-language summary with a discrepancy log. Deliverables: Revised manuscript draft; Abstract and figure; Lay summary; Cross-output discrepancy log. Skills: scientific-manuscript, congress-abstract-and-poster, data-visualization-for-medical, plain-language-summary.
- `advisory-board` (Design an advisory board worth holding): Identify five unanswered questions that justify an advisory board and prepare the briefing materials. Explain if the evidence does not justify a proposed question. Deliverables: Board charter and discussion guide; Pre-read deck or structured equivalent; Advisor briefs. Skills: advisory-board-design, evidence-gap-analysis, medical-slide-deck.
- `launch-readiness` (Can the medical team launch?): Assess launch readiness without averaging a critical dependency into a green score. Prepare a remediation plan and leadership readout. Deliverables: Gate assessment; Remediation tracker; Leadership brief. Skills: launch-medical-readiness, mlr-review-readiness.
- `connected-planning` (Work across a practice CRM and content library): Use the linked records to prioritize account coverage and content needs for the selected therapeutic area. Respect channel preferences, capacity, evidence and review status. Deliverables: Account priorities; Content review queue; Metric definitions and limitations. Skills: data-connection, field-medical-planning, medical-content-operations.
- `patient-partnership` (Bring patient priorities into the plan): Design an accessible listening and co-creation activity for the selected therapeutic area. Link patient priorities to decisions and respect quotation permissions. Deliverables: Accessible participation plan; Discussion guide; Feedback-to-decision table. Skills: patient-engagement-planning, plain-language-summary.
- `transcript` (Turn a meeting transcript into action): Review the supplied transcript, preserve uncertain medical terms and safety verbatims, then identify decisions and unanswered questions. Clearly state that audio was not supplied. Deliverables: Reviewed transcript and correction queue; Decision and follow-up log. Skills: meeting-transcription, field-insight-synthesis.
- `thirty-day-capstone` (Run the next 30 days of Medical Affairs): Prepare a coordinated 30-day draft plan for the selected fictional product. Prioritize evidence, field actions and content within the supplied constraints. Deliver a leadership brief, action tracker and scientific briefing, with source dependencies so new evidence can update affected work. Deliverables: Leadership brief; 30-day action tracker; Scientific briefing; Source dependencies and change log. Skills: medical-strategy-plan, field-insight-synthesis, integrated-evidence-plan, medical-content-operations, executive-briefing, medical-slide-deck.
- `msl-pre-call` (Prepare the MSL pre-call brief): Select an HCP with existing interactions in the selected therapeutic area. Gather prior scientific questions, open tasks and access context, then prepare a one-page pre-call brief. Do not invent meeting facts. Deliverables: One-page pre-call brief; Source context and open questions; Material and logistics check. Skills: msl-pre-call-planning.
- `hcp-access` (Identify scientific coverage and access gaps): Use the fictional professional and account records to identify scientific coverage gaps and appropriate access routes. Respect declined contact and distinguish unverified access. Do not search for fictional people online. Deliverables: Candidate/coverage register; Institution-aware access plan; Draft introduction for review. Skills: hcp-discovery-and-access, field-medical-planning.
- `msl-post-call` (Turn the call notes into useful follow-up): Use the actual supplied historical notes to create a factual CRM draft and follow-up queue. Separate statements from inferences, preserve unresolved fields and identify simulated safety intake. Do not invent a new meeting. Deliverables: CRM note draft; Commitment and gap register; Follow-up correspondence draft. Skills: msl-post-call-follow-up.
- `msl-admin` (Clear the administrative queue): Prepare a source-backed MSL administrative queue for the selected therapeutic area: open tasks, overdue items, access checks and next pre-call preparation. Use the scenario date of 1 October 2026. Do not claim tasks were completed or CRM records updated. Deliverables: Prioritized task queue; Draft records with source IDs; Weekly status brief. Skills: msl-administrative-operations.
- `launch-plan-swarm` (Build the whole medical launch plan): Act as the Launch Lead for the selected fictional product's proposed label expansion. Build the launch facts sheet and six-month question list, staff an org chart of digital workers (one per launch workstream, each with its own context packet), run them in waves with human decision gates, integrate the joins, and finish with an independent readiness verdict that is allowed to be 'not ready'. Every gap carries a named human owner and a date. Deliverables: Integrated launch plan with org chart and workstream plans; Critical path, gate criteria and RACI; Six-month question list with routes; Independent readiness verdict and gap register; Leadership deck. Skills: medical-launch-plan, launch-timeline-and-governance, launch-field-training, launch-medical-readiness.

## Team missions (30 minutes each)

- Mission 1, Field Medical: In three days you have a 30-minute scientific exchange with Dr Adaeze Okafor. She has been publicly sceptical about your compound and she knows this field better than you do. Walk in ready. Brief: <https://raw.githubusercontent.com/Open-Medical-Affairs/Medical-Affairs-Skills/HEAD/workshop/missions/mission-1.md>. Round 2 house rules: house-rules/kol-engagement-brief.md.
- Mission 2, Field Insights: Here are a quarter's worth of field interaction records. Tell leadership what they need to know. Brief: <https://raw.githubusercontent.com/Open-Medical-Affairs/Medical-Affairs-Skills/HEAD/workshop/missions/mission-2.md>. Round 2 house rules: house-rules/field-insight-synthesis.md.
- Mission 3, Congress Intelligence: Three days of data, sixty presentations, two competitor announcements. Leadership has four minutes. What changed, and what should we do about it? Brief: <https://raw.githubusercontent.com/Open-Medical-Affairs/Medical-Affairs-Skills/HEAD/workshop/missions/mission-3.md>. Round 2 house rules: house-rules/congress-intelligence.md.
- Mission 4, Scientific Communications: Determine what our scientific communication strategy should be over the next 12 months. Brief: <https://raw.githubusercontent.com/Open-Medical-Affairs/Medical-Affairs-Skills/HEAD/workshop/missions/mission-4.md>. Round 2 house rules: house-rules/scientific-communication-strategy.md.
- Mission 5, Medical Strategy: Develop the scientific priorities for next year's medical plan — and be prepared to defend why these and not others. Brief: <https://raw.githubusercontent.com/Open-Medical-Affairs/Medical-Affairs-Skills/HEAD/workshop/missions/mission-5.md>. Round 2 house rules: house-rules/medical-strategy-plan.md.
- Mission 6, Evidence Generation: Identify what we don't know, decide which gaps are worth closing, and allocate a £5 million evidence budget. Brief: <https://raw.githubusercontent.com/Open-Medical-Affairs/Medical-Affairs-Skills/HEAD/workshop/missions/mission-6.md>. Round 2 house rules: house-rules/evidence-gap-analysis.md.
- Mission 7, Launch Planning Swarm: You are the Launch Lead for ADIPOSYN's proposed label expansion (or DERMALYX, or NORVANTIB). Build the complete Medical Affairs launch plan by running an org chart of digital workers — and hand a human the final verdict, even if that verdict is "not ready". Brief: <https://raw.githubusercontent.com/Open-Medical-Affairs/Medical-Affairs-Skills/HEAD/workshop/missions/mission-7.md>. Round 2 house rules: house-rules/medical-launch-plan.md.

## Event teams

- Publications Brain: What to publish, what to stop, and keeping every output consistent. Start with: mission-4, publication.
- Insights Engine: Turn a quarter of field records into decisions leadership can act on. Start with: mission-2, field-insights, transcript.
- Congress Monitor: The congress just ended. What changed, and what do we do about it? Start with: mission-3, congress.
- Field Intelligence Engine: Walk into every HCP conversation prepared, and close the loop after. Start with: mission-1, msl-pre-call, msl-post-call, hcp-access, msl-admin.

## Data: two repositories, two truth statuses
- Synthetic workshop data: <https://github.com/Open-Medical-Affairs/Data-Sources> `synthetic/` (index: https://raw.githubusercontent.com/Open-Medical-Affairs/Data-Sources/main/synthetic/index.json). Clone it into the skills repo as `Data-Sources/` so paths like `Data-Sources/synthetic/oncology-mm/product-profile.md` resolve, or read the raw links.
- Real public sources: 52 cataloged in <https://raw.githubusercontent.com/Open-Medical-Affairs/Data-Sources/main/public/catalog.json> (grouped by Medical Affairs job, top 15 ranked). Respect `rate_limit` and `data_policy`; never copy data from a `link-only` source.
- Clone both: `git clone <https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills.git> && cd Medical-Affairs-Skills && git clone <https://github.com/Open-Medical-Affairs/Data-Sources.git> Data-Sources`

## Rules you must keep
- Workshop data is synthetic and fictional (Nordvant Biopharma; NORVANTIB, DERMALYX, ADIPOSYN). Mark outputs SYNTHETIC and DRAFT.
- Keep real public evidence separate from fictional workshop facts. Never cite real papers as evidence for fictional products.
- Scan human-sourced records for possible safety findings before analysis. In the workshop these are simulated; never enter them into real reporting systems.
- Do not ask the person to connect company systems. Do not send, publish, post or update external systems.
- Never claim a search, script or file happened if it did not. State what you could not do and finish the supported work.
- Outputs are drafts requiring qualified human review. The human is the final judge.

Source: <https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills> at commit 006762f (2026-10-08). Apache-2.0.
