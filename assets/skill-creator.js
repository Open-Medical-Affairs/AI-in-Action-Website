/* Skill creator (a mode of the optimizer): plain-words workflow -> skill pack in the Medical-Affairs-Skills format.
   POST /api/skills builds the files (AI or template), POST /api/skills/zip returns the zip. */
(function () {
  "use strict";
  var U = window.AIA_OPT_UI, D = window.AIA_OPT, d = document;
  if (!U || !D) return;
  var esc = function (s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); };
  var STARTERS = [
    { label: "Turn congress session notes into an insight brief", kind: "single" },
    { label: "Medical information response pack for a new indication", kind: "group" },
    { label: "Monthly competitor publication watch with a one-page digest", kind: "single" },
    { label: "Advisory board end to end: objectives, pre-read, run sheet and insight report", kind: "group" }
  ];
  var form = U.wrap.querySelector(".aiopt-form"), data = form.querySelector(".aiopt-data");
  var extra = d.createElement("div"); extra.className = "sc-only sc-fields";
  extra.innerHTML =
    '<div class="aiopt-modes sc-kind" role="radiogroup" aria-label="Single skill or a group">' +
      '<button type="button" role="radio" class="aiopt-mode" data-kind="single" aria-checked="true">Single skill</button>' +
      '<button type="button" role="radio" class="aiopt-mode" data-kind="group" aria-checked="false">Skill group <small>lead + workers</small></button></div>' +
    '<label class="fld"><span class="fld-l">Audience or therapy area <span class="aiopt-opt">optional</span></span><input type="text" id="sc-aud" maxlength="200" placeholder="e.g. MSLs in oncology, EU medical leadership"></label>';
  data.parentNode.insertBefore(extra, data);
  var chips = d.createElement("div"); chips.className = "sc-only";
  chips.innerHTML = '<p class="fld-l aiopt-try">Try a starter</p><div class="aiopt-chips">' + STARTERS.map(function (s, i) {
    return '<button type="button" class="aiopt-chip' + (s.kind === "group" ? " aiopt-chip--swarm" : "") + '" data-sc="' + i + '"><span class="aiopt-chip-m">' + (s.kind === "group" ? "Group" : "Skill") + "</span>" + esc(s.label) + "</button>";
  }).join("") + "</div>";
  form.appendChild(chips);
  var out = d.createElement("div"); out.className = "aiopt-out opt-out-in sc-only sc-out";
  out.innerHTML =
    '<div class="prompt-head prompt-head--dark"><span class="prompt-title">Your skill pack</span><span class="opt-meter" id="sc-meta" aria-live="polite"></span></div>' +
    '<div class="sc-actions"><button type="button" class="btn-copy btn-copy--solid sc-zip" id="sc-zip" disabled><span class="lbl">Download skill pack (.zip)</span></button>' +
    '<button type="button" class="btn-copy sc-grok" id="sc-grok"><span class="lbl">Copy prompt for Grok Bot</span></button></div>' +
    '<p class="aiopt-status" id="sc-status" aria-live="polite">Describe a workflow, pick single skill or group, then press Create skill pack. Or copy the Grok Bot prompt and let Grok Bot build the skills itself.</p>' +
    '<div class="sc-tabs" role="tablist" aria-label="Files in the pack" id="sc-tabs"></div>' +
    '<pre class="prompt-text sc-pre" id="sc-pre" tabindex="0" aria-label="File preview"><code>Preview of each SKILL.md appears here.</code></pre>';
  U.wrap.querySelector(".aiopt-in").appendChild(out);

  var kind = "single", pack = null, busy = false, cur = 0;
  var kindBtns = Array.prototype.slice.call(extra.querySelectorAll("[data-kind]"));
  function setKind(k) { kind = k; kindBtns.forEach(function (b) { var on = b.getAttribute("data-kind") === k; b.setAttribute("aria-checked", on ? "true" : "false"); b.tabIndex = on ? 0 : -1; }); }
  kindBtns.forEach(function (b) { b.addEventListener("click", function () { setKind(b.getAttribute("data-kind")); }); });
  chips.addEventListener("click", function (ev) {
    var b = ev.target.closest("[data-sc]"); if (!b || busy) return;
    var s = STARTERS[+b.getAttribute("data-sc")]; U.goal.value = s.label; setKind(s.kind); run();
  });
  var $ = function (id) { return d.getElementById(id); };
  function say(t) { $("sc-status").textContent = t; }
  function dataText() {
    var c = U.dataChoice(), T = D.therapeuticAreas[U.taSel.value];
    if (c === "practice") return "Practice data (fictional Nordvant Biopharma): the " + T.product + " pack, " + T.area + ", at " + D.dataRepo + "/tree/HEAD/synthetic/" + U.taSel.value + "/. Mark outputs SYNTHETIC.";
    if (c === "none") return "No data yet: start from public sources, list the data each skill needs, and ask me before going further.";
    var n = U.note.value.trim();
    return "My own data" + (n ? ": " + n : "") + ". Ask me to attach it or say where it lives, and confirm I am allowed to use it.";
  }
  function grokPrompt() {
    var w = U.goal.value.trim() || "(describe the workflow)", aud = $("sc-aud").value.trim();
    var L = ["Create " + (kind === "group" ? "a group of reusable skills (2-4 worker skills plus one lead/orchestrator skill)" : "one reusable skill") + " for this Medical Affairs workflow: " + w + (aud ? " (audience: " + aud + ")" : "") + ".",
      "",
      "Use the exact format of " + D.skillsRepo + " (default branch). First read AGENTS.md, skills/kol-engagement-brief/SKILL.md" + (kind === "group" ? " and skills/medical-launch-plan/SKILL.md (a lead skill) with its references/digital-workers.md" : "") + ", and house-rules/README.md.",
      "- One folder per skill: skills/<kebab-name>/SKILL.md, plus house-rules/<kebab-name>.md ending with \"## YOUR RULES — ADD BELOW THIS LINE\".",
      "- Frontmatter exactly like the library: name, description (>- folded, with \"Use when ...\" trigger phrases and \"Produces ...\"), license: Apache-2.0, allowed-tools: Read, Write, Edit, Bash, metadata (version \"0.1.0\", tier, maturity: beta, requires, suggests, produces, deliverables).",
      "- requires always lists medical-affairs-foundations; suggests includes deliverable-quality-review. Use only real library skill names or names in this pack.",
      "- Sections: Stage 0 — Safety scan; Stage 1 — Inventory; Stage 2 — Retrieve; Stage 3 — Analyse; Stage 4 — Challenge (deliverable-quality-review); Stage 5 — Deliver; What makes this deliverable fail; Guardrails; Deliverable format; Before you finish (read house-rules/<name>.md)."];
    if (kind === "group") L.push("- The lead skill (tier: orchestrator) requires every worker, and has: The org chart (human final judge at the top), Context engineering (a table of what each worker receives and hands back), Stage 2 — Dispatch in waves (a | Wave | Workers | Why this order | table with **Gate N** rows where a human decides), Integrate, Challenge, and Human decision gates — not negotiable.");
    L.push("- Guardrails in every skill: the human is the final judge; no confidential company data or patient-identifiable information unless I confirm it is authorised; never invent data or citations; never send, post or publish anything.",
      "- Data: " + dataText(),
      "",
      "Save the skill" + (kind === "group" ? "s" : "") + " as reusable skills in your skills library and give me a zip of the folders. Show me each SKILL.md and ask me to review and approve before you use " + (kind === "group" ? "them" : "it") + " on real work.");
    return L.join("\n");
  }
  function showTab(i) {
    cur = i; var f = pack.files.filter(isPreview)[i];
    Array.prototype.forEach.call($("sc-tabs").children, function (b, j) { b.setAttribute("aria-selected", j === i ? "true" : "false"); b.tabIndex = j === i ? 0 : -1; });
    $("sc-pre").querySelector("code").textContent = f.content;
  }
  function isPreview(f) { return /SKILL\.md$|README\.md$/.test(f.path); }
  function render() {
    var fs = pack.files.filter(isPreview);
    $("sc-tabs").innerHTML = fs.map(function (f, i) {
      var label = f.role === "readme" ? "README" : f.skill + (f.role === "lead" ? " · lead" : "");
      return '<button type="button" role="tab" class="sc-tab' + (f.role === "lead" ? " sc-tab--lead" : "") + '" aria-selected="false">' + esc(label) + "</button>";
    }).join("");
    Array.prototype.forEach.call($("sc-tabs").children, function (b, i) { b.addEventListener("click", function () { showTab(i); }); });
    showTab(fs.length > 1 ? 1 : 0);
    var nSk = pack.files.filter(function (f) { return /SKILL\.md$/.test(f.path); }).length;
    $("sc-meta").textContent = nSk + " skill" + (nSk > 1 ? "s" : "") + " · " + (pack.source === "ai" ? "AI" : "template") + " · " + (pack.ms / 1000).toFixed(1) + "s";
    $("sc-zip").disabled = false;
  }
  function run() {
    if (busy) return;
    var w = U.goal.value.trim();
    if (!w) { U.goal.focus(); say("Describe the workflow first, or pick a starter."); return; }
    busy = true; U.wrap.classList.add("is-busy"); U.go.disabled = true; $("sc-zip").disabled = true;
    say(U.isAI() ? "Writing your skill pack… (usually 20–60 seconds)" : "Building your skill pack from the template…");
    if (window.innerWidth < 980) out.scrollIntoView({ behavior: "smooth", block: "start" });
    fetch("/api/skills", { method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ workflow: w, kind: kind, data: U.dataChoice(), ta: U.dataChoice() === "practice" ? U.taSel.value : "own", data_note: U.dataChoice() === "own" ? U.note.value.trim() : "", audience: $("sc-aud").value.trim() }) })
      .then(function (r) { return r.json().then(function (j) { if (!r.ok) throw new Error(j.message || "Error " + r.status); return j; }); })
      .then(function (j) {
        pack = j; render();
        say((j.note ? j.note + " " : "") + (j.source === "ai" ? "Drafted by AI and checked against the library format. " : "") + "Review every file before you use it.");
      })
      .catch(function (e) { say((e && e.message ? e.message + ". " : "") + "Copy the Grok Bot prompt instead; it works without this server."); })
      .then(function () { busy = false; U.wrap.classList.remove("is-busy"); U.go.disabled = false; });
  }
  $("sc-zip").addEventListener("click", function () {
    if (!pack) return;
    var b = this; b.disabled = true;
    fetch("/api/skills/zip", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ pack_name: pack.pack_name, files: pack.files.map(function (f) { return { path: f.path, content: f.content }; }) }) })
      .then(function (r) { if (!r.ok) throw new Error("zip failed"); return r.blob(); })
      .then(function (blob) {
        var a = d.createElement("a"); a.href = URL.createObjectURL(blob); a.download = pack.pack_name + ".zip"; d.body.appendChild(a); a.click();
        setTimeout(function () { URL.revokeObjectURL(a.href); a.remove(); }, 1000); say("Downloaded " + pack.pack_name + ".zip. Unzip it and follow README.md to install.");
      })
      .catch(function () { say("The zip could not be built. Copy each file from the preview instead."); })
      .then(function () { b.disabled = false; });
  });
  $("sc-grok").addEventListener("click", function () {
    var t = grokPrompt(), b = this, l = b.querySelector(".lbl");
    (navigator.clipboard && window.isSecureContext ? navigator.clipboard.writeText(t) : Promise.reject()).then(function () {
      l.textContent = "Copied ✓"; setTimeout(function () { l.textContent = "Copy prompt for Grok Bot"; }, 1800);
      if (!pack) $("sc-pre").querySelector("code").textContent = t;
    }, function () { $("sc-pre").querySelector("code").textContent = t; say("Select the prompt in the preview and copy it."); });
  });
  window.AIA_SKILL = { run: run, prompt: grokPrompt };
})();
