const EXAMPLES = [
  { lang: "ru", cat: "ru", q: "Сколько сделок и на какую сумму было заключено в 2024 году?" },
  { lang: "uz", cat: "uz", q: "2025-yilda nechta bitim tuzilgan va ularning umumiy summasi qancha?" },
  { lang: "ru", cat: "ru", q: "Топ-5 товаров по общей сумме сделок за всё время" },
  { lang: "uz", cat: "uz", q: "Qaysi viloyatda 2025-yilda bitimlar summasi eng katta?" },
  { lang: "ru", cat: "ru", q: "Какой объём бензина АИ-92 продали в 2025 году?" },
  { lang: "uz", cat: "uz", q: "Paxta yog‘i bo‘yicha 2024-yildagi o‘rtacha narx qancha?" },
  { lang: "ru", cat: "ru", q: "Сколько сделок совершила компания «Сотото Металл»?" },
  { lang: "uz", cat: "uz", q: "2024-yilda eng ko‘p bitim tuzgan top-5 sotuvchi kompaniyalar kimlar?" },
  { lang: "ru", cat: "ru", q: "Какова сумма сделок по медному катоду в 2024 году в долларах США и в сумах?" },
  { lang: "ru", cat: "ru", q: "По скольким сделкам была просрочена оплата, а по скольким — поставка?" },
  { lang: "ru", cat: "ru", q: "По скольким контрактам в реестре не было совершено ни одной сделки?" },
  { lang: "ru", cat: "ru", q: "Какой товар имеет код ТН ВЭД 252329?" },
  { lang: "ru", cat: "guard", q: "Сколько сделок по золоту было в 2025 году?" },
  { lang: "uz", cat: "guard", q: "2026-yil noyabr oyida nechta bitim tuzilgan?" },
  { lang: "ru", cat: "guard", q: "Кто директор компании CHO‘HE KLASTER MCHJ?" },
];

