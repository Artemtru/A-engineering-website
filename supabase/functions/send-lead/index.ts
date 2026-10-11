// Публичная форма заявки с сайта А-Инжиниринг.
// Ничего не хранит: принимает заявку и сразу пересылает письмом через SMTP Яндекс 360.
// Защита: список разрешённых сайтов (Origin), скрытое поле-ловушка для ботов, проверка и ограничение полей.
// Секреты (Dashboard → Edge Functions → Secrets): SMTP_USER, SMTP_PASS (пароль приложения Яндекса),
// необязательно: MAIL_TO (куда слать, по умолчанию SMTP_USER), ALLOWED_ORIGINS (через запятую).
// Развёрнута с verify_jwt = false: это публичная форма, защита реализована в коде выше.
import { SMTPClient } from "https://deno.land/x/denomailer@1.6.0/mod.ts";

const DEFAULT_ORIGINS = [
  "https://engineeringsys.ru",
  "https://www.engineeringsys.ru",
];

function originAllowed(origin: string | null): boolean {
  if (!origin) return false;
  const extra = (Deno.env.get("ALLOWED_ORIGINS") ?? "")
    .split(",").map((s) => s.trim()).filter(Boolean);
  if ([...DEFAULT_ORIGINS, ...extra].includes(origin)) return true;
  // отладка на GitHub Pages и локально
  if (/^https:\/\/[a-z0-9-]+\.github\.io$/i.test(origin)) return true;
  if (/^http:\/\/(localhost|127\.0\.0\.1)(:\d+)?$/.test(origin)) return true;
  return false;
}

function cors(origin: string | null): Record<string, string> {
  return {
    "Access-Control-Allow-Origin": originAllowed(origin) ? origin! : "https://engineeringsys.ru",
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "content-type",
    "Vary": "Origin",
  };
}

function json(body: unknown, status: number, origin: string | null) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { "Content-Type": "application/json; charset=utf-8", ...cors(origin) },
  });
}

const esc = (s: string) =>
  s.replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]!));

Deno.serve(async (req: Request) => {
  const origin = req.headers.get("origin");
  if (req.method === "OPTIONS") return new Response(null, { status: 204, headers: cors(origin) });
  if (req.method !== "POST") return json({ ok: false, error: "method" }, 405, origin);
  if (!originAllowed(origin)) return json({ ok: false, error: "origin" }, 403, origin);

  let data: Record<string, unknown>;
  try {
    const raw = await req.text();
    if (raw.length > 5000) return json({ ok: false, error: "too_large" }, 413, origin);
    data = JSON.parse(raw);
  } catch {
    return json({ ok: false, error: "bad_json" }, 400, origin);
  }

  // ловушка для ботов: поле скрыто от людей, бот его заполняет
  if (typeof data.website === "string" && data.website.trim() !== "") {
    return json({ ok: true }, 200, origin);
  }

  const name = String(data.name ?? "").trim().slice(0, 100);
  const phone = String(data.phone ?? "").trim().slice(0, 30);
  const message = String(data.message ?? "").trim().slice(0, 2000);
  const page = String(data.page ?? "").trim().slice(0, 200);
  if (!name || phone.replace(/\D/g, "").length < 10) {
    return json({ ok: false, error: "validation" }, 422, origin);
  }

  const user = Deno.env.get("SMTP_USER");
  const pass = Deno.env.get("SMTP_PASS");
  if (!user || !pass) return json({ ok: false, error: "not_configured" }, 500, origin);
  const to = Deno.env.get("MAIL_TO") ?? user;

  const when = new Date().toLocaleString("ru-RU", { timeZone: "Europe/Moscow" });
  const text = `Новая заявка с сайта\n\nИмя: ${name}\nТелефон: ${phone}\nОбъект и задача: ${message || "—"}\n\nВремя (МСК): ${when}\nСтраница: ${page || "—"}`;
  const html = `<h2>Новая заявка с сайта</h2>
<p><b>Имя:</b> ${esc(name)}<br><b>Телефон:</b> <a href="tel:${esc(phone.replace(/[^\d+]/g, ""))}">${esc(phone)}</a></p>
<p><b>Объект и задача:</b><br>${esc(message || "—").replace(/\n/g, "<br>")}</p>
<p style="color:#666;font-size:12px">Время (МСК): ${esc(when)}<br>Страница: ${esc(page || "—")}</p>`;

  const client = new SMTPClient({
    connection: { hostname: "smtp.yandex.ru", port: 465, tls: true, auth: { username: user, password: pass } },
  });
  try {
    await client.send({
      from: `Сайт А-Инжиниринг <${user}>`,
      to,
      subject: `Заявка с сайта: ${name}`,
      content: text,
      html,
    });
    await client.close();
  } catch (e) {
    // в логи пишем только тип ошибки, без персональных данных
    console.error("smtp_error", e instanceof Error ? e.name + ": " + e.message.slice(0, 200) : "unknown");
    try { await client.close(); } catch { /* ignore */ }
    return json({ ok: false, error: "send_failed" }, 502, origin);
  }
  return json({ ok: true }, 200, origin);
});
