/* /deck slide viewer: arrows, swipe, thumbnails, counter, lazy loading (only the current slide and its neighbours load). */
(function () {
  "use strict";
  var root = document.querySelector(".dk"); if (!root) return;
  var S = JSON.parse(root.getAttribute("data-slides")), n = S.length, i = 0;
  var img = root.querySelector(".dk-img"), stage = root.querySelector(".dk-stage"), count = root.querySelector(".dk-count b");
  var ths = Array.prototype.slice.call(root.querySelectorAll(".dk-th")), cache = {};
  function preload(k) { if (k >= 0 && k < n && !cache[k]) { cache[k] = new Image(); cache[k].src = S[k]; } }
  function go(k, fromHash) {
    i = Math.max(0, Math.min(n - 1, k));
    img.src = S[i]; img.alt = "Slide " + (i + 1) + " of " + n; count.textContent = i + 1;
    ths.forEach(function (t, j) { if (j === i) { t.setAttribute("aria-current", "true"); t.scrollIntoView({ block: "nearest", inline: "nearest" }); } else t.removeAttribute("aria-current"); });
    preload(i + 1); preload(i - 1);
    if (!fromHash) history.replaceState(null, "", "#" + (i + 1));
  }
  root.querySelector(".dk-prev").addEventListener("click", function () { go(i - 1); });
  root.querySelector(".dk-next").addEventListener("click", function () { go(i + 1); });
  ths.forEach(function (t) { t.addEventListener("click", function () { go(+t.getAttribute("data-i")); stage.focus({ preventScroll: true }); }); });
  document.addEventListener("keydown", function (e) {
    if (/INPUT|TEXTAREA|SELECT/.test((e.target || {}).tagName || "")) return;
    if (e.key === "ArrowRight" || e.key === "PageDown") { go(i + 1); e.preventDefault(); }
    else if (e.key === "ArrowLeft" || e.key === "PageUp") { go(i - 1); e.preventDefault(); }
    else if (e.key === "Home") { go(0); e.preventDefault(); } else if (e.key === "End") { go(n - 1); e.preventDefault(); }
  });
  var x0 = null, y0 = 0;
  stage.addEventListener("touchstart", function (e) { x0 = e.touches[0].clientX; y0 = e.touches[0].clientY; }, { passive: true });
  stage.addEventListener("touchend", function (e) {
    if (x0 === null) return; var dx = e.changedTouches[0].clientX - x0, dy = e.changedTouches[0].clientY - y0; x0 = null;
    if (Math.abs(dx) > 40 && Math.abs(dx) > Math.abs(dy)) go(i + (dx < 0 ? 1 : -1));
  }, { passive: true });
  stage.addEventListener("click", function (e) { if (e.target === img) { var r = img.getBoundingClientRect(); go(i + (e.clientX - r.left > r.width / 2 ? 1 : -1)); } });
  var fs = root.querySelector(".dk-fs");
  fs.addEventListener("click", function () { if (document.fullscreenElement) document.exitFullscreen(); else if (stage.requestFullscreen) stage.requestFullscreen(); });
  window.addEventListener("hashchange", function () { var k = parseInt(location.hash.slice(1), 10); if (k >= 1 && k <= n && k - 1 !== i) go(k - 1, true); });
  var h = parseInt((location.hash || "").slice(1), 10);
  go(h >= 1 && h <= n ? h - 1 : 0, true);
})();