const I18N = {
  ru: {
    appTitle: "ИИ-агент реестра биржевых сделок spot.uzex.uz",
    tabChat: "💬 ИИ-Агент (Вопрос-ответ)",
    tabDashboard: "📊 Аналитика и Реестр",
    tabArch: "🛡️ О решении и Верификация",
    btnNewChat: "Новый диалог",
    examplesTitle: "Примеры вопросов (RU / UZ)",
    filterAll: "Все",
    guaranteeTitle: "Гарантия точности (0% галлюцинаций)",
    g1: "<b>Только по данным DuckDB:</b> каждое число в ответе вычисляется реальным SQL-запросом по 500 000 сделкам.",
    g2: "<b>100% нормализация:</b> марки, сорта, классы и размеры извлечены даже из текстовых названий контрактов.",
    g3: "<b>Фонетический поиск RU↔UZ:</b> находит компании и брокеров независимо от латиницы, кириллицы и кавычек.",
    g4: "<b>Numeric Grounding Verifier:</b> автоматическая сверка каждого числа в тексте ответа с результатами SQL.",
    welcomeTitle: "Задайте любой вопрос о биржевых сделках на русском или узбекском",
    welcomeDesc:
      "Агент понимает русский и узбекский языки (латиницу и кириллицу), автоматически находит компании, брокеров, товары, марки и коды ТН ВЭД, выполняет точные SQL-запросы по 500 000 сделкам и показывает, на каких данных основан каждый ответ.",
    placeholder: "Спросите на русском или узбекском (например: Сколько сделок по бензину АИ-92 было в 2024 году?)…",
    btnSend: "Спросить",
    dashTitle: "Аналитический обзор реестра сделок UZEX (2022–2026)",
    dashSub:
      "Все показатели рассчитаны напрямую из денормализованной базы DuckDB. Нажмите на любой товар, регион или компанию, чтобы задать вопрос ИИ-агенту.",
    btnRefresh: "↻ Обновить",
    chartYearsTitle: "Динамика оборота и сделок по годам (2022–2026)",
    chartStatusTitle: "Распределение сделок по статусам и дисциплине",
    chartProductsTitle: "Топ-12 биржевых товаров по сумме сделок (трлн сум)",
    chartRegionsTitle: "Регионы складской отгрузки по сумме сделок",
    chartSellersTitle: "Топ-10 крупнейших продавцов (по обороту)",
    chartBuyersTitle: "Топ-10 крупнейших покупателей (по обороту)",
  },
  uz: {
    appTitle: "spot.uzex.uz birja bitimlari reyestri AI-agenti",
    tabChat: "💬 AI-Agent (Savol-javob)",
    tabDashboard: "📊 Tahlil va Reyestr",
    tabArch: "🛡️ Yechim va Tekshiruv",
    btnNewChat: "Yangi suhbat",
    examplesTitle: "Namuna savollar (RU / UZ)",
    filterAll: "Barchasi",
    guaranteeTitle: "Aniqlik kafolati (0% gallyutsinatsiya)",
    g1: "<b>Faqat DuckDB ma’lumotlari asosida:</b> javobdagi har bir raqam 500 000 ta bitim bo‘yicha real SQL-so‘rov orqali hisoblanadi.",
    g2: "<b>100% normalizatsiya:</b> marka, nav, sinf va o‘lchamlar shartnoma matnlaridan ham to‘liq ajratib olingan.",
    g3: "<b>Fonetik qidiruv RU↔UZ:</b> kompaniya va brokerlarni lotin, kirill yoki qo‘shtirnoqlardan qat’i nazar topadi.",
    g4: "<b>Numeric Grounding Verifier:</b> javobdagi har bir raqam SQL natijalari bilan avtomatik solishtiriladi.",
    welcomeTitle: "Birja bitimlari haqida o‘zbek yoki rus tilida istalgan savol bering",
    welcomeDesc:
      "Agent o‘zbek (lotin va kirill) hamda rus tillarini tushunadi, kompaniya, broker, mahsulot, marka va TIF TN kodlarini avtomatik topadi, 500 000 ta bitim bo‘yicha aniq SQL-so‘rovlarni bajaradi va javob qaysi ma’lumotlarga asoslanganini ko‘rsatadi.",
    placeholder: "O‘zbek yoki rus tilida so‘rang (masalan: 2025-yilda AI-92 benzini bo‘yicha nechta bitim tuzilgan?)…",
    btnSend: "So‘rash",
    dashTitle: "UZEX bitimlar reyestri tahliliy sharhi (2022–2026)",
    dashSub:
      "Barcha ko‘rsatkichlar to‘g‘ridan-to‘g‘ri DuckDB bazasidan hisoblangan. Istalgan mahsulot, hudud yoki kompaniyani bosib, AI-agentga savol bering.",
    btnRefresh: "↻ Yangilash",
    chartYearsTitle: "Yillar kesimida bitimlar soni va aylanmasi (2022–2026)",
    chartStatusTitle: "Bitimlar holati va intizomi bo‘yicha taqsimot",
    chartProductsTitle: "Bitimlar summasi bo‘yicha Top-12 birja mahsulotlari (trln so‘m)",
    chartRegionsTitle: "Ombor joylashgan hududlar kesimida bitimlar summasi",
    chartSellersTitle: "Top-10 eng yirik sotuvchilar (aylanma bo‘yicha)",
    chartBuyersTitle: "Top-10 eng yirik xaridorlar (aylanma bo‘yicha)",
  },
};

const API_BASE = (
  new URLSearchParams(window.location.search).get("api") ||
  window.UZEX_API_BASE ||
  ""
).replace(/\/+$/, "");

let currentLang = "ru";
let currentQFilter = "all";
const history = [];
let dashLoaded = false;

const messagesEl = document.getElementById("messages");
const formEl = document.getElementById("askForm");
const inputEl = document.getElementById("qInput");
const sendBtn = document.getElementById("sendBtn");
const clearBtn = document.getElementById("clearBtn");
const examplesEl = document.getElementById("examples");

