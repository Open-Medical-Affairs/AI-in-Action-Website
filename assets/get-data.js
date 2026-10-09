/* "Get the data" table, driven by the Data-Sources manifest (data-manifest.json, kept in sync by the server). */
(function () {
  "use strict";
  var d = document, list = d.getElementById("gd-list");
  if (!list) return;
  var q = d.getElementById("gd-q"), count = d.getElementById("gd-count"), more = d.getElementById("gd-more");
  var fBtns = Array.prototype.slice.call(d.querySelectorAll(".gd-f"));
  var rows = [], filter = "all", showAll = false, LIMIT = 30;
  var esc = function (s) { return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); };
  var GROUP = { "oncology-mm": "Oncology · NORVANTIB", "immunology-ad": "Immunology · DERMALYX", "cardiometabolic-obesity": "Cardiometabolic · ADIPOSYN", connected: "Practice CRM", all: "All packs" };
  var DIRECT = { download: 1, "api-sample": 1, "bulk-file": 1 };

  function size(b) { if (!b) return ""; return b > 1048576 ? (b / 1048576).toFixed(1) + " MB" : Math.max(1, Math.round(b / 1024)) + " KB"; }
  function badge(r) {
    if (r.type === "synthetic") return '<span class="badge badge--syn">Synthetic</span>';
    if (r.link_only) return '<span class="badge badge--pub">Public</span><span class="badge badge--lo">Link only</span>';
    return '<span class="badge badge--pub">Public</span>' + (r.data_policy === "check-terms" ? '<span class="badge badge--terms">Check terms</span>' : "");
  }
  /* Copy-first actions: the direct file URL (never a GitHub HTML page) and a ready-to-paste agent instruction. */
  var GITHUB_HTML = /^https:\/\/github\.com\/[^/]+\/[^/]+\/(blob|tree)\//;
  function fileName(r) { var u = String(r.direct_url || "").split("?")[0]; return u.slice(u.lastIndexOf("/") + 1) || r.id; }
  function localPath(r) {
    var m = String(r.direct_url).match(/raw\.githubusercontent\.com\/[^/]+\/[^/]+\/[^/]+\/(.+)$/);
    if (m) return "/workspace/data/" + m[1];
    return "/workspace/data/public/" + r.id + "/" + (r.access === "api-sample" ? r.id + ".json" : fileName(r));
  }
  function grok(r) {
    var u = r.direct_url, lic = r.license ? " (licence: " + r.license + ")" : "";
    if (r.type === "synthetic")
      return "Download " + u + " to your computer (e.g. " + localPath(r) + "), unzip if needed, confirm it is labelled SYNTHETIC (fictional workshop data, not real patients or products), then ask me what I want to do with it.";
    if (r.type === "public-snapshot")
      return "Download " + u + " to your computer (e.g. " + localPath(r) + "). It is a snapshot of real public paper metadata" + lic + ": keep citations exactly as given and verify them before use. Then ask me what I want to do with it.";
    if (r.link_only)
      return "Open " + u + " (" + r.name + "). This source is LINK ONLY" + lic + ": do not download, copy or redistribute its data. Use it only at the official site under its terms, tell me what it offers and how I can access it, then ask me what I want to do.";
    if (r.access === "official-site")
      return "Open the official source " + u + " (" + r.name + ")" + lic + ". There is no single download file: read its access instructions, tell me what data is available and how to get it under its terms, then ask me what I want to do.";
    if (r.access === "api-sample")
      return "Fetch " + u + " (a small sample from the public " + r.name + " API" + lic + ") and save the response to your computer (e.g. " + localPath(r) + "). Check the terms, then ask me what I want to do with it.";
    return "Download " + u + " (" + r.name + ", official public file" + lic + ") to your computer (e.g. " + localPath(r) + "), unzip if needed, check the terms, then ask me what I want to do with it.";
  }
  function actions(r) {
    var direct = (r.access === "download" || r.access === "api-sample" || r.access === "bulk-file") && !r.link_only && !GITHUB_HTML.test(r.direct_url);
    var label = direct ? "Copy link" : r.link_only ? "Copy official link (link only)" : "Copy official link";
    var a = '<button type="button" class="gd-c gd-c--main" data-copy-text="' + esc(r.direct_url) + '" data-done="Link copied"><svg aria-hidden="true"><use href="#ic-copy"/></svg><span>' + label + "</span></button>" +
      '<button type="button" class="gd-c gd-c--grok" data-copy-text="' + esc(grok(r)) + '" data-done="Instruction copied"><span class="gd-c-g" aria-hidden="true">G</span><span>Copy for Grok Bot</span></button>';
    var sec = direct ? '<a class="gd-dl" href="' + esc(r.direct_url) + '"' + (r.access === "download" ? " download" : ' target="_blank" rel="noopener"') + ">download</a>" : "";
    sec += '<a class="gd-dl" href="' + esc(r.view_url) + '" target="_blank" rel="noopener">' + (r.type === "synthetic" ? "view" : "source page") + "</a>";
    return a + '<span class="gd-sec">' + sec + "</span>";
  }
  function match(r, t) {
    if (filter === "synthetic" && r.type !== "synthetic") return false;
    if (filter === "public" && r.type === "synthetic") return false;
    if (filter === "direct" && !DIRECT[r.access]) return false;
    if (filter === "linkonly" && !r.link_only) return false;
    return !t || r._s.indexOf(t) > -1;
  }
  function render() {
    var t = (q.value || "").trim().toLowerCase(), hits = rows.filter(function (r) { return match(r, t); });
    var shown = showAll || t ? hits : hits.slice(0, LIMIT);
    count.textContent = hits.length + " of " + rows.length + " datasets";
    more.hidden = shown.length >= hits.length;
    more.textContent = "Show all " + hits.length;
    if (!hits.length) { list.innerHTML = '<p class="muted gd-empty">No dataset matches. Try another word or filter.</p>'; return; }
    list.innerHTML = '<div class="gd-row gd-row--h" aria-hidden="true"><span>Dataset</span><span>Type</span><span>Licence</span><span>Copy for your agent</span></div>' +
      shown.map(function (r) {
        var meta = [GROUP[r.group] || r.group, r.format, size(r.size_bytes), r.rows ? r.rows + " rows" : ""].filter(Boolean).join(" · ");
        return '<div class="gd-row' + (r.link_only ? " is-lo" : "") + '">' +
          '<div class="gd-name"><strong>' + esc(r.name) + '</strong><span class="gd-meta">' + esc(meta) + "</span>" +
          (r.description ? '<span class="gd-desc">' + esc(r.description) + "</span>" : "") + "</div>" +
          '<div class="gd-type">' + badge(r) + "</div>" +
          '<div class="gd-lic" title="' + esc(r.license) + '">' + esc(r.license) + "</div>" +
          '<div class="gd-act">' + actions(r) + "</div></div>";
      }).join("");
  }
  function copy(text) {
    if (navigator.clipboard && window.isSecureContext) return navigator.clipboard.writeText(text);
    return new Promise(function (res, rej) {
      var ta = d.createElement("textarea"); ta.value = text; ta.style.position = "fixed"; ta.style.opacity = "0"; d.body.appendChild(ta); ta.select();
      try { d.execCommand("copy") ? res() : rej(); } catch (e) { rej(e); } d.body.removeChild(ta);
    });
  }
  d.addEventListener("click", function (ev) {
    var b = ev.target.closest("[data-copy-text]"); if (!b) return;
    var t = b.getAttribute("data-copy-text"), lbl = b.querySelector("span:last-child") || b, old = b.getAttribute("data-label") || lbl.textContent;
    b.setAttribute("data-label", old);
    copy(t).then(function () {
      b.classList.add("is-copied"); lbl.textContent = b.classList.contains("gd-mini") ? "Copied" : (b.getAttribute("data-done") || "Copied");
      var toast = d.getElementById("toast"); if (toast) { toast.textContent = "Copied: " + (t.length > 70 ? t.slice(0, 67) + "…" : t); toast.classList.add("is-on"); setTimeout(function () { toast.classList.remove("is-on"); }, 1800); }
      setTimeout(function () { b.classList.remove("is-copied"); lbl.textContent = old; }, 1800);
    }, function () { window.prompt("Copy this:", t); });
  });
  fBtns.forEach(function (b) {
    b.addEventListener("click", function () {
      filter = b.getAttribute("data-f");
      fBtns.forEach(function (x) { x.setAttribute("aria-checked", x === b ? "true" : "false"); });
      render();
    });
  });
  q.addEventListener("input", render);
  more.addEventListener("click", function () { showAll = true; render(); });

  fetch(list.getAttribute("data-manifest"), { cache: "no-cache" }).then(function (r) { if (!r.ok) throw 0; return r.json(); })
    .then(function (m) {
      if (m.groups) for (var g in m.groups) GROUP[g] = m.groups[g];
      rows = (m.datasets || []).map(function (r) {
        r._s = [r.name, r.description, r.group, GROUP[r.group], r.license, r.format, r.id, r.type, r.link_only ? "link only" : ""].join(" ").toLowerCase();
        r._doc = /^(README\.md|SKILL-COVERAGE\.md)$/.test(r.name) ? 1 : 0;
        return r;
      });
      var T = { synthetic: 0, public: 1, "public-snapshot": 2 };
      rows = rows.map(function (r, i) { r._i = i; return r; }).sort(function (a, b) {
        return (T[a.type] - T[b.type]) || (a.type === "synthetic" ? (a.group === "all") - (b.group === "all") : 0) || 0 || (a._i - b._i);
      });
      render();
    })
    .catch(function () {
      list.innerHTML = '<p class="muted">The dataset list could not load. Open <a href="https://github.com/Open-Medical-Affairs/Data-Sources/releases/latest/download/manifest.csv">manifest.csv</a> or <a href="https://github.com/Open-Medical-Affairs/Data-Sources" target="_blank" rel="noopener">the Data-Sources repository</a>.</p>';
    });
})();
