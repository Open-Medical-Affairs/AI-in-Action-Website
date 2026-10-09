/* AI in Action website server.
   - Serves the static site.
   - POST /api/optimize : expands a short goal into a Grok Bot / agent-swarm assignment via the Venice API.
   - GET  /healthz      : health check for Railway.
   No dependencies: Node 18+ (built-in fetch). The Venice key never leaves the server. */
"use strict";
const http = require("http");
const fs = require("fs");
const path = require("path");
const { buildMessages } = require("./prompts");
const DATA = require("../assets/optimizer-data.js");

const ROOT = path.resolve(__dirname, "..");

/* Local runs: load .env if present (Railway sets real environment variables instead). */
try {
  fs.readFileSync(path.join(ROOT, ".env"), "utf8").split(/\r?\n/).forEach((line) => {
    const m = line.match(/^\s*([A-Z0-9_]+)\s*=\s*(.*)\s*$/);
    if (m && !process.env[m[1]]) process.env[m[1]] = m[2];
  });
} catch (_) { /* no .env: fine */ }
const PORT = Number(process.env.PORT) || 3000;
const VENICE_URL = (process.env.VENICE_BASE_URL || "https://api.venice.ai/api/v1").replace(/\/+$/, "") + "/chat/completions";
const MODEL = (process.env.VENICE_MODEL || "").trim() || "z-ai-glm-5-3-flash";
const MAX_GOAL = 1500;            // characters
const MAX_BODY = 16 * 1024;       // bytes
const TIMEOUT_MS = Number(process.env.VENICE_TIMEOUT_MS) || 60000;
// Conference Wi-Fi puts many attendees behind one IP, so per-IP limits are generous and a global cap protects credits.
const RATE = { perMinute: Number(process.env.RATE_PER_MINUTE) || 20, perHour: Number(process.env.RATE_PER_HOUR) || 200, globalPerMinute: Number(process.env.RATE_GLOBAL_PER_MINUTE) || 90 };