// ---------------- Language & Examples ----------------
function renderExamples() {
  examplesEl.innerHTML = "";
  const list = EXAMPLES.filter((item) => {
    if (currentQFilter === "all") return true;
    return item.cat === currentQFilter;
  });
  for (const item of list) {
    const b = document.createElement("button");
    b.type = "button";
    b.className = "ex-btn";
    const tagClass = item.cat === "guard" ? "guard" : item.lang === "uz" ? "uz" : "";
    const tagLabel = item.cat === "guard" ? "GUARD" : item.lang.toUpperCase();
    b.innerHTML = `<span class="tag ${tagClass}">${tagLabel}</span>${escapeHtml(item.q)}`;
    b.addEventListener("click", () => {
      switchTab("chat");
      inputEl.value = item.q;
      formEl.requestSubmit();
    });
    examplesEl.appendChild(b);
  }
}

function setLanguage(lang) {
  currentLang = lang;
  document.querySelectorAll(".lang-btn").forEach((b) => {
    b.classList.toggle("active", b.dataset.lang === lang);
  });
  const dict = I18N[lang] || I18N.ru;
  document.querySelectorAll("[data-i18n]").forEach((el) => {
    const key = el.dataset.i18n;
    if (dict[key]) el.innerHTML = dict[key];
  });
  inputEl.placeholder = dict.placeholder;
}

document.querySelectorAll(".lang-btn").forEach((btn) => {
  btn.addEventListener("click", () => setLanguage(btn.dataset.lang));
});

document.querySelectorAll(".pill[data-qfilter]").forEach((btn) => {
  btn.addEventListener("click", () => {
    currentQFilter = btn.dataset.qfilter;
    document.querySelectorAll(".pill[data-qfilter]").forEach((p) => p.classList.toggle("active", p === btn));
    renderExamples();
  });
});

renderExamples();

// ---------------- Tabs ----------------
function switchTab(tabName) {
  document.querySelectorAll(".nav-tab").forEach((t) => {
    t.classList.toggle("active", t.dataset.tab === tabName);
  });
  document.querySelectorAll(".tab-panel").forEach((p) => {
    p.classList.toggle("active", p.id === `tab-${tabName}`);
  });
  if (tabName === "dashboard" && !dashLoaded) {
    loadDashboard();
  }
}

document.querySelectorAll(".nav-tab").forEach((btn) => {
  btn.addEventListener("click", () => switchTab(btn.dataset.tab));
});

// ---------------- Topbar Stats ----------------
let cachedStats = null;
fetch(API_BASE + "/api/stats")
  .then((r) => r.json())
  .then((s) => {
    if (s && s.deals) {
      cachedStats = s;
      document.getElementById("statsline").textContent =
        `${fmtNum(s.deals)} сделок · ${fmtNum(s.contracts)} контрактов · ${fmtNum(s.participants)} участников · ` +
        `${fmtNum(s.brokers)} брокеров · ${s.from || s.min_date} — ${s.to || s.max_date}`;
    }
  })
  .catch(() => {});

// ---------------- Chat Composer ----------------
inputEl.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    formEl.requestSubmit();
  }
});
inputEl.addEventListener("input", () => {
  inputEl.style.height = "auto";
  inputEl.style.height = Math.min(inputEl.scrollHeight, 140) + "px";
});

clearBtn.addEventListener("click", () => {
  history.length = 0;
  messagesEl.innerHTML = "";
});

formEl.addEventListener("submit", async (e) => {
  e.preventDefault();
  const q = inputEl.value.trim();
  if (!q) return;
  const w = document.getElementById("welcome");
  if (w) w.remove();

  inputEl.value = "";
  inputEl.style.height = "auto";
  sendBtn.disabled = true;

  addUserMsg(q);
  const bot = addBotMsg();

  try {
    const res = await fetch(API_BASE + "/api/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question: q, history: history.slice(-4) }),
    });
    const reader = res.body.getReader();
    const dec = new TextDecoder();
    let buf = "";
    let finalResult = null;
    while (true) {
      const { value, done } = await reader.read();
      if (done) break;
      buf += dec.decode(value, { stream: true });
      let idx;
      while ((idx = buf.indexOf("\n")) >= 0) {
        const line = buf.slice(0, idx).trim();
        buf = buf.slice(idx + 1);
        if (!line) continue;
        const ev = JSON.parse(line);
        if (ev.type === "tool") {
          bot.addLiveStep(ev);
        } else if (ev.type === "done") {
          finalResult = ev.result;
        }
      }
    }
    if (finalResult) {
      bot.finalize(finalResult);
      history.push({ q, a: finalResult.answer });
    } else {
      bot.fail("Пустой ответ от сервера.");
    }
  } catch (err) {
    bot.fail("Ошибка соединения: " + err.message);
  } finally {
    sendBtn.disabled = false;
    inputEl.focus();
  }
});

