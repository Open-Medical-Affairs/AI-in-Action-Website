/* Skill creator: turn a plain-words workflow into a skill pack in the Medical-Affairs-Skills format.
   The model returns structured JSON (content only); this module validates it and renders every file
   itself, so the frontmatter and sections always match the library's conventions. Template fallback included.
   Also: a dependency-free ZIP writer. */
"use strict";
const zlib = require("zlib");
const D = require("../assets/optimizer-data.js");

const KNOWN = new Set(D.skills);
const FOUNDATION = "medical-affairs-foundations";
const REVIEW = "deliverable-quality-review";
const TIERS = new Set(["workflow", "content", "data", "primitive"]);
const FORMATS = ["docx", "pdf", "pptx", "xlsx", "html"];
const REPO = D.skillsRepo;

/* ---------- small text helpers ---------- */
const s = (v, n) => String(v == null ? "" : v).replace(/\r/g, "").trim().slice(0, n || 4000);
const oneLine = (v, n) => s(v, n).replace(/\s+/g, " ");
function kebab(v, fallback) {
  const k = String(v || "").toLowerCase().normalize("NFKD").replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "").replace(/-{2,}/g, "-").slice(0, 48).replace(/-+$/, "");
  return k || fallback || "custom-skill";
}
function titleCase(k) { return k.split("-").map((w) => w.charAt(0).toUpperCase() + w.slice(1)).join(" "); }
function wrap(text, width, indent) {
  const words = oneLine(text).split(" "); const lines = []; let cur = "";
  for (const w of words) { if ((cur + " " + w).trim().length > width) { if (cur) lines.push(cur); cur = w; } else cur = (cur + " " + w).trim(); }
  if (cur) lines.push(cur);
  return lines.map((l) => indent + l).join("\n");
}
function list(v, n, len) { return (Array.isArray(v) ? v : []).map((x) => oneLine(x, len || 300)).filter(Boolean).slice(0, n || 8); }
function yamlScalar(v) { const t = oneLine(v, 200).replace(/"/g, "'"); return /[:#\[\]{}&*!|>%@`,]/.test(t) || /^[-?]/.test(t) ? `"${t}"` : t; }
function md(v, n) { return s(v, n || 2500).replace(/^#{1,2} /gm, "### "); }   // keep model text below our section headings

/* ---------- data choice (same three options as the optimizer) ---------- */
function dataSection(choice, ta, note) {
  const T = D.therapeuticAreas[ta];
  if (choice === "practice" && T && T.product)
    return `Practice data (fictional): the ${T.product} pack, ${T.area}, from the fictional company Nordvant Biopharma. Fetch it from ${D.dataRepo}/tree/HEAD/synthetic/${ta}/ (or the release bundle). Mark every output SYNTHETIC and DRAFT and never present it as real.`;
  if (choice === "none")
    return "No data has been supplied yet. Start from public sources where they help (" + D.dataRepo + "/blob/HEAD/public/catalog.json), list the data this skill needs, where it usually lives and who owns it, and ask the person before going further.";
  const n = oneLine(note, 300);
  return (n ? `The person's own data: ${n}. ` : "The person's own data. ") +
    "Ask them to attach it or say where it lives before you start, and confirm they are allowed to use it here. Use only that data; list anything missing instead of inventing it.";
}

/* ---------- prompt for the model ---------- */
function buildMessages({ workflow, kind, choice, ta, note, audience }) {
  const sys = `You design reusable agent skills for Medical Affairs teams, in the format of the open library ${REPO}.
Return ONLY one JSON object, no prose, no code fences. Write plain, specific, practical English. Never use the words "job" or "jobs"; say "task" or "workflow" instead. Never invent data, references, people or products.
Existing library skills you may list in "requires" or "suggests" (use only these names, or names of skills in this pack): ${D.skills.join(", ")}.
Every skill must:
- run a safety scan first (possible adverse events / product complaints in human-sourced records) via medical-affairs-foundations;
- keep the human as the final judge, with explicit points where a named person decides;
- never use confidential company data or patient-identifiable information unless the person confirms it is authorised; never send, post or publish anything.
JSON shape for a ${kind === "group" ? "GROUP (a lead skill that orchestrates 2-4 worker skills)" : "SINGLE skill"}:
${kind === "group" ? `{
 "pack_name": "kebab-case name for the pack",
 "summary": "one sentence",
 "lead": { "name": "kebab-case", "description": "2-4 sentences: what it does, 'Use when ...' trigger phrases in quotes, 'Produces ...'", "intro": "2 short paragraphs on why this workflow fails today and what the lead owns",
   "produces": "short noun phrase", "deliverables": ["docx","pdf"], "inventory": "markdown bullet list of what to gather",
   "integrate": "markdown: how the lead merges worker outputs and resolves conflicts",
   "waves": [ {"workers": ["worker-name"], "why": "why this order"} ],
   "gates": [ {"after_wave": 1, "who": "Human: what they approve", "why": "why it matters"} ] },
 "workers": [ { "name": "kebab-case", "role": "short role title", "tier": "workflow|content|data", "description": "2-4 sentences incl. 'Use when ...' and 'Produces ...'",
   "intro": "1-2 paragraphs", "requires": [], "suggests": [], "produces": "noun phrase", "deliverables": ["docx","pdf"],
   "context": "exactly what the lead hands this worker", "hands_back": "what it returns to the lead",
   "inventory": "markdown", "retrieve": "markdown", "analyse": "markdown with ### subheadings", "deliver": "markdown",
   "failure_modes": ["..."], "house_rules": ["example organisation rules"] } ]
}` : `{
 "pack_name": "kebab-case",
 "summary": "one sentence",
 "skill": { "name": "kebab-case", "tier": "workflow|content|data", "description": "2-4 sentences incl. 'Use when ...' trigger phrases in quotes and 'Produces ...'",
   "intro": "2 short paragraphs: the task and the standard", "requires": [], "suggests": [], "produces": "noun phrase", "deliverables": ["docx","pdf"],
   "inventory": "markdown", "retrieve": "markdown", "analyse": "markdown with ### subheadings", "deliver": "markdown",
   "failure_modes": ["..."], "house_rules": ["example organisation rules"] }
}`}
Use 2-4 workers for a group, at least one gate between waves, and a final human decision.`;
  const user = [`Workflow to automate, in the person's words:\n"""\n${workflow}\n"""`,
    audience ? `Audience / therapy area: ${audience}` : "",
    `Data: ${dataSection(choice, ta, note)}`,
    "Return the JSON now."].filter(Boolean).join("\n\n");
  return [{ role: "system", content: sys }, { role: "user", content: user }];
}

function parseJson(text) {
  let t = String(text || "").replace(/<think>[\s\S]*?<\/think>/g, "").trim();
  t = t.replace(/^```(?:json)?\s*/i, "").replace(/```\s*$/, "");
  const a = t.indexOf("{"), b = t.lastIndexOf("}");
  if (a < 0 || b < a) throw new Error("no JSON object");
  return JSON.parse(t.slice(a, b + 1));
}

/* ---------- normalise model (or template) output into a validated pack spec ---------- */
function normWorker(w, taken, packNames) {
  let name = kebab(w.name, "custom-worker");
  if (KNOWN.has(name)) name += "-custom";
  while (taken.has(name)) name += "-2";
  taken.add(name);
  const tier = TIERS.has(w.tier) ? w.tier : "workflow";
  return {
    name, role: oneLine(w.role || titleCase(name), 60), tier,
    description: oneLine(w.description, 700) || `Custom Medical Affairs skill: ${titleCase(name)}.`,
    intro: md(w.intro, 1500), produces: oneLine(w.produces, 120) || "Draft deliverable for human review",
    deliverables: list(w.deliverables, 4).map((x) => x.toLowerCase()).filter((x) => FORMATS.includes(x)),
    requires: list(w.requires, 6).map((x) => kebab(x)).filter((x) => KNOWN.has(x) || packNames.has(x)),
    suggests: list(w.suggests, 6).map((x) => kebab(x)).filter((x) => KNOWN.has(x) || packNames.has(x)),
    context: oneLine(w.context, 500), hands_back: oneLine(w.hands_back, 400),
    inventory: md(w.inventory), retrieve: md(w.retrieve), analyse: md(w.analyse, 4000), deliver: md(w.deliver),
    failure_modes: list(w.failure_modes, 6), house_rules: list(w.house_rules, 5)
  };
}

function normalize(raw, kind) {
  const taken = new Set();
  const pack = kebab(raw.pack_name, "custom-skill-pack");
  if (kind !== "group") {
    const sk = normWorker(raw.skill || {}, taken, new Set());
    return { kind: "single", pack, summary: oneLine(raw.summary, 300), skills: [sk] };
  }
  const rawWorkers = (Array.isArray(raw.workers) ? raw.workers : []).slice(0, 4);
  if (rawWorkers.length < 2) throw new Error("group needs at least two workers");
  const packNames = new Set(rawWorkers.map((w) => kebab(w.name)));
  const L = raw.lead || {};
  let leadName = kebab(L.name, pack + "-lead"); if (KNOWN.has(leadName) || packNames.has(leadName)) leadName = pack + "-lead";
  taken.add(leadName);
  const rename = {};
  const workers = rawWorkers.map((w) => { const n = normWorker(w, taken, packNames); rename[kebab(w.name)] = n.name; return n; });
  const wnames = workers.map((w) => w.name);
  workers.forEach((w) => { w.requires = w.requires.map((x) => rename[x] || x).filter((x) => x !== w.name); w.suggests = w.suggests.map((x) => rename[x] || x).filter((x) => x !== w.name); });
  // waves: keep only real worker names; every worker appears once
  const seen = new Set(); let waves = [];
  for (const wv of (Array.isArray(L.waves) ? L.waves : [])) {
    const ws = list(wv.workers, 6).map((x) => rename[kebab(x)] || kebab(x)).filter((x) => wnames.includes(x) && !seen.has(x));
    ws.forEach((x) => seen.add(x));
    if (ws.length) waves.push({ workers: ws, why: oneLine(wv.why, 200) || "Independent of each other" });
  }
  const rest = wnames.filter((x) => !seen.has(x));
  if (rest.length) waves.push({ workers: rest, why: "Uses the outputs above" });
  if (!waves.length) waves = [{ workers: wnames, why: "Independent of each other" }];
  let gates = (Array.isArray(L.gates) ? L.gates : []).map((g) => ({ after: Math.max(1, Math.min(waves.length, Number(g.after_wave) || 1)), who: oneLine(g.who, 160) || "Human: review and approve", why: oneLine(g.why, 200) })).slice(0, 4);
  if (waves.length > 1 && !gates.some((g) => g.after < waves.length)) gates.unshift({ after: 1, who: "Human: approve the first-wave outputs", why: "Nothing downstream should be built on unapproved work" });
  gates = gates.filter((g) => g.after < waves.length);
  const lead = {
    name: leadName, role: "Lead", tier: "orchestrator",
    description: oneLine(L.description, 700) || `Coordinate ${wnames.join(", ")} as one team of digital workers, with a person deciding at every gate.`,
    intro: md(L.intro, 1500), produces: oneLine(L.produces, 120) || "Integrated deliverable with decision log",
    deliverables: list(L.deliverables, 4).map((x) => x.toLowerCase()).filter((x) => FORMATS.includes(x)),
    inventory: md(L.inventory), integrate: md(L.integrate), waves, gates
  };
  return { kind: "group", pack, summary: oneLine(raw.summary, 300), lead, skills: [lead].concat(workers), workers };
}

/* ---------- template fallback (no key, or Venice failed) ---------- */
function templateSpec(workflow, kind) {
  workflow = oneLine(workflow, 300); workflow = workflow.charAt(0).toLowerCase() + workflow.slice(1);
  const base = kebab(oneLine(workflow, 80).split(" ").slice(0, 5).join(" "), "custom-workflow").replace(/-(into|an|a|the|for|of|to|and)$/, "");
  const generic = (name, role, task) => ({
    name, role, tier: "workflow",
    description: `${task} for this workflow: ${oneLine(workflow, 200)}. Use when asked to "${oneLine(workflow, 80).toLowerCase()}". Produces a draft for human review.`,
    intro: `This skill does one task well: ${task.toLowerCase()}. It is a starting point generated from a template; edit it to match how your team works.`,
    produces: `${role} output`, deliverables: ["docx", "pdf"], requires: [], suggests: [],
    context: "The workflow goal, the inventory, and only the inputs this step needs.", hands_back: "A draft file plus open questions and gaps, each with a proposed owner.",
    inventory: "- The request in the person's words, the audience and the deadline\n- Every input file or source, with its kind (record, document, public source)\n- What is missing, listed rather than guessed",
    retrieve: "- Use only the data described under *Data this skill works with*\n- For public evidence, record the exact query and retrieval date\n- Keep public sources and the person's material clearly separate",
    analyse: "### Do the work\nFollow the person's workflow step by step. Separate facts (with a source for each) from interpretation.\n\n### Name the uncertainty\nState confidence for each conclusion and what would change it.",
    deliver: "- Build the deliverable in the formats listed in the frontmatter\n- Put open decisions for the human at the top\n- Mark the output DRAFT",
    failure_modes: ["Claims without a source", "Conclusions the data cannot support", "Missing the decision the reader actually has to make"],
    house_rules: ["Our preferred length and structure for this deliverable", "Who must review it before it is used"]
  });
  if (kind !== "group") return { pack_name: base, summary: oneLine(workflow, 200), skill: generic(base, titleCase(base), "Carry out the workflow end to end") };
  return {
    pack_name: base, summary: oneLine(workflow, 200),
    lead: { name: base + "-lead", description: `Coordinate a small team of skills to ${oneLine(workflow, 200)}, with a person deciding at each gate. Use when asked to "${oneLine(workflow, 80).toLowerCase()}". Produces an integrated deliverable with a decision log.`,
      intro: "The lead owns the joins between the workers: one shared brief, one set of facts, and one place where conflicts are written down.", produces: "Integrated deliverable with decision log", deliverables: ["docx", "pdf"],
      inventory: "- The goal, the audience, the deadline\n- The inputs and who owns them\n- What is missing", integrate: "Merge the workers' outputs, resolve conflicts explicitly in the decision log, and never rewrite a worker's conclusion silently.",
      waves: [{ workers: [base + "-intake", base + "-analysis"], why: "Gather and analyse the inputs" }, { workers: [base + "-drafting"], why: "Draft from the approved analysis" }],
      gates: [{ after_wave: 1, who: "Human: approve the analysis", why: "Nothing should be drafted from an unapproved analysis" }] },
    workers: [generic(base + "-intake", "Intake", "Gather, check and structure the inputs"), generic(base + "-analysis", "Analysis", "Analyse the structured inputs"), generic(base + "-drafting", "Drafting", "Draft the deliverable from the approved analysis")]
  };
}

/* ---------- rendering, in the library's SKILL.md format ---------- */
function frontmatter(sk, requires, suggests) {
  const L = ["---", `name: ${sk.name}`, "description: >-", wrap(sk.description, 76, "  "), "license: Apache-2.0", "allowed-tools: Read, Write, Edit, Bash", "metadata:",
    '  version: "0.1.0"', `  tier: ${sk.tier}`, "  maturity: beta", "  requires:"];
  requires.forEach((r) => L.push(`    - ${r}`));
  if (suggests.length) { L.push("  suggests:"); suggests.forEach((r) => L.push(`    - ${r}`)); }
  L.push(`  produces: ${yamlScalar(sk.produces)}`, `  deliverables: [${(sk.deliverables.length ? sk.deliverables : ["docx", "pdf"]).join(", ")}]`, "---", "");
  return L.join("\n");
}
const GUARDRAILS = (name) => `## Guardrails

- **The human is the final judge.** This skill drafts; a named person reviews and decides before anything is used, approved or acted on.
- **No confidential company data or patient-identifiable information** unless the person confirms it is authorised and de-identified; never paste either into outside tools.
- **Never invent** data, citations, quotes, people or numbers. If no source supports a claim, say so and leave it open.
- **Never send, post, publish, register or change an external system.** Prepare drafts for a person to act on.
- Keep fictional practice data and real evidence clearly separate; mark outputs DRAFT.`;
const FORMAT = (sk) => {
  const f = sk.deliverables.length ? sk.deliverables : ["docx", "pdf"];
  const names = { docx: "Word document (.docx)", pdf: "PDF copy", pptx: "PowerPoint deck (.pptx)", xlsx: "Excel workbook (.xlsx)", html: "HTML report" };
  return `## Deliverable format

Deliver a designed ${f.map((x) => names[x]).join(" plus a ")}. Markdown is for drafting only. If the Medical-Affairs-Skills renderer is available (\`scripts/ma_render.py\` in any library skill), build the files with it and check the preview before handing over. Put a source on every data element and list the open decisions on the first page.`;
};
const BEFORE = (name) => `## Before you finish

Read \`house-rules/${name}.md\`. Rules there override the defaults in this skill. Then confirm: the safety scan ran first, every claim has a source, the output is marked DRAFT, and the person knows exactly what they need to decide.`;

function renderWorker(sk, dataText, leadName) {
  const requires = [FOUNDATION].concat(sk.requires.filter((r) => r !== FOUNDATION));
  const suggests = [REVIEW].concat(sk.suggests.filter((r) => r !== REVIEW && !requires.includes(r)));
  return frontmatter(sk, requires, suggests) + `
# ${titleCase(sk.name)}

${sk.intro || sk.description}
${leadName ? `\nThis skill is a worker in the \`${leadName}\` team. The lead hands it a context packet: ${sk.context || "the shared brief and only the inputs this step needs"}. It hands back: ${sk.hands_back || "its draft file plus assumptions, open questions and gaps, each with a proposed human owner"}.\n` : ""}
## Data this skill works with

${dataText}

## Stage 0 — Safety scan, before anything else

Load \`${FOUNDATION}\` and read its house rules. Scan every human-sourced record for possible adverse events, product complaints or special situations **before** any analysis, and surface findings first. Workshop findings are simulated; real cases follow the organisation's intake procedure.

## Stage 1 — Inventory

${sk.inventory || "- What was asked, by whom, for which audience and deadline\n- The inputs available, and what is missing"}

## Stage 2 — Retrieve

${sk.retrieve || "- Fill real evidence gaps from public sources when useful; record the exact query and retrieval date."}

## Stage 3 — Analyse

${sk.analyse || "Do the work. Separate facts (with sources) from interpretation."}

## Stage 4 — Challenge

Run \`${REVIEW}\` on the actual draft and correct what it finds. Do not invent an error just to show self-critique.

## Stage 5 — Deliver

${sk.deliver || "- Build the deliverable, mark it DRAFT, and hand it to a named person for review."}

Hand the draft to a named person for review. Nothing is final until they decide.

## What makes this deliverable fail

${(sk.failure_modes.length ? sk.failure_modes : ["Claims without a source", "Skipping the safety scan", "No clear decision for the reader"]).map((x) => "- " + x).join("\n")}

${GUARDRAILS(sk.name)}

${FORMAT(sk)}

${BEFORE(sk.name)}
`;
}

function renderLead(spec, dataText) {
  const L = spec.lead, W = spec.workers;
  const requires = [FOUNDATION].concat(W.map((w) => w.name));
  const tree = ["HUMAN (final judge)", "      │", `${L.name.toUpperCase()} (lead — this skill)`, "      │"].concat(W.map((w, i) => `      ${i === W.length - 1 ? "└──" : "├──"} ${w.role}: ${w.name}`)).join("\n");
  const rows = []; const gatesAfter = {};
  L.gates.forEach((g, i) => { (gatesAfter[g.after] = gatesAfter[g.after] || []).push({ n: i + 1, g }); });
  rows.push(`| 0 | Lead | Shared brief, facts sheet, worker roster |`);
  L.waves.forEach((wv, i) => {
    rows.push(`| ${i + 1} | ${wv.workers.map((x) => (W.find((w) => w.name === x) || {}).role || x).join(" · ")} | ${wv.why} |`);
    (gatesAfter[i + 1] || []).forEach(({ n, g }) => rows.push(`| **Gate ${n}** | **${g.who}** | ${g.why} |`));
  });
  rows.push(`| ${L.waves.length + 1} | Independent check | \`${REVIEW}\` on the integrated draft |`);
  rows.push(`| **Gate ${L.gates.length + 1}** | **Human: final decision on the integrated deliverable** | Accept, send back, or accept with named gaps |`);
  const packets = W.map((w) => `| ${w.role} | \`${w.name}\` | ${w.context || "Shared brief + its slice of the inputs"} | ${w.hands_back || "Draft file + gaps with owners"} |`).join("\n");
  return frontmatter(L, requires, [REVIEW]) + `
# ${titleCase(L.name)}

${L.intro || L.description}

## The org chart

\`\`\`
${tree}
\`\`\`

Every worker loads \`${FOUNDATION}\` and its own skill's \`requires\`, and reads \`house-rules/<skill>.md\`. Workers draft; people decide.

## Context engineering — what each worker receives

A sub-agent knows only what it is handed. Build one shared brief (goal, audience, facts, definitions, what is unknown) before anyone starts, then give each worker exactly its packet.

| Worker | Skill | Context it receives | Hands back |
|---|---|---|---|
${packets}

## Data this team works with

${dataText}

## Stage 0 — Orient

Load \`${FOUNDATION}\` and read this skill's house rules. Run the foundations safety scan on any human-sourced records **before** dispatching workers, and surface findings first. Announce the plan: which workers, which waves, which human gates.

## Stage 1 — Inventory

${L.inventory || "- The goal, audience and deadline\n- The inputs and their owners\n- What is missing"}

## Stage 2 — Dispatch in waves

Parallel where independent; sequenced where one output is another's input.

| Wave | Workers | Why this order |
|---|---|---|
${rows.join("\n")}

Report at each wave boundary in two or three lines: what came back, what conflicts, what needs a person.

## Stage 3 — Integrate

${L.integrate || "Merge the outputs, resolve conflicts explicitly in a decision log, and never rewrite a worker's conclusion silently."}

## Stage 4 — Challenge

Run \`${REVIEW}\` on the integrated draft — independently of the workers that wrote it — and correct what it finds.

## Human decision gates — not negotiable

The team drafts; people decide. Nothing moves past a gate until a named person approves, sends it back, or accepts it with named gaps. Agents do not approve, certify, send, register or contact anyone.

${GUARDRAILS(L.name)}

${FORMAT(L)}

${BEFORE(L.name)}
`;
}

function houseRules(sk) {
  return `# House rules — \`${sk.name}\`

Rules here override the defaults in \`skills/${sk.name}/SKILL.md\`.
Write rules that are specific and explain themselves.

## Seeded examples

${(sk.house_rules && sk.house_rules.length ? sk.house_rules : ["Who must review this output before it is used", "Our required length, structure and terminology"]).map((x) => "- " + x).join("\n")}

## YOUR RULES — ADD BELOW THIS LINE
`;
}

function readme(spec, dataText, generatedBy) {
  const lead = spec.kind === "group" ? spec.lead.name : null;
  const rows = spec.skills.map((sk) => `| \`${sk.name}\` | ${sk.name === lead ? "Lead (orchestrator)" : spec.kind === "group" ? "Worker" : "Skill"} | ${oneLine(sk.description, 160)} |`).join("\n");
  return `# ${titleCase(spec.pack)} — skill pack

${spec.summary || ""}

Made with the AI in Action skill creator (${generatedBy}). These are **drafts**: read every SKILL.md and adjust it before anyone relies on it.

| Skill | Role | What it does |
|---|---|---|
${rows}

Data: ${dataText}

## Folder layout (same as Medical-Affairs-Skills)

\`\`\`
skills/<skill-name>/SKILL.md     the skill itself
house-rules/<skill-name>.md      your organisation's overrides
\`\`\`

Every skill loads \`${FOUNDATION}\` from ${REPO}${lead ? `; start the team with \`${lead}\`` : ""}.

## Install

1. **Grok Bot:** upload this zip and say: "Unzip this skill pack, save each skills/<name>/SKILL.md as a reusable skill, load ${FOUNDATION} from ${REPO}, show me each skill, and wait for my review before using them."
2. **With the library:** copy \`skills/*\` into the \`skills/\` folder and \`house-rules/*\` into \`house-rules/\` of your copy of Medical-Affairs-Skills.
3. **Claude Code:** copy each \`skills/<name>\` folder to \`~/.claude/skills/\` (or your project's \`.claude/skills/\`).
4. **Other agents:** upload the SKILL.md files and ask the agent to follow them.

## Before you use it

- A person reviews every skill and every output; the human is the final judge.
- Do not put confidential company data or patient-identifiable information into a tool that is not approved for it.
`;
}

function buildPack(spec, opts) {
  const dataText = dataSection(opts.choice, opts.ta, opts.note);
  const files = [];
  const lead = spec.kind === "group" ? spec.lead.name : null;
  if (lead) files.push({ path: `skills/${lead}/SKILL.md`, content: renderLead(spec, dataText), skill: lead, role: "lead" });
  (spec.kind === "group" ? spec.workers : spec.skills).forEach((w) => files.push({ path: `skills/${w.name}/SKILL.md`, content: renderWorker(w, dataText, lead), skill: w.name, role: lead ? "worker" : "single" }));
  spec.skills.forEach((sk) => files.push({ path: `house-rules/${sk.name}.md`, content: houseRules(sk), skill: sk.name, role: "house-rules" }));
  files.unshift({ path: "README.md", content: readme(spec, dataText, opts.generatedBy), role: "readme" });
  files.forEach((f) => { f.content = soften(f.content); });
  return { pack_name: spec.pack, kind: spec.kind, summary: soften(spec.summary || ""), files };
}

/* Wording rule for the site: no "job"/"jobs" in generated packs (belt and braces after the prompt rule). */
function soften(t) {
  return String(t).replace(/(^|[^\w\/_\-.=#@])(jobs?|Jobs?|JOBS?)(?![\w\/_\-=(])/g, (m, pre, w) => pre + ({ job: "task", jobs: "tasks", Job: "Task", Jobs: "Tasks", JOB: "TASK", JOBS: "TASKS" })[w]);
}

/* ---------- validation of files posted back for zipping ---------- */
const OK_PATH = /^(README\.md|skills\/[a-z0-9][a-z0-9-]{0,60}\/SKILL\.md|house-rules\/[a-z0-9][a-z0-9-]{0,60}\.md)$/;
function checkFiles(files) {
  if (!Array.isArray(files) || !files.length || files.length > 20) throw new Error("bad files");
  let total = 0;
  return files.map((f) => {
    const p = String(f.path || ""), c = String(f.content || "");
    if (!OK_PATH.test(p)) throw new Error("bad path " + p);
    total += c.length; if (total > 400000) throw new Error("too large");
    if (/SKILL\.md$/.test(p) && !/^---\nname: [a-z0-9-]+\ndescription: /.test(c)) throw new Error("bad frontmatter in " + p);
    return { path: p, content: c };
  });
}

/* ---------- minimal ZIP writer (deflate, no dependencies) ---------- */
const CRC = (() => { const t = new Uint32Array(256); for (let n = 0; n < 256; n++) { let c = n; for (let k = 0; k < 8; k++) c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1; t[n] = c >>> 0; } return t; })();
function crc32(buf) { let c = 0xffffffff; for (let i = 0; i < buf.length; i++) c = CRC[(c ^ buf[i]) & 0xff] ^ (c >>> 8); return (c ^ 0xffffffff) >>> 0; }
function zip(entries) {
  const now = new Date();
  const time = (now.getHours() << 11) | (now.getMinutes() << 5) | (now.getSeconds() >> 1);
  const date = ((now.getFullYear() - 1980) << 9) | ((now.getMonth() + 1) << 5) | now.getDate();
  const locals = [], centrals = []; let offset = 0;
  for (const e of entries) {
    const name = Buffer.from(e.path, "utf8"), data = Buffer.from(e.content, "utf8"), comp = zlib.deflateRawSync(data), crc = crc32(data);
    const lh = Buffer.alloc(30);
    lh.writeUInt32LE(0x04034b50, 0); lh.writeUInt16LE(20, 4); lh.writeUInt16LE(0x0800, 6); lh.writeUInt16LE(8, 8); lh.writeUInt16LE(time, 10); lh.writeUInt16LE(date, 12);
    lh.writeUInt32LE(crc, 14); lh.writeUInt32LE(comp.length, 18); lh.writeUInt32LE(data.length, 22); lh.writeUInt16LE(name.length, 26); lh.writeUInt16LE(0, 28);
    const ch = Buffer.alloc(46);
    ch.writeUInt32LE(0x02014b50, 0); ch.writeUInt16LE(20, 4); ch.writeUInt16LE(20, 6); ch.writeUInt16LE(0x0800, 8); ch.writeUInt16LE(8, 10); ch.writeUInt16LE(time, 12); ch.writeUInt16LE(date, 14);
    ch.writeUInt32LE(crc, 16); ch.writeUInt32LE(comp.length, 20); ch.writeUInt32LE(data.length, 24); ch.writeUInt16LE(name.length, 28); ch.writeUInt32LE(0, 30); ch.writeUInt16LE(0, 34); ch.writeUInt32LE((0o100644 * 65536) >>> 0, 38); ch.writeUInt32LE(offset, 42);
    locals.push(lh, name, comp); centrals.push(ch, name);
    offset += lh.length + name.length + comp.length;
  }
  const cd = Buffer.concat(centrals), end = Buffer.alloc(22);
  end.writeUInt32LE(0x06054b50, 0); end.writeUInt16LE(entries.length, 8); end.writeUInt16LE(entries.length, 10); end.writeUInt32LE(cd.length, 12); end.writeUInt32LE(offset, 16);
  return Buffer.concat(locals.concat([cd, end]));
}

module.exports = { soften, buildMessages, parseJson, normalize, templateSpec, buildPack, checkFiles, zip, kebab };
