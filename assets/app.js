/* AI in Action companion site. No dependencies, no network calls. */
(function () {
  "use strict";
  var d = document, root = d.documentElement;
  root.classList.add("js");
  var $ = function (s, c) { return (c || d).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || d).querySelectorAll(s)); };

  /* ---------- toast + clipboard ---------- */
  var toast = $("#toast"), toastT;
  function say(msg) {
    toast.textContent = msg; toast.classList.add("is-on");
    clearTimeout(toastT); toastT = setTimeout(function () { toast.classList.remove("is-on"); }, 1800);
  }
  function copyText(text) {
    if (navigator.clipboard && window.isSecureContext) return navigator.clipboard.writeText(text);
    return new Promise(function (res, rej) {
      var ta = d.createElement("textarea"); ta.value = text; ta.setAttribute("readonly", "");
      ta.style.position = "fixed"; ta.style.opacity = "0"; d.body.appendChild(ta); ta.select();
      try { d.execCommand("copy") ? res() : rej(); } catch (e) { rej(e); } d.body.removeChild(ta);
    });
  }
  d.addEventListener("click", function (ev) {
    var b = ev.target.closest("[data-copy]"); if (!b) return;
    var el = $(b.getAttribute("data-copy")); if (!el) return;
    var text = (el.innerText || el.textContent).replace(/\u00a0/g, " ").trim();
    if (el.hidden || !el.innerText) text = el.textContent.trim();
    copyText(text).then(function () {
      b.classList.add("is-copied"); var l = $(".lbl", b), old = l && l.textContent;
      if (l && !b.classList.contains("btn-copy--float")) l.textContent = "Copied";
      say("Copied to clipboard");
      setTimeout(function () { b.classList.remove("is-copied"); if (l) l.textContent = old; }, 1600);
    }, function () { say("Press Ctrl/Cmd+C to copy"); });
  });

  /* ---------- nav state ---------- */
  var nav = $(".nav");
  var onScroll = function () { nav.classList.toggle("is-scrolled", window.scrollY > 8); };
  onScroll(); window.addEventListener("scroll", onScroll, { passive: true });
  var links = $$(".nav-links a");
  if ("IntersectionObserver" in window) {
    var secObs = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (!e.isIntersecting) return;
        links.forEach(function (a) { a.classList.toggle("is-active", a.getAttribute("href") === "#" + e.target.id); });
      });
    }, { rootMargin: "-45% 0px -50% 0px" });
    links.forEach(function (a) { var s = $(a.getAttribute("href")); if (s) secObs.observe(s); });
    var rev = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("is-in"); rev.unobserve(e.target); } });
    }, { rootMargin: "0px 0px -8% 0px" });
    $$(".reveal").forEach(function (el) { rev.observe(el); });
  } else { $$(".reveal").forEach(function (el) { el.classList.add("is-in"); }); }

  /* ---------- radiogroup keyboard helper ---------- */
  function radiogroup(group, sel, onPick) {
    var items = $$(sel, group);
    items.forEach(function (b, i) {
      b.addEventListener("click", function () { onPick(b); });
      b.addEventListener("keydown", function (ev) {
        var k = ev.key, j = null;
        if (k === "ArrowRight" || k === "ArrowDown") j = (i + 1) % items.length;
        if (k === "ArrowLeft" || k === "ArrowUp") j = (i - 1 + items.length) % items.length;
        if (j !== null) { ev.preventDefault(); items[j].focus(); onPick(items[j]); }
      });
    });
    return items;
  }
  function check(items, el, attr) {
    items.forEach(function (b) { var on = b === el; b.setAttribute(attr, on ? "true" : "false"); b.tabIndex = on ? 0 : -1; });
  }

  /* ---------- therapeutic area switch ---------- */
  var TA_SHORT = { "oncology-mm": "oncology", "immunology-ad": "immunology", "cardiometabolic-obesity": "cardiometabolic" };
  var taSwitch = $(".ta-switch"), taBtns = [];
  function applyTA(ta) {
    $$("[data-ta-tpl]").forEach(function (el) {
      var t = el.getAttribute("data-ta-tpl").split("__TA__").join(ta).split("__short__").join(TA_SHORT[ta]);
      var c = el.querySelector("code"); (c || el).textContent = t;
    });
    $$("code[data-ta-path]").forEach(function (el) { el.textContent = el.getAttribute("data-ta-path").replace("{ta}", ta); });
    var b = taBtns.filter(function (x) { return x.getAttribute("data-ta") === ta; })[0];
    if (b) check(taBtns, b, "aria-checked");
    try { localStorage.setItem("aia-ta", ta); } catch (e) {}
  }
  if (taSwitch) {
    taBtns = radiogroup(taSwitch, "button", function (b) {
      var ta = b.getAttribute("data-ta"); applyTA(ta);
      say("Prompts now use " + TA_SHORT[ta] + " data");
      if (opt && opt.ta.value !== "own") { opt.ta.value = ta; opt.render(); }
    });
    var saved = null; try { saved = localStorage.getItem("aia-ta"); } catch (e) {}
    if (saved && TA_SHORT[saved] && saved !== "oncology-mm") applyTA(saved);
  }

  /* ---------- give-to-agent block uses this page's own address ---------- */
  var give = $("#give");
  if (give && /^https?:/.test(location.protocol)) {
    var base = location.origin + location.pathname.replace(/[^/]*$/, "");
    $("code", give).textContent = give.getAttribute("data-site-template").split("{SITE}").join(base);
  }

  /* ---------- tabs ---------- */
  var tabs = $$('.tabs [role="tab"]');
  function selectTab(t) {
    tabs.forEach(function (x) {
      var on = x === t; x.setAttribute("aria-selected", on ? "true" : "false"); x.tabIndex = on ? 0 : -1;
      $("#" + x.getAttribute("aria-controls")).hidden = !on;
    });
  }
  tabs.forEach(function (t, i) {
    t.addEventListener("click", function () { selectTab(t); });
    t.addEventListener("keydown", function (ev) {
      var j = ev.key === "ArrowRight" ? (i + 1) % tabs.length : ev.key === "ArrowLeft" ? (i - 1 + tabs.length) % tabs.length : null;
      if (j !== null) { ev.preventDefault(); tabs[j].focus(); selectTab(tabs[j]); }
    });
  });

  /* ---------- skills filter ---------- */
  var filter = $("#skill-filter");
  if (filter) filter.addEventListener("input", function () {
    var q = filter.value.trim().toLowerCase();
    $$(".sg").forEach(function (g) {
      var hits = 0;
      $$("li", g).forEach(function (li) { var m = !q || li.getAttribute("data-skill").indexOf(q) > -1; li.hidden = !m; if (m) hits++; });
      g.hidden = q && !hits; g.open = !!q && hits > 0;
    });
  });

  /* ---------- prompt optimizer (mirrors compose_prompt in build.py) ---------- */
  var opt = null, dataEl = $("#opt-data");
  if (dataEl) {
    var O = JSON.parse(dataEl.textContent), form = $(".opt-form"), out = $("#opt-text code"), meter = $("#opt-meter");
    var TAS = {}; O.therapeutic_areas.forEach(function (t) { TAS[t.id] = t; });
    var typeBtns, current = $('.opt-type[aria-checked="true"]').getAttribute("data-type");
    var typeOf = function (id) { return O.types.filter(function (t) { return t.id === id; })[0]; };
    function items(v) {
      return (Array.isArray(v) ? v : String(v || "").split("\n"))
        .map(function (x) { return String(x).trim().replace(/^-+/, "").trim(); }).filter(Boolean);
    }
    function fill(line, vals) {
      return line.replace(/\{\{([a-z_|]+)\}\}/g, function (_, k) {
        var p = k.split("|"), v = vals[p[0]] === undefined ? "" : vals[p[0]], f = p[1];
        if (f === "list") return items(v).map(function (x) { return "- " + x; }).join("\n");
        if (f === "numbered") return items(v).map(function (x, i) { return (i + 1) + ". " + x; }).join("\n");
        return Array.isArray(v) ? items(v).join(", ") : String(v).trim();
      });
    }
    function compose(typeId, fields, ta, dialect) {
      var t = typeOf(typeId), vals = {}, k;
      for (k in t.defaults) vals[k] = t.defaults[k];
      for (k in fields) if (fields[k] !== null && fields[k] !== undefined) vals[k] = fields[k];
      var dl = TAS[ta]
        ? "- Workshop mode: use the " + TAS[ta].short.toLowerCase() + " synthetic data in workshop/data/" + ta + "/ (mission `" + t.mission + "` in workshop/catalog.json). Read files there by name."
        : "- Use only the material I attach or paste. If something you need is missing, list it instead of inventing it.";
      vals.title = t.label; vals.role = t.role; vals.repo = O.repo; vals.skills = t.skills; vals.data_line = dl;
      vals.steps = O.common_steps_start.concat(t.steps, O.common_steps_end); vals.guardrails = O.guardrails;
      var outp = [];
      O.sections.forEach(function (s) {
        if ((s.needs || []).some(function (n) { return !String(vals[n] || "").trim(); })) return;
        var body = s.lines.map(function (l) { return fill(l, vals); }).filter(function (x) { return x.trim(); });
        if (!body.length) return;
        if (!s.title) outp.push(body.join("\n"));
        else if (dialect === "xml") outp.push("<" + s.tag + ">\n" + body.join("\n") + "\n</" + s.tag + ">");
        else outp.push("## " + s.title + "\n" + body.join("\n"));
      });
      return outp.join("\n\n");
    }
    function setFields(vals) { O.fields.forEach(function (f) { form.elements[f.id].value = vals[f.id] || ""; }); }
    function readFields() { var v = {}; O.fields.forEach(function (f) { v[f.id] = form.elements[f.id].value; }); return v; }
    function render() {
      var text = compose(current, readFields(), form.elements.ta.value, form.elements.dialect.value);
      out.textContent = text;
      var words = text.split(/\s+/).filter(Boolean).length;
      meter.textContent = words + " words";
    }
    function pickType(b) {
      current = b.getAttribute("data-type"); check(typeBtns, b, "aria-checked");
      setFields(typeOf(current).defaults); render();
    }
    typeBtns = radiogroup($(".opt-types"), ".opt-type", pickType);
    form.addEventListener("input", render);
    form.addEventListener("change", render);
    $("#opt-reset").addEventListener("click", function () { setFields(typeOf(current).defaults); render(); say("Reset to defaults"); });
    $$("[data-load-lib]").forEach(function (b) {
      b.addEventListener("click", function () {
        var it = O.library.filter(function (x) { return x.id === b.getAttribute("data-load-lib"); })[0];
        var tb = typeBtns.filter(function (x) { return x.getAttribute("data-type") === it.type; })[0];
        current = it.type; check(typeBtns, tb, "aria-checked");
        var v = {}, k, def = typeOf(it.type).defaults; for (k in def) v[k] = def[k]; for (k in it.fields) v[k] = it.fields[k];
        setFields(v); form.elements.ta.value = it.ta; render();
        $("#opt").scrollIntoView({ behavior: "smooth", block: "start" });
        say("Loaded: " + it.team);
      });
    });
    form.elements.dialect.addEventListener("change", function () {
      var dlt = form.elements.dialect.value;
      $$(".lib-text").forEach(function (p) { $("code", p).textContent = JSON.parse(p.getAttribute("data-dialects"))[dlt]; });
    });
    opt = { ta: form.elements.ta, render: render };
    try { var s = localStorage.getItem("aia-ta"); if (s && TAS[s]) { form.elements.ta.value = s; } } catch (e) {}
    render();
  }
})();