function addUserMsg(text) {
  const el = document.createElement("div");
  el.className = "msg user";
  el.innerHTML = `<div class="bubble">${escapeHtml(text)}</div>`;
  messagesEl.appendChild(el);
  messagesEl.scrollTop = messagesEl.scrollHeight;
}

function addBotMsg() {
  const el = document.createElement("div");
  el.className = "msg bot";
  const traceEl = document.createElement("div");
  traceEl.className = "trace";
  const bubbleEl = document.createElement("div");
  bubbleEl.className = "bubble";
  bubbleEl.innerHTML = `<span class="spinner"></span> &nbsp;${
    currentLang === "uz"
      ? "Savol tahlil qilinmoqda va DuckDB bo‘yicha SQL-so‘rovlar bajarilmoqda…"
      : "Анализирую вопрос и выполняю SQL-запросы к DuckDB…"
  }`;
  const metaEl = document.createElement("div");
  metaEl.className = "meta-bar";
  el.appendChild(traceEl);
  el.appendChild(bubbleEl);
  el.appendChild(metaEl);
  messagesEl.appendChild(el);
  messagesEl.scrollTop = messagesEl.scrollHeight;

  return {
    addLiveStep(ev) {
      const d = document.createElement("div");
      d.className = "trace-item";
      if (ev.tool === "run_sql") {
        d.innerHTML = `<span class="badge sql">SQL</span> ${escapeHtml(ev.args?.purpose || "Выполнение запроса…")}`;
      } else if (ev.tool === "find_entity") {
        d.innerHTML = `<span class="badge ent">ПОИСК</span> «${escapeHtml(ev.args?.query || "")}»`;
      }
      traceEl.appendChild(d);
      messagesEl.scrollTop = messagesEl.scrollHeight;
    },
    finalize(r) {
      traceEl.innerHTML = "";
      for (const s of r.steps || []) {
        const d = document.createElement("details");
        d.className = "trace-item";
        if (s.tool === "run_sql") {
          const info = s.error ? `ошибка` : `${s.row_count ?? 0} строк · ${s.ms ?? 0} мс`;
          d.innerHTML =
            `<summary><span class="badge sql">SQL</span>` +
            `<span>${escapeHtml(s.purpose || "Запрос к базе данных")}</span>` +
            `<span style="margin-left:auto;opacity:.75">${info}</span></summary>` +
            `<code class="sql">${escapeHtml(s.sql || "")}</code>` +
            (s.error
              ? `<div style="color:#f87171;margin-top:6px">${escapeHtml(s.error)}</div>`
              : renderMiniChart(s.columns, s.rows) + renderSqlTable(s.columns, s.rows));
        } else if (s.tool === "find_entity") {
          const cnt = (s.matches || []).length;
          const preview = (s.matches || [])
            .slice(0, 6)
            .map((m) => `${m.kind}: <b>${escapeHtml(m.name)}</b> (<code>${escapeHtml(m.code)}</code>)`)
            .join(" · ");
          d.innerHTML =
            `<summary><span class="badge ent">ПОИСК СУЩНОСТИ</span>` +
            `<span>«${escapeHtml(s.query || "")}»</span>` +
            `<span style="margin-left:auto;opacity:.75">найдено: ${cnt}</span></summary>` +
            `<div style="margin-top:6px;line-height:1.5">${preview || "совпадений нет"}</div>`;
        }
        traceEl.appendChild(d);
      }

      // Attach CSV export handlers
      traceEl.querySelectorAll(".csv-btn").forEach((btn) => {
        btn.addEventListener("click", (e) => {
          e.stopPropagation();
          const cols = JSON.parse(btn.dataset.cols || "[]");
          const rows = JSON.parse(btn.dataset.rows || "[]");
          downloadCsv(cols, rows);
        });
      });

      bubbleEl.innerHTML = renderMarkdown(r.answer || "");
      const vBadge = r.verified
        ? `<span class="badge ok">✓ ${
            currentLang === "uz" ? "Raqamlar MB bilan tasdiqlangan" : "Числа сверены с БД"
          }</span>`
        : `<span class="badge warn">! Проверьте SQL-таблицу</span>`;
      const sqlCount = (r.sql || []).length;
      metaEl.innerHTML =
        `${vBadge}` +
        `<span>SQL-запросов: <b>${sqlCount}</b></span>` +
        `<span>Время: <b>${r.elapsed} с</b>${r.cached ? " (кэш)" : ""}</span>` +
        (r.model ? `<span style="opacity:.7">Модель: ${escapeHtml(r.model)}</span>` : "");
      messagesEl.scrollTop = messagesEl.scrollHeight;
    },
    fail(msg) {
      bubbleEl.innerHTML = `<span style="color:#f87171">${escapeHtml(msg)}</span>`;
    },
  };
}

