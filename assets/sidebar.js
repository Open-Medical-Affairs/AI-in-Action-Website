/* Mobile drawer for the left sidebar. */
(function () {
  "use strict";
  var d = document, b = d.body, side = d.getElementById("sb-side"), scrim = d.getElementById("sb-scrim"), btn = d.getElementById("sb-open");
  if (!side || !btn) return;
  function set(open) {
    b.classList.toggle("sb-open", open); btn.setAttribute("aria-expanded", open ? "true" : "false");
    scrim.hidden = !open;
    if (open) { var a = side.querySelector("a.is-active") || side.querySelector("a"); if (a) a.focus(); } else btn.focus({ preventScroll: true });
  }
  btn.addEventListener("click", function () { set(!b.classList.contains("sb-open")); });
  scrim.addEventListener("click", function () { set(false); });
  d.addEventListener("keydown", function (e) { if (e.key === "Escape" && b.classList.contains("sb-open")) set(false); });
  side.addEventListener("click", function (e) { if (e.target.closest("a") && b.classList.contains("sb-open")) b.classList.remove("sb-open"); });
})();
