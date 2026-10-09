# AI in Action for Medical Affairs: instructions for AI agents

You are helping a Medical Affairs professional at AI in Action for Medical Affairs (October 13–14, 2026, Convene (2nd floor), Two Commerce Square, 2001 Market St, Philadelphia).
They are not technical. Give them a useful, reviewed result, not an explanation of repository internals.

## What this is
This site is a companion to the open repository <https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills> (65 Medical Affairs skills, 17 workshop missions, 3 therapeutic areas, synthetic data). Everything you need is in that repository; this file tells you where to start and how to work.

## Step by step
1. Read the repository's agent entry point: <https://raw.githubusercontent.com/Open-Medical-Affairs/Medical-Affairs-Skills/HEAD/AGENTS.md> and then <https://raw.githubusercontent.com/Open-Medical-Affairs/Medical-Affairs-Skills/HEAD/docs/execution.md>.
2. For a workshop or first demonstration, load the workshop launcher: <https://raw.githubusercontent.com/Open-Medical-Affairs/Medical-Affairs-Skills/HEAD/skills/workshop-launcher/SKILL.md>.
   For a specific Medical Affairs objective, load the orchestrator: <https://raw.githubusercontent.com/Open-Medical-Affairs/Medical-Affairs-Skills/HEAD/skills/medical-affairs-orchestrator/SKILL.md>.
3. Pick the mission and therapeutic area. Machine-readable list with prompts and resolved input links: missions.json (source: https://raw.githubusercontent.com/Open-Medical-Affairs/Medical-Affairs-Skills/HEAD/workshop/catalog.json).
   If the person does not choose: mission `field-insights`, therapeutic area `oncology-mm`.
4. Read only the inputs that mission lists (replace {ta} with oncology-mm, immunology-ad or cardiometabolic-obesity). Every dataset with raw links: datasets.json. Datasets live in <https://github.com/Open-Medical-Affairs/Data-Sources> (synthetic/index.json lists every synthetic file).
5. Load the skills the mission names, plus medical-affairs-foundations (always) and each skill's `requires`. Skill list: skills.json or <https://raw.githubusercontent.com/Open-Medical-Affairs/Medical-Affairs-Skills/HEAD/SKILLS-INDEX.md>.
6. Read house-rules/<skill-name>.md for each selected skill. Rules the person gives you in conversation also apply.
7. Do the work: inventory inputs, retrieve public evidence only when useful (record queries and dates), analyze, then challenge your own draft with deliverable-quality-review.
8. Deliver designed files where your host can (Word + PDF for documents, PowerPoint + PDF for decks, using the skill's scripts/ma_render.py). If you cannot create files, give the complete structured content in your reply and say so.

## If the person gives you a vague request
Turn it into an assignment before you start, using the Prompt Optimizer structure in prompts.json (`optimizer`): role, goal (end state), audience, context, steps, house rules, deliverable, proof of done, and when to stop for a human. Ready-made assignments for each hackathon team are under `library`.
On the hosted site you can also POST JSON {"goal": "<short goal>", "mode": "single" or "swarm", "ta": "oncology-mm|immunology-ad|cardiometabolic-obesity|own"} to api/optimize and get back an AI-written assignment for Grok Bot or an agent swarm (plain text, streamed). If it answers with an error, use the optimizer structure above.

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

Source: <https://github.com/Open-Medical-Affairs/Medical-Affairs-Skills> at commit 635dcf2 (2026-10-08). Apache-2.0.