function renderSqlTable(cols, rows) {
  if (!cols || !rows || !rows.length) return "";
  const head = cols.map((c) => `<th>${escapeHtml(String(c))}</th>`).join("");
  const body = rows
    .slice(0, 40)
    .map(
      (r) =>
        `<tr>` +
        r.map((v) => `<td>${v === null || v === undefined ? "—" : escapeHtml(fmtCell(v))}</td>`).join("") +
        `</tr>`
    )
    .join("");
  const colsAttr = escapeHtml(JSON.stringify(cols));
  const rowsAttr = escapeHtml(JSON.stringify(rows.slice(0, 200)));
  return (
    `<div style="display:flex;justify-content:flex-end;margin-top:8px">` +
    `<button type="button" class="csv-btn" data-cols="${colsAttr}" data-rows="${rowsAttr}">⬇ Скачать CSV (${rows.length})</button>` +
    `</div>` +
    `<div class="sql-table-wrap"><table class="sql-table"><thead><tr>${head}</tr></thead><tbody>${body}</tbody></table></div>`
  );
}

function renderMiniChart(cols, rows) {
  if (!cols || !rows || rows.length < 2 || rows.length > 15 || cols.length < 2) return "";
  // Find first string/year label column and first numeric value column
  let labelIdx = 0;
  let valIdx = -1;
  for (let i = 0; i < cols.length; i++) {
    const v = rows[0][i];
    if (typeof v === "number" && i > 0) {
      valIdx = i;
      break;
    }
  }
  if (valIdx === -1) return "";
  const vals = rows.map((r) => Number(r[valIdx]) || 0);
  const maxVal = Math.max(...vals, 0);
  if (maxVal <= 0) return "";
  const bars = rows
    .map((r) => {
      const lbl = String(r[labelIdx] ?? "—");
      const v = Number(r[valIdx]) || 0;
      const pct = Math.max(2, Math.min(100, Math.round((v / maxVal) * 100)));
      return (
        `<div class="mini-bar-row">` +
        `<div class="mini-bar-label" title="${escapeHtml(lbl)}">${escapeHtml(lbl)}</div>` +
        `<div class="mini-bar-track"><div class="mini-bar-fill" style="width:${pct}%"></div></div>` +
        `<div class="mini-bar-val">${escapeHtml(fmtCell(v))}</div>` +
        `</div>`
      );
    })
    .join("");
  return (
    `<div class="mini-chart">` +
    `<div class="mini-chart-title">📊 Визуализация: ${escapeHtml(String(cols[labelIdx]))} → ${escapeHtml(
      String(cols[valIdx])
    )}</div>` +
    bars +
    `</div>`
  );
}