function veniceKey() {
  const k = process.env.VENICE_API_KEY;
  return k ? k.replace(/['"]/g, "").trim() : "";   // tolerate accidental quotes in the dashboard
}

/* ---------- tiny in-memory rate limiter (per IP) ---------- */
const hits = new Map();
function clientIp(req) {
  const xf = String(req.headers["x-forwarded-for"] || "").split(",")[0].trim();
  return xf || req.socket.remoteAddress || "unknown";
}
let globalHits = [];
function rateLimited(ip) {
  const now = Date.now();
  globalHits = globalHits.filter((t) => now - t < 60e3);
  if (globalHits.length >= RATE.globalPerMinute) return true;
  const list = (hits.get(ip) || []).filter((t) => now - t < 3600e3);
  const lastMin = list.filter((t) => now - t < 60e3).length;
  if (lastMin >= RATE.perMinute || list.length >= RATE.perHour) { hits.set(ip, list); return true; }
  list.push(now); hits.set(ip, list); globalHits.push(now); return false;
}
setInterval(() => { const now = Date.now(); for (const [ip, l] of hits) if (!l.some((t) => now - t < 3600e3)) hits.delete(ip); }, 600e3).unref();

/* ---------- helpers ---------- */
const SEC_HEADERS = { "X-Content-Type-Options": "nosniff", "Referrer-Policy": "strict-origin-when-cross-origin", "X-Frame-Options": "SAMEORIGIN" };
function json(res, status, obj, extra) {
  res.writeHead(status, Object.assign({ "Content-Type": "application/json; charset=utf-8", "Cache-Control": "no-store" }, SEC_HEADERS, extra || {}));
  res.end(JSON.stringify(obj));
}
function readBody(req) {
  return new Promise((resolve, reject) => {
    let size = 0; const chunks = [];
    req.on("data", (c) => { size += c.length; if (size > MAX_BODY) { reject(Object.assign(new Error("too_large"), { code: 413 })); req.destroy(); } else chunks.push(c); });
    req.on("end", () => resolve(Buffer.concat(chunks).toString("utf8")));
    req.on("error", reject);
  });
}

/* ---------- /api/optimize ---------- */
async function optimize(req, res) {
  const key = veniceKey();
  if (!key) return json(res, 503, { error: "not_configured", message: "The AI optimizer is not configured on this server (VENICE_API_KEY is missing). Use the built-in template instead." });

  let body;
  try { body = JSON.parse(await readBody(req) || "{}"); }
  catch (e) { return json(res, e.code === 413 ? 413 : 400, { error: "bad_request", message: e.code === 413 ? "Request too large." : "Send JSON: {\"goal\": \"...\", \"mode\": \"single\"|\"swarm\"}." }); }

  const goal = String(body.goal || "").trim();
  if (!goal) return json(res, 400, { error: "bad_request", message: "Type a goal first." });
  if (goal.length > MAX_GOAL) return json(res, 400, { error: "too_long", message: `Keep the goal under ${MAX_GOAL} characters. Short is fine: the optimizer expands it.` });
  if (rateLimited(clientIp(req))) return json(res, 429, { error: "rate_limited", message: "Too many requests from your network. Wait a minute, or use the built-in template." }, { "Retry-After": "60" });
  const mode = body.mode === "swarm" ? "swarm" : "single";
  const ta = Object.prototype.hasOwnProperty.call(DATA.therapeuticAreas, body.ta) ? body.ta : "own";
  const starter = DATA.starters.find((s) => s.id === body.starter) || null;
  const data = ["own", "practice", "none"].includes(body.data) ? body.data : undefined;
  const dataNote = String(body.data_note || "").slice(0, 300);
  const stream = body.stream !== false;

  const ctrl = new AbortController();
  const timer = setTimeout(() => ctrl.abort(), TIMEOUT_MS);
  req.on("close", () => { if (!res.writableEnded) ctrl.abort(); });

  let upstream;
  try {
    upstream = await fetch(VENICE_URL, {
      method: "POST",
      signal: ctrl.signal,
      headers: { "Content-Type": "application/json", Authorization: `Bearer ${key}` },
      body: JSON.stringify({
        model: MODEL,
        messages: buildMessages({ goal, mode, ta, starter, data, dataNote }),
        temperature: 0.4,
        max_tokens: 4000,
        stream,
        venice_parameters: { include_venice_system_prompt: false, enable_web_search: "off", strip_thinking_response: true, disable_thinking: true }
      })
    });
  } catch (e) {
    clearTimeout(timer);
    return json(res, e.name === "AbortError" ? 504 : 502, { error: "upstream_unreachable", message: e.name === "AbortError" ? "Venice took too long. Try again or use the template." : "Could not reach Venice. Use the built-in template." });
  }

  if (!upstream.ok) {
    clearTimeout(timer);
    const detail = await upstream.text().catch(() => "");
    console.error(`[optimize] Venice ${upstream.status}: ${detail.slice(0, 300)}`);
    const msg = { 401: "The server's Venice key was rejected.", 402: "The Venice account is out of credit.", 429: "Venice is rate limiting. Try again shortly.", 503: "The model is at capacity. Try again shortly." }[upstream.status] || `Venice returned ${upstream.status}.`;
    return json(res, 502, { error: "upstream_error", status: upstream.status, message: msg + " The built-in template still works." });
  }

  if (!stream || !/event-stream/.test(upstream.headers.get("content-type") || "")) {
    clearTimeout(timer);
    const data = await upstream.json().catch(() => null);
    const text = data && data.choices && data.choices[0] && data.choices[0].message && data.choices[0].message.content;
    if (!text) return json(res, 502, { error: "empty", message: "Venice returned no text. Use the template." });
    return json(res, 200, { text: clean(text), model: data.model || MODEL });
  }

  // Stream plain-text deltas to the browser (Venice SSE -> text chunks).
  res.writeHead(200, Object.assign({ "Content-Type": "text/plain; charset=utf-8", "Cache-Control": "no-store", "X-Accel-Buffering": "no", "X-Model": MODEL }, SEC_HEADERS));
  const decoder = new TextDecoder(); let buf = "";
  try {
    for await (const chunk of upstream.body) {
      buf += decoder.decode(chunk, { stream: true });
      let i;
      while ((i = buf.indexOf("\n")) >= 0) {
        const line = buf.slice(0, i).trim(); buf = buf.slice(i + 1);
        if (!line.startsWith("data:")) continue;
        const payload = line.slice(5).trim();
        if (payload === "[DONE]") continue;
        try {
          const j = JSON.parse(payload);
          const delta = j.choices && j.choices[0] && j.choices[0].delta && j.choices[0].delta.content;
          if (delta) res.write(delta);
        } catch (_) { /* ignore keep-alives */ }
      }
    }
  } catch (e) {
    if (e.name !== "AbortError") console.error("[optimize] stream error", e.message);
  } finally { clearTimeout(timer); res.end(); }
}
function clean(t) { return String(t).replace(/<think>[\s\S]*?<\/think>/g, "").trim(); }

/* ---------- data manifest: kept in sync with the Data-Sources release ---------- */
const MANIFEST_URL = process.env.DATA_MANIFEST_URL || "https://github.com/Open-Medical-Affairs/Data-Sources/releases/latest/download/manifest.json";
let liveManifest = null;   // JSON string, refreshed every 6 hours; falls back to the bundled data-manifest.json
async function refreshManifest() {
  try {
    const r = await fetch(MANIFEST_URL, { signal: AbortSignal.timeout(20000), headers: { "User-Agent": "ai-in-action-website" } });
    if (!r.ok) throw new Error("HTTP " + r.status);
    const m = await r.json();
    if (!Array.isArray(m.datasets) || !m.datasets.length) throw new Error("no datasets");
    liveManifest = JSON.stringify(m);
    console.log(`[data] manifest refreshed: ${m.datasets.length} datasets`);
  } catch (e) { console.warn(`[data] manifest refresh failed (${e.message}); serving the bundled copy`); }
}
if (process.env.DATA_MANIFEST_SYNC !== "off") { refreshManifest(); setInterval(refreshManifest, 6 * 3600e3).unref(); }

/* ---------- static files ---------- */
const TYPES = { ".html": "text/html; charset=utf-8", ".css": "text/css; charset=utf-8", ".js": "text/javascript; charset=utf-8", ".json": "application/json; charset=utf-8",
  ".md": "text/markdown; charset=utf-8", ".txt": "text/plain; charset=utf-8", ".svg": "image/svg+xml", ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
  ".webp": "image/webp", ".ico": "image/x-icon", ".csv": "text/csv; charset=utf-8", ".pdf": "application/pdf", ".woff2": "font/woff2" };
const BLOCKED = /^\/(server|node_modules|shots|tools|__pycache__)(\/|$)|\/\.|^\/(package(-lock)?\.json|railway\.json|Procfile|build\.py)$/i;
function sendFile(req, res, file, st, status) {
  const type = TYPES[path.extname(file).toLowerCase()];
  const cache = /\.(html|json|md|txt)$/.test(file) ? "no-cache" : "public, max-age=3600";
  res.writeHead(status || 200, Object.assign({ "Content-Type": type, "Content-Length": st.size, "Cache-Control": cache }, SEC_HEADERS));
  if (req.method === "HEAD") return res.end();
  fs.createReadStream(file).pipe(res);
}
function statFile(file) { try { const st = fs.statSync(file); return st.isFile() ? st : null; } catch (_) { return null; } }
/* Clean routes: /missions -> missions.html, /missions/launch-plan-swarm -> missions/launch-plan-swarm.html,
   /agents/ -> 301 /agents. Anything else that is missing gets 404.html with a 404 status. */
function serveStatic(req, res, urlPath) {
  let p; try { p = decodeURIComponent(urlPath); } catch (_) { return json(res, 400, { error: "bad_path" }); }
  if (p.length > 1 && p.endsWith("/")) { res.writeHead(301, Object.assign({ Location: p.replace(/\/+$/, "") || "/" }, SEC_HEADERS)); return res.end(); }
  if (p === "/") p = "/index.html";
  if (BLOCKED.test(p)) return notFound(req, res);
  const file = path.join(ROOT, path.normalize(p));
  if (!file.startsWith(ROOT + path.sep)) return notFound(req, res);
  const candidates = path.extname(file) ? [file] : [file + ".html", path.join(file, "index.html")];
  for (const f of candidates) {
    if (!TYPES[path.extname(f).toLowerCase()]) continue;
    const st = statFile(f);
    if (st) return sendFile(req, res, f, st);
  }
  notFound(req, res);
}
function notFound(req, res) {
  const page = path.join(ROOT, "404.html"), st = statFile(page);
  if (st && /text\/html|\*\/\*/.test(req.headers.accept || "*/*") && !/\.(js|css|json|png|svg|jpg|webp|md|txt|csv)$/i.test(req.url.split("?")[0])) return sendFile(req, res, page, st, 404);
  res.writeHead(404, Object.assign({ "Content-Type": "text/plain; charset=utf-8" }, SEC_HEADERS)); res.end("Not found");
}

/* ---------- router ---------- */
const server = http.createServer((req, res) => {
  const url = new URL(req.url, "http://localhost");
  if (url.pathname === "/healthz") return json(res, 200, { ok: true, ai: !!veniceKey(), model: MODEL });
  if (url.pathname === "/api/optimize") {
    if (req.method !== "POST") return json(res, 405, { error: "method_not_allowed", message: "POST a JSON body." }, { Allow: "POST" });
    return optimize(req, res).catch((e) => { console.error(e); if (!res.headersSent) json(res, 500, { error: "server_error", message: "Something went wrong. Use the template." }); else res.end(); });
  }
  if (req.method !== "GET" && req.method !== "HEAD") return json(res, 405, { error: "method_not_allowed" });
  if (url.pathname === "/data-manifest.json" && liveManifest) {
    res.writeHead(200, Object.assign({ "Content-Type": "application/json; charset=utf-8", "Cache-Control": "public, max-age=300" }, SEC_HEADERS));
    return res.end(req.method === "HEAD" ? undefined : liveManifest);
  }
  serveStatic(req, res, url.pathname);
});
server.requestTimeout = 120000;
server.listen(PORT, () => console.log(`AI in Action site on :${PORT} · Venice ${veniceKey() ? "configured" : "NOT configured (template fallback only)"} · model ${MODEL}`));
