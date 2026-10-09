/* Click a node in a mission org chart to see the skill's one-line job and a link to its SKILL.md. */
(function () {
  "use strict";
  var d = document, data = d.getElementById("md-data"), out = d.getElementById("md-detail");
  if (!data || !out) return;
  var D = JSON.parse(data.textContent), panel = d.getElementById("md-panel");
  function close() { panel.hidden = true; Array.prototype.forEach.call(d.querySelectorAll(".is-sel"), function (x) { x.classList.remove("is-sel"); }); }
  panel.querySelector(".md-close").addEventListener("click", close);
  d.addEventListener("keydown", function (e) { if (e.key === "Escape" && !panel.hidden) close(); });
  var esc = function (s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); };
  function show(el) {
    Array.prototype.forEach.call(d.querySelectorAll(".is-sel"), function (x) { x.classList.remove("is-sel"); });
    el.classList.add("is-sel"); panel.hidden = false;
    if (el.classList.contains("g-gate")) {
      out.innerHTML = '<h3>Human checkpoint · ' + esc(el.getAttribute("data-gate")) + '</h3><p>' + esc(el.getAttribute("data-detail")) + '</p><p class="muted">Agents draft; people decide. The work stops here until a named person approves, sends back, or accepts with named gaps.</p>';
      return;
    }
    var n = D.nodes[el.getAttribute("data-node")]; if (!n) return;
    var h = '<p class="kicker">' + esc(n.kicker || "") + '</p><h3>' + esc(n.role || n.skills[0]) + '</h3>';
    n.skills.forEach(function (s) {
      var k = D.skills[s]; if (!k) return;
      h += '<div class="md-sk"><code>' + esc(s) + '</code>' +
        '<p>' + esc(k.summary) + '</p>' +
        (k.requires && k.requires.length ? '<p class="md-req">Loads first: ' + k.requires.map(esc).join(", ") + '</p>' : '') +
        '<a class="md-link" href="' + esc(k.url) + '" target="_blank" rel="noopener">Open SKILL.md on GitHub ↗</a></div>';
    });
    if (n.context) h += '<p class="md-ctx"><strong>Context packet:</strong> ' + esc(n.context) + '</p>';
    if (n.consumes && n.consumes.length) h += '<p class="md-ctx"><strong>Waits for:</strong> ' + n.consumes.map(esc).join(", ") + '</p>';
    out.innerHTML = h;
  }
  var sc = d.querySelector(".md-scroll"); if (sc && sc.scrollWidth > sc.clientWidth) sc.scrollLeft = (sc.scrollWidth - sc.clientWidth) / 2;
  d.addEventListener("click", function (e) { var el = e.target.closest(".gnode,.g-gate"); if (el) show(el); });
  d.addEventListener("keydown", function (e) {
    if (e.key !== "Enter" && e.key !== " ") return;
    var el = e.target.closest && e.target.closest(".gnode,.g-gate"); if (el) { e.preventDefault(); show(el); }
  });
})();
/* Simple view by default; the checkbox reveals the skills each worker loads. */
(function () {
  var t = document.getElementById("md-sup"); if (!t) return;
  var s = document.querySelector(".md-v--simple"), f = document.querySelector(".md-v--full");
  t.addEventListener("change", function () { s.hidden = t.checked; f.hidden = !t.checked; });
})();