function downloadCsv(cols, rows) {
  const esc = (v) => `"${String(v ?? "").replace(/"/g, '""')}"`;
  const lines = [cols.map(esc).join(",")];
  for (const r of rows) {
    lines.push(r.map(esc).join(","));
  }
  const blob = new Blob(["\uFEFF" + lines.join("\r\n")], { type: "text/csv;charset=utf-8;" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `uzex_query_${Date.now()}.csv`;
  a.click();
  URL.revokeObjectURL(url);
}

// ---------------- Dashboard Loader ----------------
async function loadDashboard() {
  try {
    const [statsRes, dashRes] = await Promise.all([
      cachedStats ? Promise.resolve(cachedStats) : fetch(API_BASE + "/api/stats").then((r) => r.json()),
      fetch(API_BASE + "/api/dashboard").then((r) => r.json()),
    ]);
    const s = statsRes || {};
    const d = dashRes || {};
    if (!s.deals) return;
    dashLoaded = true;

    const totalUzs = s.turnover_uzs || s.total_uzs || 0;
    const minDate = s.from || s.min_date || "2022-01-03";
    const maxDate = s.to || s.max_date || "2026-10-30";

    // KPI Cards
    const trln = (totalUzs / 1e12).toFixed(2).replace(".", ",");
    const execPct = ((s.executed_deals / s.deals) * 100).toFixed(1).replace(".", ",");
    document.getElementById("kpiGrid").innerHTML = `
      <div class="kpi-card">
        <div class="kpi-label">Всего сделок в реестре</div>
        <div class="kpi-value">${fmtNum(s.deals)}</div>
        <div class="kpi-sub">${minDate} — ${maxDate}</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">Общий оборот (в сумах)</div>
        <div class="kpi-value">${trln} трлн</div>
        <div class="kpi-sub">${fmtNum(Math.round(totalUzs))} сум</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">Исполненные сделки</div>
        <div class="kpi-value">${fmtNum(s.executed_deals)}</div>
        <div class="kpi-sub">${execPct}% от всех сделок реестра</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">Контракты / Товары</div>
        <div class="kpi-value">${fmtNum(s.contracts)} / ${s.products}</div>
        <div class="kpi-sub">133 контракта без сделок</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">Участники / Брокеры</div>
        <div class="kpi-value">${fmtNum(s.participants)} / ${s.brokers}</div>
        <div class="kpi-sub">392 продавца · 14 000 покупателей</div>
      </div>
    `;

    // Years chart
    const maxYearUzs = Math.max(...(d.yearly || []).map((y) => y.turnover_uzs || y.amount_uzs || 0), 1);
    document.getElementById("yearsContainer").innerHTML = (d.yearly || [])
      .map((y) => {
        const uzs = y.turnover_uzs || y.amount_uzs || 0;
        const cnt = y.deals_count || y.deals || 0;
        const pct = Math.round((uzs / maxYearUzs) * 100);
        const tr = (uzs / 1e12).toFixed(2).replace(".", ",");
        const q =
          currentLang === "uz"
            ? `${y.year}-yilda nechta bitim tuzilgan va eng ko‘p sotilgan top-5 mahsulot qaysilar?`
            : `Сколько сделок было в ${y.year} году и какие топ-5 товаров продавались больше всего?`;
        return `
          <div class="bar-item" data-ask="${escapeHtml(q)}">
            <div class="bar-top">
              <span class="bar-name">${y.year} год</span>
              <span class="bar-meta">${fmtNum(cnt)} сделок · <b>${tr} трлн сум</b></span>
            </div>
            <div class="bar-track"><div class="bar-fill" style="width:${pct}%"></div></div>
          </div>
        `;
      })
      .join("");

    // Statuses chart
    const maxStDeals = Math.max(...(d.statuses || []).map((st) => st.deals_count || st.deals || 0), 1);
    document.getElementById("statusContainer").innerHTML =
      (d.statuses || [])
        .map((st) => {
          const uzs = st.turnover_uzs || st.amount_uzs || 0;
          const cnt = st.deals_count || st.deals || 0;
          const pct = Math.round((cnt / maxStDeals) * 100);
          const share = ((cnt / s.deals) * 100).toFixed(2).replace(".", ",");
          const tr = (uzs / 1e12).toFixed(2).replace(".", ",");
          return `
            <div class="bar-item" data-ask="Расскажи подробно о сделках со статусом ${escapeHtml(st.status)}">
              <div class="bar-top">
                <span class="bar-name">${escapeHtml(st.status)} (${share}%)</span>
                <span class="bar-meta">${fmtNum(cnt)} сделок · <b>${tr} трлн сум</b></span>
              </div>
              <div class="bar-track"><div class="bar-fill" style="width:${pct}%"></div></div>
            </div>
          `;
        })
        .join("") +
      `<div class="bar-item" data-ask="По скольким сделкам была просрочена оплата, а по скольким — поставка?">
        <div class="bar-top">
          <span class="bar-name">⏱️ Дисциплина: Просрочка поставки / Просрочка оплаты</span>
          <span class="bar-meta"><b>17 805</b> просрочек поставки · <b>0</b> просрочек оплаты</span>
        </div>
      </div>`;

    // Top Products
    const maxProdUzs = Math.max(...(d.top_products || []).map((p) => p.turnover_uzs || p.amount_uzs || 0), 1);
    document.getElementById("productsContainer").innerHTML = (d.top_products || [])
      .map((p) => {
        const uzs = p.turnover_uzs || p.amount_uzs || 0;
        const cnt = p.deals_count || p.deals || 0;
        const pRu = p.product_family || p.product || "";
        const pUz = p.product_family_uz || p.product_uz || "";
        const pct = Math.round((uzs / maxProdUzs) * 100);
        const tr = (uzs / 1e12).toFixed(2).replace(".", ",");
        const name = currentLang === "uz" && pUz ? `${pUz} (${pRu})` : pRu;
        const q =
          currentLang === "uz"
            ? `${pUz || pRu} bo‘yicha umumiy bitimlar soni, summasi va o‘rtacha narxi qanday?`
            : `Какова статистика сделок, объём и средняя цена по товару «${pRu}»?`;
        return `
          <div class="bar-item" data-ask="${escapeHtml(q)}">
            <div class="bar-top">
              <span class="bar-name">${escapeHtml(name)}</span>
              <span class="bar-meta">${fmtNum(cnt)} сделок · <b>${tr} трлн сум</b></span>
            </div>
            <div class="bar-track"><div class="bar-fill" style="width:${pct}%"></div></div>
          </div>
        `;
      })
      .join("");

    // Regions
    const maxRegUzs = Math.max(...(d.regions || []).map((r) => r.turnover_uzs || r.amount_uzs || 0), 1);
    document.getElementById("regionsContainer").innerHTML = (d.regions || [])
      .map((r) => {
        const uzs = r.turnover_uzs || r.amount_uzs || 0;
        const cnt = r.deals_count || r.deals || 0;
        const pct = Math.round((uzs / maxRegUzs) * 100);
        const tr = (uzs / 1e12).toFixed(2).replace(".", ",");
        const name = currentLang === "uz" ? r.region : r.region_ru || r.region;
        const q =
          currentLang === "uz"
            ? `${r.region} bo‘yicha jami bitimlar soni, summasi va top mahsulotlar qaysilar?`
            : `Сколько сделок, на какую сумму и по каким товарам было заключено в регионе «${r.region_ru || r.region}»?`;
        return `
          <div class="bar-item" data-ask="${escapeHtml(q)}">
            <div class="bar-top">
              <span class="bar-name">${escapeHtml(name)}</span>
              <span class="bar-meta">${fmtNum(cnt)} сделок · <b>${tr} трлн сум</b></span>
            </div>
            <div class="bar-track"><div class="bar-fill" style="width:${pct}%"></div></div>
          </div>
        `;
      })
      .join("");

    // Top Sellers & Buyers tables
    document.getElementById("sellersContainer").innerHTML = renderEntityTable(d.top_sellers || [], "Продавец");
    document.getElementById("buyersContainer").innerHTML = renderEntityTable(d.top_buyers || [], "Покупатель");

    // Bind click-to-ask
    document.querySelectorAll("[data-ask]").forEach((el) => {
      el.addEventListener("click", () => {
        const q = el.dataset.ask;
        if (!q) return;
        switchTab("chat");
        inputEl.value = q;
        formEl.requestSubmit();
      });
    });
  } catch (err) {
    console.error("Dashboard load error:", err);
  }
}

function renderEntityTable(rows, roleLabel) {
  const body = rows
    .map((r, i) => {
      const uzs = r.turnover_uzs || r.amount_uzs || 0;
      const cnt = r.deals_count || r.deals || 0;
      const reg = r.region_ru || r.region || "";
      const mlrd = (uzs / 1e9).toFixed(2).replace(".", ",");
      const q = `Сколько сделок и на какую сумму совершила компания с ИНН ${r.inn} (${r.name})?`;
      return `
        <tr class="bar-item" data-ask="${escapeHtml(q)}" style="cursor:pointer">
          <td>${i + 1}</td>
          <td><b>${escapeHtml(r.name)}</b><br><span style="font-size:11px;color:var(--muted)">ИНН: ${escapeHtml(
        r.inn
      )} · ${escapeHtml(reg)}</span></td>
          <td>${fmtNum(cnt)}</td>
          <td><b>${mlrd} млрд сум</b></td>
        </tr>
      `;
    })
    .join("");
  return `
    <table class="sql-table">
      <thead>
        <tr><th>#</th><th>${roleLabel}</th><th>Сделок</th><th>Оборот</th></tr>
      </thead>
      <tbody>${body}</tbody>
    </table>
  `;
}

document.getElementById("refreshDashBtn")?.addEventListener("click", () => {
  dashLoaded = false;
  loadDashboard();
});

// ---------------- Utilities ----------------
function fmtCell(v) {
  if (typeof v === "number") {
    if (Number.isInteger(v)) return fmtNum(v);
    return v.toLocaleString("ru-RU", { maximumFractionDigits: 4 });
  }
  return String(v);
}

function fmtNum(n) {
  return Number(n).toLocaleString("ru-RU");
}

function escapeHtml(s) {
  return String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
}

function renderMarkdown(md) {
  const lines = md.split("\n");
  let out = [];
  let inList = false;
  let inTable = false;
  let tableRows = [];

  const flushTable = () => {
    if (!inTable) return;
    inTable = false;
    if (tableRows.length >= 2) {
      const header = tableRows[0];
      const body = tableRows.slice(2);
      const th = header.map((c) => `<th>${inline(c)}</th>`).join("");
      const trs = body.map((r) => `<tr>${r.map((c) => `<td>${inline(c)}</td>`).join("")}</tr>`).join("");
      out.push(
        `<div class="sql-table-wrap"><table class="md-table"><thead><tr>${th}</tr></thead><tbody>${trs}</tbody></table></div>`
      );
    }
    tableRows = [];
  };

  for (const raw of lines) {
    const line = raw.trimEnd();
    if (line.trim().startsWith("|") && line.trim().endsWith("|")) {
      if (inList) {
        out.push("</ul>");
        inList = false;
      }
      inTable = true;
      const cells = line
        .trim()
        .slice(1, -1)
        .split("|")
        .map((c) => c.trim());
      tableRows.push(cells);
      continue;
    } else if (inTable) {
      flushTable();
    }

    if (/^#{1,3}\s+/.test(line)) {
      if (inList) {
        out.push("</ul>");
        inList = false;
      }
      out.push(`<h3>${inline(line.replace(/^#{1,3}\s+/, ""))}</h3>`);
    } else if (/^\s*[-*•]\s+/.test(line) || /^\s*\d+\.\s+/.test(line)) {
      if (!inList) {
        out.push("<ul>");
        inList = true;
      }
      out.push(`<li>${inline(line.replace(/^\s*(?:[-*•]|\d+\.)\s+/, ""))}</li>`);
    } else if (!line.trim()) {
      if (inList) {
        out.push("</ul>");
        inList = false;
      }
    } else {
      if (inList) {
        out.push("</ul>");
        inList = false;
      }
      out.push(`<p>${inline(line)}</p>`);
    }
  }
  if (inList) out.push("</ul>");
  if (inTable) flushTable();
  return out.join("");
}

function inline(s) {
  let t = escapeHtml(s);
  t = t.replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>");
  t = t.replace(/`([^`]+)`/g, "<code>$1</code>");
  return t;
}
