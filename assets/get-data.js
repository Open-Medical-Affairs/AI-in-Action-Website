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
  function actions(r) {
    var a = [];
    if (r.access === "download") a.push('<a class="gd-a gd-a--dl" href="' + esc(r.direct_url) + '" download>Download</a>');
    else if (r.access === "api-sample") a.push('<a class="gd-a gd-a--dl" href="' + esc(r.direct_url) + '" target="_blank" rel="noopener">Get sample</a>');
    else if (r.access === "bulk-file") a.push('<a class="gd-a gd-a--dl" href="' + esc(r.direct_url) + '">Download</a>');
    else if (r.access === "official-site" && r.direct_url !== r.view_url) a.push('<a class="gd-a" href="' + esc(r.direct_url) + '" target="_blank" rel="noopener">Download / API page</a>');
    a.push('<a class="gd-a" href="' + esc(r.view_url) + '" target="_blank" rel="noopener">' + (r.type === "synthetic" ? "View" : "Open source") + "</a>");
    return a.join("");
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
    list.innerHTML = '<div class="gd-row gd-row--h" aria-hidden="true"><span>Dataset</span><span>Type</span><span>Licence</span><span>Get it</span></div>' +
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
