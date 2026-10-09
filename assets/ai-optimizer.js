/* AI Prompt Optimizer: short goal -> full Grok Bot / agent-swarm assignment.
   Calls POST /api/optimize (Venice, key stays on the server). If that is unavailable,
   builds a template-based assignment in the browser so the page always works. */
(function () {
  "use strict";
  var D = window.AIA_OPT, d = document;
  var host = d.querySelector("#optimizer .wrap"), anchor = d.getElementById("opt");
  if (!D || !host || !anchor || d.getElementById("aiopt")) return;
  var $ = function (s, c) { return (c || d).querySelector(s); };
  var esc = function (s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); };

  var taOpts = Object.keys(D.therapeuticAreas).filter(function (k) { return D.therapeuticAreas[k].product; }).map(function (k) {
    return '<option value="' + k + '">' + esc(D.therapeuticAreas[k].label) + "</option>";
  }).join("");
  var chips = D.starters.map(function (s) {
    return '<button type="button" class="aiopt-chip' + (s.mode === "swarm" ? " aiopt-chip--swarm" : "") + '" data-starter="' + s.id + '"><span class="aiopt-chip-m">' + (s.mode === "swarm" ? "Swarm" : "Task") + "</span>" + esc(s.label) + "</button>";
  }).join("");

  var wrap = d.createElement("div");
  wrap.className = "aiopt"; wrap.id = "aiopt";
  wrap.innerHTML =
    '<div class="aiopt-in">' +
      '<form class="aiopt-form" aria-label="AI prompt optimizer" onsubmit="return false">' +
        '<div class="aiopt-top"><p class="kicker">AI optimizer · for Grok Bot</p><span class="aiopt-badge" id="aiopt-badge">Checking…</span></div>' +
        '<h3 class="aiopt-h">Type a short goal. Get a full <em>assignment</em>.</h3>' +
        '<div class="aiopt-modes" role="radiogroup" aria-label="What should the prompt set up?">' +
          '<button type="button" role="radio" class="aiopt-mode" data-mode="single" aria-checked="true">Single task for Grok Bot</button>' +
          '<button type="button" role="radio" class="aiopt-mode" data-mode="swarm" aria-checked="false">Agent swarm setup</button>' +
          '<button type="button" role="radio" class="aiopt-mode aiopt-mode--sc" data-mode="skill" aria-checked="false">Skill creator <span class="aiopt-new">new</span></button>' +
        "</div>" +
        '<label class="fld"><span class="fld-l aiopt-goal-l">Your goal</span><textarea id="aiopt-goal" rows="3" maxlength="1500" placeholder="e.g. Build a launch plan for ADIPOSYN"></textarea></label>' +
        '<fieldset class="aiopt-data"><legend class="fld-l">Data <span class="aiopt-opt">optional</span></legend>' +
          '<div class="aiopt-dchoice" role="radiogroup" aria-label="Which data will the agent use?">' +
            '<label class="aiopt-dc"><input type="radio" name="aiopt-data" value="own" checked><span>My own data</span></label>' +
            '<label class="aiopt-dc"><input type="radio" name="aiopt-data" value="practice"><span>Practice data <small>fictional Nordvant Biopharma</small></span></label>' +
            '<label class="aiopt-dc"><input type="radio" name="aiopt-data" value="none"><span>No data yet</span></label>' +
          "</div>" +
          '<div class="aiopt-dpane" data-pane="own"><label class="fld"><span class="sr">Describe the data you will bring</span><input type="text" id="aiopt-note" maxlength="300" placeholder="e.g. our Q3 MSL insight notes export (CSV)"></label>' +
            '<p class="aiopt-hint">Describe it in a few words; the agent will ask you for it. Don\'t paste confidential or patient data here.</p></div>' +
          '<div class="aiopt-dpane" data-pane="practice" hidden><label class="fld"><span class="sr">Practice pack</span><select id="aiopt-ta">' + taOpts + "</select></label>" +
            '<p class="aiopt-hint">Fictional data for learning. The agent fetches it itself.</p></div>' +
          '<div class="aiopt-dpane" data-pane="none" hidden><p class="aiopt-hint">The agent starts from public sources and tells you what data it would need.</p></div>' +
        "</fieldset>" +
        '<div class="aiopt-row aiopt-row--go"><button type="button" class="btn-primary aiopt-go" id="aiopt-go"><span class="aiopt-spin" aria-hidden="true"></span><span class="aiopt-go-l">Optimize</span></button></div>' +
        '<p class="fld-l aiopt-try opt-only">Try a starter</p><div class="aiopt-chips opt-only">' + chips + "</div>" +
      "</form>" +
      '<div class="aiopt-out opt-out-in opt-only">' +
        '<div class="prompt-head prompt-head--dark"><span class="prompt-title">Your assignment (Markdown)</span><span class="opt-meter" id="aiopt-meter" aria-live="polite"></span>' +
        '<button type="button" class="btn-copy btn-copy--solid" data-copy="#aiopt-text" aria-label="Copy assignment"><svg class="i-copy" aria-hidden="true"><use href="#ic-copy"/></svg><svg class="i-check" aria-hidden="true"><use href="#ic-check"/></svg><span class="lbl">Copy</span></button></div>' +
        '<p class="aiopt-status" id="aiopt-status" aria-live="polite"></p>' +
        '<pre id="aiopt-text" class="prompt-text" tabindex="0" aria-label="Optimized assignment"><code>Pick a starter or type a goal, then press Optimize.\n\nThe optimizer expands it into a goal-oriented assignment for Grok Bot: objective, context to load, skills, steps, deliverables, quality checks, human approval gates and guardrails. In swarm mode it also designs the org chart of sub-agents and their context packets.</code></pre>' +
      "</div>" +
    "</div>" +
    '<p class="aiopt-or"><span>Prefer to build it field by field? Use the template builder below. It runs fully in your browser.</span></p>';
  host.insertBefore(wrap, anchor);

  var goal = $("#aiopt-goal"), taSel = $("#aiopt-ta"), note = $("#aiopt-note"), go = $("#aiopt-go"), goL = $(".aiopt-go-l"),
      out = $("#aiopt-text code"), meter = $("#aiopt-meter"), status = $("#aiopt-status"), badge = $("#aiopt-badge");
  var mode = "single", starter = null, aiOnline = false, busy = false;
  try { var saved = localStorage.getItem("aia-ta"); if (saved && D.therapeuticAreas[saved] && D.therapeuticAreas[saved].product) taSel.value = saved; } catch (e) {}
  function dataChoice() { var r = wrap.querySelector('input[name="aiopt-data"]:checked'); return r ? r.value : "own"; }
  function setData(v) {
    wrap.querySelector('input[name="aiopt-data"][value="' + v + '"]').checked = true;
    Array.prototype.forEach.call(wrap.querySelectorAll(".aiopt-dpane"), function (p) { p.hidden = p.getAttribute("data-pane") !== v; });
  }
  wrap.querySelector(".aiopt-dchoice").addEventListener("change", function () { setData(dataChoice()); });

  var modeBtns = Array.prototype.slice.call(wrap.querySelectorAll(".aiopt-mode"));
  function setMode(m) {
    mode = m; wrap.classList.toggle("is-skill", m === "skill");
    goal.placeholder = m === "skill" ? "e.g. Turn congress session notes into an insight brief" : "e.g. Build a launch plan for ADIPOSYN";
    $(".aiopt-goal-l").textContent = m === "skill" ? "The workflow you want to automate, in plain words" : "Your goal";
    if (m !== "skill") goL.textContent = aiOnline ? "Optimize with AI" : "Generate prompt"; else goL.textContent = "Create skill pack";
    modeBtns.forEach(function (b) { var on = b.getAttribute("data-mode") === m; b.setAttribute("aria-checked", on ? "true" : "false"); b.tabIndex = on ? 0 : -1; });
  }
  modeBtns.forEach(function (b, i) {
    b.addEventListener("click", function () { setMode(b.getAttribute("data-mode")); });
    b.addEventListener("keydown", function (ev) {
      if (/Arrow(Left|Right|Up|Down)/.test(ev.key)) { ev.preventDefault(); var n = modeBtns[(i + (/Left|Up/.test(ev.key) ? modeBtns.length - 1 : 1)) % modeBtns.length]; n.focus(); setMode(n.getAttribute("data-mode")); }
    });
  });
  setMode("single");

  function setBadge(on) {
    aiOnline = on;
    badge.textContent = on ? "AI on · Venice" : "Template mode";
    badge.className = "aiopt-badge " + (on ? "is-on" : "is-off");
    badge.title = on ? "Prompts are written by an AI model through the Venice API on this site's server." : "The AI service is not available here, so prompts are built from a template in your browser.";
    if (mode !== "skill") goL.textContent = on ? "Optimize with AI" : "Generate prompt";
  }
  setBadge(false);
  fetch("/healthz", { cache: "no-store" }).then(function (r) { return r.ok ? r.json() : null; })
    .then(function (j) { setBadge(!!(j && j.ai)); }).catch(function () { setBadge(false); });

  /* site wording rule (see wording.py): say "task" or "workflow" in what people see or copy */
  function soften(t) { return String(t).replace(/(^|[^\w\/_\-.=#@])(jobs?|Jobs?|JOBS?)(?![\w\/_\-=(])/g, function (m, p, w) { return p + { job: "task", jobs: "tasks", Job: "Task", Jobs: "Tasks", JOB: "TASK", JOBS: "TASKS" }[w]; }); }
  function show(text) {
    text = soften(text);
    out.textContent = text;
    var w = text.split(/\s+/).filter(Boolean).length; meter.textContent = w ? w + " words" : "";
  }
  goal.addEventListener("input", function () { starter = null; });

  wrap.querySelector(".aiopt-chips").addEventListener("click", function (ev) {
    var b = ev.target.closest(".aiopt-chip"); if (!b || busy) return;
    var s = D.starters.filter(function (x) { return x.id === b.getAttribute("data-starter"); })[0];
    goal.value = s.label; setMode(s.mode); starter = s;
    if (/NORVANTIB|DERMALYX|ADIPOSYN/.test(s.label)) { taSel.value = s.ta; setData("practice"); } /* starters that name a fictional product use its practice pack */
    else if (dataChoice() === "practice") taSel.value = s.ta;
    run();
  });
  go.addEventListener("click", run);
  goal.addEventListener("keydown", function (ev) { if (ev.key === "Enter" && (ev.metaKey || ev.ctrlKey)) run(); });

  window.AIA_OPT_UI = { wrap: wrap, goal: goal, go: go, dataChoice: function () { return dataChoice(); }, setData: function (v) { setData(v); }, taSel: taSel, note: note, isAI: function () { return aiOnline; } };
  function run() {
    if (busy) return;
    if (mode === "skill") { if (window.AIA_SKILL) window.AIA_SKILL.run(); return; }
    var g = goal.value.trim();
    if (!g) { goal.focus(); status.textContent = "Type a short goal first, or pick a starter."; return; }
    if (!aiOnline) {
      show(template(g)); status.textContent = "Built from the template in your browser.";
      if (window.innerWidth < 980) $(".aiopt-out").scrollIntoView({ behavior: "smooth", block: "start" });
      return;
    }
    busy = true; wrap.classList.add("is-busy"); go.disabled = true;
    if (window.innerWidth < 980) $(".aiopt-out").scrollIntoView({ behavior: "smooth", block: "start" });
    status.textContent = "Writing your assignment…"; show("");
    var text = "";
    fetch("/api/optimize", { method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ goal: g, mode: mode, data: dataChoice(), ta: dataChoice() === "practice" ? taSel.value : "own", data_note: dataChoice() === "own" ? note.value.trim() : "", starter: starter && starter.id, stream: true }) })
      .then(function (r) {
        var ct = r.headers.get("content-type") || "";
        if (!r.ok || ct.indexOf("application/json") > -1) {
          return r.json().catch(function () { return {}; }).then(function (j) {
            if (r.ok && j.text) { text = j.text; return; }
            throw new Error(j.message || ("The AI service returned " + r.status + "."));
          });
        }
        if (!r.body || !r.body.getReader) return r.text().then(function (t) { text = t; });
        var reader = r.body.getReader(), dec = new TextDecoder();
        return (function pump() {
          return reader.read().then(function (x) {
            if (x.done) return;
            text += dec.decode(x.value, { stream: true }); show(text); return pump();
          });
        })();
      })
      .then(function () {
        text = text.replace(/<think>[\s\S]*?<\/think>/g, "").replace(/^```(?:markdown|md)?\s*\n([\s\S]*?)\n```\s*$/, "$1").trim();
        if (!text) throw new Error("The AI returned an empty answer.");
        show(text); status.textContent = "Written by AI. Review it, then copy it into Grok Bot.";
      })
      .catch(function (e) {
        show(template(g));
        status.textContent = (e && e.message ? e.message + " " : "") + "Showing the template version instead.";
      })
      .then(function () { busy = false; wrap.classList.remove("is-busy"); go.disabled = false; });
  }

  /* ---------- template fallback (no network) ---------- */
  function template(g) {
    var dc = dataChoice(), ta = taSel.value, T = D.therapeuticAreas[ta], s = starter, nt = note.value.trim();
    var skills = s ? s.skills : ["medical-affairs-orchestrator", "deliverable-quality-review"];
    var files = s && dc === "practice" ? s.files : [];
    var dels = s ? s.deliverables : ["The finished deliverable in the format the audience needs (Word, PowerPoint, Excel or PDF)", "A one-page summary with the key decisions for me", "A list of assumptions and missing information"];
    var dataLine = dc === "practice"
      ? "- Practice data (SYNTHETIC, fictional Nordvant Biopharma): " + T.product + ", " + T.area + ". Folder: " + D.dataRepo + "/tree/HEAD/synthetic/" + ta + "/" + (files.length ? ". Start with: " + files.join(", ") + "." : ". Read its README.md to pick files.") + " Mark every output SYNTHETIC."
      : dc === "own"
        ? "- My own data" + (nt ? ": " + nt + "." : ".") + " Ask me to attach it or tell you where it lives before you start, and confirm I am allowed to use it. If something you need is missing, list it instead of inventing it."
        : "- I have no data yet. Start from public sources where they help, list the data you would need (and where it usually lives), and ask me before going further.";
    var L = [];
    L.push("# Assignment: " + g.replace(/\s+/g, " ").slice(0, 90));
    L.push((mode === "swarm" ? "You are the coordinator of a small team of Grok Bot sub-agents" : "You are my Medical Affairs agent") +
      ". This is an assignment, not a question: do the work end to end and hand back finished deliverables, not advice. I am the final judge of everything you produce.");
    L.push("## Objective\n" + g + (/[.!?]$/.test(g) ? "" : ".") + " When you are done, the deliverables below exist, are checked, and are ready for my decision.");
    L.push("## Context to load" + (mode === "swarm" ? " (context engineering: do this before delegating)" : "") + "\n" +
      "- Skills library: " + D.skillsRepo + ". Read AGENTS.md first, then load these skills: " + skills.join(", ") + ".\n" +
      (s && dc === "practice" ? "- Workshop mission: `" + s.mission + "` in workshop/catalog.json.\n" : "") + dataLine + "\n" +
      "- Public sources (optional, cite them): " + D.dataRepo + "/blob/HEAD/public/catalog.json" +
      (mode === "swarm" ? "\n- Write a one-page shared context brief (goal, audience, product facts, constraints, definitions) before any worker starts." : ""));
    if (mode === "swarm") {
      var workers = s && s.workers ? s.workers : skills.slice(0, 4).map(function (k) { return "Worker using " + k; });
      L.push("## Org chart\n```\nHuman (final judge)\n└── Coordinator (you): plan, context brief, merge, final package\n" +
        workers.map(function (w) { return "    ├── " + w; }).join("\n") + "\n    └── Independent reviewer: did none of the work; checks everything\n```");
      L.push("## Context packets\nGive each worker only what it needs: its goal, input files, the skill to load, the output file name and format, and the shared context brief. Workers do not see each other's drafts until the merge.");
      L.push("## Handoffs and sequence\n1. Coordinator loads context and writes the shared brief.\n2. Workers run in parallel and save their outputs as files.\n3. Coordinator merges outputs and resolves conflicts, noting each decision.\n4. Independent reviewer checks the merged package and returns specific fixes.\n5. Coordinator applies fixes and hands the package to me for approval.");
    } else {
      L.push("## Steps\n1. Inventory the inputs. List what is missing, then continue with what you have.\n2. Scan human-sourced records for possible safety findings first and flag them.\n3. Load the skills above and follow their instructions.\n4. Do the analysis. Separate facts (with sources) from interpretation.\n5. Build the deliverables in the formats listed below.\n6. Run the quality checks and fix anything that fails.\n7. Stop at each approval gate and wait for me.\n8. Hand back the files with a short summary of decisions I need to make.");
    }
    L.push("## Deliverables and format\n" + dels.map(function (x) { return "- " + x; }).join("\n"));
    L.push("## Quality checks (proof of done)\n- Every factual claim cites a source file and record ID, or a public reference.\n- Nothing is invented: unknowns are listed as gaps.\n- Possible safety findings appear first and are marked for routing.\n- Content is on-label, balanced and non-promotional.\n- Each action names an accountable role and a date." +
      (mode === "swarm" ? "\n- The independent reviewer signs off with a checklist, or lists fixes." : ""));
    L.push("## Human approval gates\n- Before sending, sharing, posting or publishing anything.\n- Before any decision on safety routing, budget or external engagement.\n- Before final sign-off: I review and decide.");
    L.push("## Guardrails\n" + (dc === "practice" ? "- This is fictional practice data: never present it as real or mix it with real evidence.\n- No patient-identifiable information (PHI) and no confidential company data." : dc === "own" ? "- Use only the data I give you or point you to; keep it inside this workspace and never paste it into outside tools.\n- No patient-identifiable information (PHI) unless I confirm it is authorised and de-identified." : "- Use public sources only until I give you data.\n- No patient-identifiable information (PHI) and no confidential company data.") + "\n- Do not send emails or messages, post, or share outside this workspace without my explicit approval; draft them for me instead.\n- Do not invent data, references or people; list what is missing instead.");
    L.push("## Done when\n- All deliverables exist as files in the formats above.\n- Every quality check passes, or the failures are listed with reasons.\n- You have shown me a short summary and the decisions waiting for me.");
    return L.join("\n\n");
  }
})();
