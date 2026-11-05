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
    statusOnline: "DuckDB Online",
    tabChat: "ИИ-Агент",
    tabDashboard: "Аналитика",
    tabArch: "О решении",
    tabChatMobile: "Чат с ИИ",
    tabDashboardMobile: "Аналитика",
    tabArchMobile: "О решении",
    btnNewChat: "Новый диалог",
    examplesTitle: "Примеры вопросов",
    mobileExamplesLabel: "Примеры:",
    filterAll: "Все",
    guaranteeTitle: "Гарантия точности (0% галлюцинаций)",
    g1: "<b>Только по данным DuckDB:</b> каждое число в ответе вычисляется реальным SQL-запросом по 500 000 сделкам.",
    g2: "<b>100% нормализация:</b> марки, сорта, классы и размеры извлечены даже из текстовых названий контрактов.",
    g3: "<b>Фонетический поиск RU↔UZ:</b> находит компании и брокеров независимо от латиницы, кириллицы и кавычек.",
    g4: "<b>Numeric Grounding Verifier:</b> автоматическая сверка каждого числа в тексте ответа с результатами SQL.",
    welcomeBadge: "SPOT.UZEX.UZ · 2022–2026 · ZERO-HALLUCINATION ENGINE",
    welcomeTitle: "Задайте любой вопрос о биржевых сделках на русском или узбекском",
    welcomeDesc:
      "Агент понимает русский и узбекский языки (латиницу и кириллицу), автоматически находит компании, брокеров, товары, марки и коды ТН ВЭД, выполняет точные SQL-запросы по 500 000 сделкам и показывает, на каких данных основан каждый ответ.",
    chipDeals: "500 000 сделок",
    chipContracts: "6 616 контрактов",
    chipParticipants: "14 392 участника",
    chipBrokers: "120 брокеров",
    chipRates: "1 765 курсов USD",
    chipCatalog: "41 товар · 14 регионов",
    welcomeQuickTitle: "Нажмите на пример вопроса для быстрой проверки:",
    placeholder: "Спросите на русском или узбекском (например: Сколько сделок по бензину АИ-92 было в 2025 году?)…",
    btnSend: "Спросить",
    dashTitle: "Аналитический обзор реестра сделок UZEX (2022–2026)",
    dashSub:
      "Все показатели рассчитаны напрямую из денормализованной базы DuckDB. Нажмите на любой товар, регион или компанию, чтобы задать вопрос ИИ-агенту.",
    btnRefresh: "↻ Обновить",
    chartYearsTitle: "Динамика оборота и сделок по годам (2022–2026)",
    chartStatusTitle: "Распределение сделок по статусам и дисциплине",
    chartProductsTitle: "Топ-12 биржевых товаров по сумме сделок (трлн сум)",
    chartRegionsTitle: "Регионы складской отгрузки по сумме сделок",
    chartSellersTitle: "Топ крупнейших продавцов (по обороту)",
    chartBuyersTitle: "Топ крупнейших покупателей (по обороту)",
    // Architecture Tab
    archBadge: "ОПИСАНИЕ РЕШЕНИЯ · АРХИТЕКТУРА И ВЕРИФИКАЦИЯ ОТВЕТОВ",
    archTitle: "Как устроен UZEX Spot AI и почему он не выдумывает ответы",
    archSub:
      "Архитектура разработана специально под требования конкурса: <b>точная аналитика по 500 000 сделкам</b>, <b>двуязычность (RU / UZ латиница и кириллица)</b>, <b>время ответа 2–7 секунд</b> (при лимите 90 сек) и <b>строгая верификация каждого числа против галлюцинаций</b>.",
    pipe1Title: "Каноническая нормализация и DuckDB",
    pipe1Desc:
      "Все 9 CSV-файлов (500 000 сделок, 6 616 контрактов, 14 392 участника, 120 брокеров, 1 765 курсов USD) объединены в колоночную БД <b>DuckDB</b>. Когда в карточке контракта поля <code>Марка</code>, <code>Сорт</code>, <code>Класс</code> или <code>Размер</code> пустые, но указаны внутри текста названия (<i>«Бензин АИ-92»</i>, <i>«Мука пшеничная В/С»</i>), нормализатор <code>src/normalize.py</code> извлекает <b>100% атрибутов по всем 697 комбинациям без единого пропуска</b>.",
    pipe2Title: "Кросс-скриптовый и фонетический индекс (RU ↔ UZ)",
    pipe2Desc:
      "Построен поисковый индекс <code>entity_index</code> (14 553 сущности) с двумя ключами: <code>translit_key</code> (транслитерация кириллицы/латиницы, очистка кавычек и ОПФ <i>MChJ, ООО, ҚК, ХК, АЖ</i>) и <code>phonetic_key</code> (унификация пар <code>q/k</code>, <code>h/x</code>, <code>o‘/u/o</code>, <code>ts/s</code>) + метрика <b>Jaro-Winkler</b>. Запрос <i>«Сотото Металл»</i> мгновенно находит <code>\"СОТЎТО МЕТАЛЛ\" МЧЖ (ИНН 917899526)</code>.",
    pipe3Title: "Агентное планирование + SQLGlot AST Sandbox",
    pipe3Desc:
      "Агент использует <b>Gemini Function Calling</b> (<code>find_entity</code> + <code>run_sql</code>) с температурой <code>0.0</code> и встроенным каталогом всех 41 семейств товаров и их марок. Каждый SQL-запрос перед выполнением проходит AST-валидацию через <b>SQLGlot</b> (разрешён только read-only <code>SELECT</code>). Вся математика выполняется внутри DuckDB за <b>5–25 мс</b>.",
    pipe4Title: "Numeric Grounding Verifier (Защита от галлюцинаций)",
    pipe4Desc:
      "Перед отправкой ответа модуль <code>ungrounded_numbers()</code> извлекает все числа и множители (<i>тыс., млн, млрд, трлн, %</i>) из текста ответа и сверяет каждое число с фактическими ячейками, возвращёнными SQL-запросами. Если товара или сущности нет в БД (например, <i>золото, нефть, ноябрь 2026</i>), агент прямо сообщает об отсутствии данных.",
    archNuancesTitle: "Ключевые особенности датасета, учтённые в системе",
    archEvalTitle: "Методика проверки и тестирования (Evaluation Suite)",
    nuancesList: [
      "<b>Двуязычные регионы:</b> в <code>deals/participants/brokers</code> регионы записаны на узбекской латинице с типографским апострофом (<code>Farg‘ona viloyati</code>), а в <code>contracts</code> — на русском (<code>Ферганская область</code>). В БД добавлены оба поля (<code>region</code> и <code>region_ru</code>) во все таблицы.",
      "<b>Двойные валюты (UZS и USD):</b> 493 410 внутренних сделок заключены в <code>UZS</code>, а 6 590 экспортных сделок (<i>Катод медный</i> и <i>Пряжа хлопчатобумажная</i>) — в <code>USD</code>. Поле <code>amount_uzs</code> автоматически конвертирует USD по курсу <code>usd_rates</code> на дату сделки.",
      "<b>Разные единицы измерения одного товара:</b> <i>Бензин</i> торгуется в <code>тоннах</code> и <code>литрах</code>, а <i>Дизельное топливо</i> — в <code>тоннах</code> и <code>килограммах</code>. Агент никогда не складывает тонны с литрами без группировки по <code>unit</code>.",
      "<b>Контракты и участники без сделок:</b> из 6 616 контрактов по 133 контрактам нет сделок; из 14 000 покупателей у 3 покупателей (ИНН <code>934519810</code>, <code>937876670</code>, <code>975709868</code>) 0 сделок.",
      "<b>Дисциплина оплаты и поставки:</b> просрочка оплаты (<code>is_late_payment</code>) = <b>0 сделок</b>; просрочка поставки (<code>is_late_delivery</code>) = <b>17 805 сделок</b>.",
    ],
    evalList: [
      "<b>Автоматический аудит нормализации:</b> скрипт проверяет все 697 уникальных комбинаций карточек контрактов и названий товаров — 0 пустых значений после нормализации.",
      "<b>Двуязычный бенчмарк (30+ вопросов RU / UZ-Latin / UZ-Cyrillic):</b> включает простые агрегации, вопросы с подвохом (марки внутри текста, тонны+литры, компании на кириллице, контракты без сделок, курс доллара) и вопросы по отсутствующим данным (золото, нефть, директор компании, ноябрь 2026).",
      "<b>Отказоустойчивый пул моделей (Multi-Key + Multi-Model Failover):</b> автоматическая балансировка между ключами Gemini API и быстрыми моделями семейства Gemini Flash гарантирует ответ за <b>2–7 секунд</b> (при лимите регламента 90 секунд).",
    ],
  },
  uz: {
    appTitle: "spot.uzex.uz birja bitimlari reyestri AI-agenti",
    statusOnline: "DuckDB Faol",
    tabChat: "AI-Agent",
    tabDashboard: "Tahlil",
    tabArch: "Yechim",
    tabChatMobile: "AI Chat",
    tabDashboardMobile: "Tahlil",
    tabArchMobile: "Yechim",
    btnNewChat: "Yangi suhbat",
    examplesTitle: "Namuna savollar",
    mobileExamplesLabel: "Namunalar:",
    filterAll: "Barchasi",
    guaranteeTitle: "Aniqlik kafolati (0% gallyutsinatsiya)",
    g1: "<b>Faqat DuckDB ma’lumotlari asosida:</b> javobdagi har bir raqam 500 000 ta bitim bo‘yicha real SQL-so‘rov orqali hisoblanadi.",
    g2: "<b>100% normalizatsiya:</b> marka, nav, sinf va o‘lchamlar shartnoma matnlaridan ham to‘liq ajratib olingan.",
    g3: "<b>Fonetik qidiruv RU↔UZ:</b> kompaniya va brokerlarni lotin, kirill yoki qo‘shtirnoqlardan qat’i nazar topadi.",
    g4: "<b>Numeric Grounding Verifier:</b> javobdagi har bir raqam SQL natijalari bilan avtomatik solishtiriladi.",
    welcomeBadge: "SPOT.UZEX.UZ · 2022–2026 · ZERO-HALLUCINATION ENGINE",
    welcomeTitle: "Birja bitimlari haqida o‘zbek yoki rus tilida istalgan savol bering",
    welcomeDesc:
      "Agent o‘zbek (lotin va kirill) hamda rus tillarini tushunadi, kompaniya, broker, mahsulot, marka va TIF TN kodlarini avtomatik topadi, 500 000 ta bitim bo‘yicha aniq SQL-so‘rovlarni bajaradi va javob qaysi ma’lumotlarga asoslanganini ko‘rsatadi.",
    chipDeals: "500 000 ta bitim",
    chipContracts: "6 616 ta shartnoma",
    chipParticipants: "14 392 ta ishtirokchi",
    chipBrokers: "120 ta broker",
    chipRates: "1 765 kunlik USD kursi",
    chipCatalog: "41 ta mahsulot · 14 ta hudud",
    welcomeQuickTitle: "Tezkor tekshirish uchun namuna savol ustiga bosing:",
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
    chartSellersTitle: "Top eng yirik sotuvchilar (aylanma bo‘yicha)",
    chartBuyersTitle: "Top eng yirik xaridorlar (aylanma bo‘yicha)",
    // Architecture Tab
    archBadge: "YECHIM TAVSIFI · ARXITEKTURA VA JAVOBLARNI TEKSHIRISH",
    archTitle: "UZEX Spot AI qanday ishlaydi va nima uchun javoblarni o‘ylab topmaydi",
    archSub:
      "Arxitektura tanlov talablari asosida ishlab chiqilgan: <b>500 000 ta bitim bo‘yicha aniq tahlil</b>, <b>ikki tillilik (O‘zbek lotin/kirill va Rus tili)</b>, <b>2–7 soniyada javob qaytarish</b> (90 soniya limit ichida) va <b>har bir raqamni gallyutsinatsiyaga qarshi qat’iy tekshirish</b>.",
    pipe1Title: "Kanonik normalizatsiya va DuckDB",
    pipe1Desc:
      "Barcha 9 ta CSV fayl (500 000 bitim, 6 616 shartnoma, 14 392 ishtirokchi, 120 broker, 1 765 USD kursi) ustunli <b>DuckDB</b> bazasiga birlashtirilgan. Shartnoma kartochkasida <code>Marka</code>, <code>Nav</code>, <code>Sinf</code> yoki <code>O‘lcham</code> bo‘sh qoldirilib, mahsulot nomida yozilgan bo‘lsa ham (masalan, <i>«Benzin AI-92»</i>), <code>src/normalize.py</code> moduli barcha <b>697 ta kombinatsiya bo‘yicha 100% atributlarni xatosiz ajratib oladi</b>.",
    pipe2Title: "Kross-skript va fonetik indeks (UZ ↔ RU)",
    pipe2Desc:
      "14 553 ta subyekt uchun ikki kalitli <code>entity_index</code> qidiruv indeksi qurilgan: <code>translit_key</code> (kirill/lotin transliteratsiyasi, qo‘shtirnoq va MChJ/XK/AJ qisqartmalarini tozalash) hamda <code>phonetic_key</code> (<code>q/k</code>, <code>h/x</code>, <code>o‘/u/o</code>, <code>ts/s</code> fonetik juftliklari) + <b>Jaro-Winkler</b> o‘xshashlik o‘lchovi. <i>«Sototo Metall»</i> so‘rovi darhol <code>\"СОТЎТО МЕТАЛЛ\" МЧЖ (STIR 917899526)</code> kompaniyasini topadi.",
    pipe3Title: "Agentli rejalashtirish + SQLGlot AST Sandbox",
    pipe3Desc:
      "Agent <code>0.0</code> haroratda <b>Gemini Function Calling</b> (<code>find_entity</code> + <code>run_sql</code>) va 41 ta mahsulot oilasi katalogidan foydalanadi. Har bir SQL-so‘rov bajarilishidan oldin <b>SQLGlot</b> AST-tekshiruvidan o‘tadi (faqat read-only <code>SELECT</code> ruxsat etilgan). Barcha hisob-kitoblar DuckDB ichida <b>5–25 ms</b> da bajariladi.",
    pipe4Title: "Numeric Grounding Verifier (Gallyutsinatsiyadan himoya)",
    pipe4Desc:
      "Javob foydalanuvchiga yuborilishidan oldin <code>ungrounded_numbers()</code> moduli matndagi barcha raqam va ko‘paytiruvchilarni (<i>ming, mln, mlrd, trln, %</i>) ajratib olib, SQL natijalari bilan solishtiradi. Agar so‘ralgan mahsulot yoki ma’lumot bazada mavjud bo‘lmasa (masalan, <i>oltin, neft, 2026-yil noyabr</i>), agent ma’lumot yo‘qligini ochiq aytadi.",
    archNuancesTitle: "Tizimda hisobga olingan ma’lumotlar bazasining asosiy xususiyatlari",
    archEvalTitle: "Javoblarni tekshirish va sinovdan o‘tkazish metodikasi (Evaluation Suite)",
    nuancesList: [
      "<b>Ikki tildagi hududlar:</b> <code>deals/participants/brokers</code> jadvallarida hududlar o‘zbek lotin yozuvida (<code>Farg‘ona viloyati</code>), <code>contracts</code> jadvalida esa rus tilida (<code>Ферганская область</code>) berilgan. Bazada barcha jadvallarga ikkala ustun (<code>region</code> va <code>region_ru</code>) qo‘shilgan.",
      "<b>Ikki xil valyuta (UZS va USD):</b> 493 410 ta ichki bitim <code>UZS</code> da, 6 590 ta eksport bitimi (<i>Mis katodi</i> va <i>Paxta kalavasi</i>) esa <code>USD</code> da tuzilgan. <code>amount_uzs</code> ustuni bitim sanasidagi <code>usd_rates</code> kursi bo‘yicha avtomatik hisoblangan.",
      "<b>Bitta mahsulotning turli o‘lchov birliklari:</b> <i>Benzin</i> <code>tonna</code> va <code>litrda</code>, <i>Dizel yoqilg‘isi</i> esa <code>tonna</code> va <code>kilogrammda</code> sotiladi. Agent tonna va litrni hech qachon <code>unit</code> bo‘yicha guruhlamasdan qo‘shib yubormaydi.",
      "<b>Bitimsiz shartnomalar va ishtirokchilar:</b> 6 616 ta shartnomadan 133 tasida bitimlar yo‘q; 14 000 ta xaridordan 3 tasida (STIR <code>934519810</code>, <code>937876670</code>, <code>975709868</code>) 0 ta bitim mavjud.",
      "<b>To‘lov va yetkazib berish intizomi:</b> to‘lov kechikishi (<code>is_late_payment</code>) = <b>0 ta bitim</b>; yetkazib berish kechikishi (<code>is_late_delivery</code>) = <b>17 805 ta bitim</b>.",
    ],
    evalList: [
      "<b>Normalizatsiya avtomatik auditi:</b> maxsus skript shartnoma kartochkalari va mahsulot nomlarining barcha 697 ta noyob kombinatsiyasini tekshiradi — normalizatsiyadan so‘ng 0 ta bo‘sh qiymat.",
      "<b>Ikki tilli benchmark (30+ savollar RU / UZ-Lotin / UZ-Kirill):</b> oddiy agregatsiyalar, murakkab savollar (matn ichidagi markalar, tonna+litr, kirilldagi kompaniya nomlari, bitimsiz shartnomalar, dollar kursi) va bazada yo‘q ma’lumotlar bo‘yicha savollarni (oltin, neft, kompaniya direktori, 2026-yil noyabr) o‘z ichiga oladi.",
      "<b>Barqaror modellar puli (Multi-Key + Multi-Model Failover):</b> Gemini API kalitlari va tezkor Gemini Flash modellari o‘rtasida avtomatik yuklama taqsimoti 90 soniyalik reglament ichida o‘rtacha <b>2–7 soniyada</b> javob qaytarishni kafolatlaydi.",
    ],
  },
};

const DEFAULT_TUNNEL_URL = "https://breach-adam-crew-wiley.trycloudflare.com";
const isStaticHost =
  window.location.hostname.endsWith(".netlify.app") ||
  window.location.hostname.endsWith(".github.io") ||
  window.location.hostname.endsWith(".vercel.app") ||
  window.location.protocol === "file:";

const API_BASE = (
  new URLSearchParams(window.location.search).get("api") ||
  localStorage.getItem("UZEX_API_BASE") ||
  window.UZEX_API_BASE ||
  (isStaticHost ? DEFAULT_TUNNEL_URL : "")
).replace(/\/+$/, "");

let currentLang = "ru";
let currentQFilter = "all";
const history = [];
let dashLoaded = false;
let cachedStats = null;
let cachedDash = null;

const messagesEl = document.getElementById("messages");
const formEl = document.getElementById("askForm");
const inputEl = document.getElementById("qInput");
const sendBtn = document.getElementById("sendBtn");
const clearBtn = document.getElementById("clearBtn");
const examplesEl = document.getElementById("examples");
const mobileExamplesEl = document.getElementById("mobileExamples");

// ---------------- Language & Examples ----------------
function askQuestion(q) {
  if (!q) return;
  switchTab("chat");
  inputEl.value = q;
  formEl.requestSubmit();
}

function renderExamples() {
  if (examplesEl) examplesEl.innerHTML = "";
  if (mobileExamplesEl) mobileExamplesEl.innerHTML = "";

  const list = EXAMPLES.filter((item) => {
    if (currentQFilter === "all") return true;
    return item.cat === currentQFilter;
  });

  for (const item of list) {
    if (examplesEl) {
      const b = document.createElement("button");
      b.type = "button";
      b.className = "ex-btn";
      const tagClass = item.cat === "guard" ? "guard" : item.lang === "uz" ? "uz" : "";
      const tagLabel = item.cat === "guard" ? "GUARD" : item.lang.toUpperCase();
      b.innerHTML = `<span class="tag ${tagClass}">${tagLabel}</span>${escapeHtml(item.q)}`;
      b.addEventListener("click", () => askQuestion(item.q));
      examplesEl.appendChild(b);
    }
  }

  // Mobile strip & Welcome grid prioritized by currentLang
  const langFirst = [
    ...EXAMPLES.filter((x) => x.lang === currentLang),
    ...EXAMPLES.filter((x) => x.lang !== currentLang),
  ];

  if (mobileExamplesEl) {
    for (const item of langFirst) {
      const chip = document.createElement("button");
      chip.type = "button";
      chip.className = "mobile-chip";
      chip.textContent = item.q;
      chip.addEventListener("click", () => askQuestion(item.q));
      mobileExamplesEl.appendChild(chip);
    }
  }

  const welcomeGrid = document.getElementById("welcomeQuickGrid");
  if (welcomeGrid) {
    welcomeGrid.innerHTML = "";
    for (const item of langFirst.slice(0, 6)) {
      const b = document.createElement("button");
      b.type = "button";
      b.className = "ex-btn";
      const tagClass = item.cat === "guard" ? "guard" : item.lang === "uz" ? "uz" : "";
      const tagLabel = item.cat === "guard" ? "GUARD" : item.lang.toUpperCase();
      b.innerHTML = `<span class="tag ${tagClass}">${tagLabel}</span>${escapeHtml(item.q)}`;
      b.addEventListener("click", () => askQuestion(item.q));
      welcomeGrid.appendChild(b);
    }
  }
}

function updateStatsLine() {
  const el = document.getElementById("statsline");
  if (!el) return;
  const s = cachedStats || {
    deals: 500000,
    contracts: 6616,
    participants: 14392,
    brokers: 120,
    from: "2022-01-03",
    to: "2026-10-30",
  };
  if (currentLang === "uz") {
    el.textContent =
      `${fmtNum(s.deals)} bitim · ${fmtNum(s.contracts)} shartnoma · ${fmtNum(s.participants)} ishtirokchi · ` +
      `${fmtNum(s.brokers)} broker · ${s.from || s.min_date} — ${s.to || s.max_date}`;
  } else {
    el.textContent =
      `${fmtNum(s.deals)} сделок · ${fmtNum(s.contracts)} контрактов · ${fmtNum(s.participants)} участников · ` +
      `${fmtNum(s.brokers)} брокеров · ${s.from || s.min_date} — ${s.to || s.max_date}`;
  }
}

function renderArchLists() {
  const dict = I18N[currentLang] || I18N.ru;
  const nuancesEl = document.getElementById("archNuancesList");
  const evalEl = document.getElementById("archEvalList");
  if (nuancesEl && dict.nuancesList) {
    nuancesEl.innerHTML = dict.nuancesList.map((li) => `<li>${li}</li>`).join("");
  }
  if (evalEl && dict.evalList) {
    evalEl.innerHTML = dict.evalList.map((li) => `<li>${li}</li>`).join("");
  }
}

function setLanguage(lang) {
  currentLang = lang;
  document.documentElement.lang = lang;
  document.querySelectorAll(".lang-btn").forEach((b) => {
    b.classList.toggle("active", b.dataset.lang === lang);
  });
  const dict = I18N[lang] || I18N.ru;
  document.querySelectorAll("[data-i18n]").forEach((el) => {
    const key = el.dataset.i18n;
    if (dict[key]) el.innerHTML = dict[key];
  });
  if (inputEl) inputEl.placeholder = dict.placeholder;
  updateStatsLine();
  renderExamples();
  renderArchLists();
  if (cachedDash && cachedStats) {
    renderDashboardData(cachedStats, cachedDash);
  }
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

setLanguage("ru");

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
fetch(API_BASE + "/api/stats")
  .then((r) => r.json())
  .then((s) => {
    if (s && s.deals) {
      cachedStats = s;
      updateStatsLine();
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
  messagesEl.querySelectorAll(".msg").forEach((m) => m.remove());
  const w = document.getElementById("welcome");
  if (w) w.style.display = "";
  messagesEl.scrollTop = 0;
  switchTab("chat");
});

formEl.addEventListener("submit", async (e) => {
  e.preventDefault();
  const q = inputEl.value.trim();
  if (!q) return;
  const w = document.getElementById("welcome");
  if (w) w.style.display = "none";

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
    if (!res.ok) {
      bot.fail(
        currentLang === "uz"
          ? `Server xatosi (HTTP ${res.status})`
          : `Ошибка сервера (HTTP ${res.status})`
      );
      return;
    }
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
        } else if (ev.type === "done" || ev.type === "final") {
          finalResult = ev.result || ev;
        } else if (ev.type === "error") {
          bot.fail((currentLang === "uz" ? "Server xatosi: " : "Ошибка сервера: ") + (ev.error || ""));
          return;
        }
      }
    }
    if (finalResult) {
      bot.finalize(finalResult);
      history.push({ q, a: finalResult.answer });
    } else {
      bot.fail(currentLang === "uz" ? "Serverdan bo‘sh javob keldi." : "Пустой ответ от сервера.");
    }
  } catch (err) {
    bot.fail((currentLang === "uz" ? "Ulanish xatosi: " : "Ошибка соединения: ") + err.message);
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
  const isUz = currentLang === "uz";
  const el = document.createElement("div");
  el.className = "msg bot";
  const traceEl = document.createElement("div");
  traceEl.className = "trace";
  const bubbleEl = document.createElement("div");
  bubbleEl.className = "bubble";
  bubbleEl.innerHTML = `<span class="spinner"></span> &nbsp;${
    isUz
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
      const uz = currentLang === "uz";
      const d = document.createElement("div");
      d.className = "trace-item";
      if (ev.tool === "run_sql") {
        d.innerHTML = `<span class="badge sql">SQL</span> ${escapeHtml(
          ev.args?.purpose || (uz ? "So‘rov bajarilmoqda…" : "Выполнение запроса…")
        )}`;
      } else if (ev.tool === "find_entity") {
        d.innerHTML = `<span class="badge ent">${uz ? "QIDIRUV" : "ПОИСК"}</span> «${escapeHtml(
          ev.args?.query || ""
        )}»`;
      }
      traceEl.appendChild(d);
      messagesEl.scrollTop = messagesEl.scrollHeight;
    },
    finalize(r) {
      const uz = currentLang === "uz";
      traceEl.innerHTML = "";
      for (const s of r.steps || []) {
        const d = document.createElement("details");
        d.className = "trace-item";
        if (s.tool === "run_sql") {
          const info = s.error
            ? uz
              ? "xato"
              : "ошибка"
            : `${s.row_count ?? 0} ${uz ? "qator" : "строк"} · ${s.ms ?? 0} ms`;
          d.innerHTML =
            `<summary><span class="badge sql">SQL</span>` +
            `<span>${escapeHtml(s.purpose || (uz ? "Ma’lumotlar bazasiga so‘rov" : "Запрос к базе данных"))}</span>` +
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
            `<summary><span class="badge ent">${uz ? "SUBYEKT QIDIRUVI" : "ПОИСК СУЩНОСТИ"}</span>` +
            `<span>«${escapeHtml(s.query || "")}»</span>` +
            `<span style="margin-left:auto;opacity:.75">${uz ? "topildi" : "найдено"}: ${cnt}</span></summary>` +
            `<div style="margin-top:6px;line-height:1.5">${
              preview || (uz ? "moslik topilmadi" : "совпадений нет")
            }</div>`;
        }
        traceEl.appendChild(d);
      }

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
        ? `<span class="badge ok">✓ ${uz ? "Raqamlar MB bilan tasdiqlangan" : "Числа сверены с БД"}</span>`
        : `<span class="badge warn">! ${uz ? "SQL-jadvalni tekshiring" : "Проверьте SQL-таблицу"}</span>`;
      const sqlCount = (r.sql || []).length;
      metaEl.innerHTML =
        `${vBadge}` +
        `<span>${uz ? "SQL-so‘rovlar" : "SQL-запросов"}: <b>${sqlCount}</b></span>` +
        `<span>${uz ? "Vaqt" : "Время"}: <b>${r.elapsed} s</b>${
          r.cached ? (uz ? " (kesh)" : " (кэш)") : ""
        }</span>` +
        (r.model ? `<span style="opacity:.7">${uz ? "Model" : "Модель"}: ${escapeHtml(r.model)}</span>` : "");
      messagesEl.scrollTop = messagesEl.scrollHeight;
    },
    fail(msg) {
      bubbleEl.innerHTML = `<span style="color:#f87171">${escapeHtml(msg)}</span>`;
    },
  };
}

function renderSqlTable(cols, rows) {
  if (!cols || !rows || !rows.length) return "";
  const uz = currentLang === "uz";
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
    `<button type="button" class="csv-btn" data-cols="${colsAttr}" data-rows="${rowsAttr}">⬇ ${
      uz ? "CSV yuklab olish" : "Скачать CSV"
    } (${rows.length})</button>` +
    `</div>` +
    `<div class="sql-table-wrap"><table class="sql-table"><thead><tr>${head}</tr></thead><tbody>${body}</tbody></table></div>`
  );
}

function renderMiniChart(cols, rows) {
  if (!cols || !rows || rows.length < 2 || rows.length > 15 || cols.length < 2) return "";
  const uz = currentLang === "uz";
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
    `<div class="mini-chart-title">📊 ${uz ? "Vizualizatsiya" : "Визуализация"}: ${escapeHtml(
      String(cols[labelIdx])
    )} → ${escapeHtml(String(cols[valIdx]))}</div>` +
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
      cachedDash ? Promise.resolve(cachedDash) : fetch(API_BASE + "/api/dashboard").then((r) => r.json()),
    ]);
    const s = statsRes || {};
    const d = dashRes || {};
    if (!s.deals) return;
    cachedStats = s;
    cachedDash = d;
    dashLoaded = true;
    renderDashboardData(s, d);
  } catch (err) {
    console.error("Dashboard load error:", err);
  }
}

function renderDashboardData(s, d) {
  const uz = currentLang === "uz";
  const totalUzs = s.turnover_uzs || s.total_uzs || 0;
  const minDate = s.from || s.min_date || "2022-01-03";
  const maxDate = s.to || s.max_date || "2026-10-30";

  const dealWord = uz ? "ta bitim" : "сделок";
  const trlnUnit = uz ? "trln so‘m" : "трлн сум";
  const sumUnit = uz ? "so‘m" : "сум";

  // KPI Cards
  const trln = (totalUzs / 1e12).toFixed(2).replace(".", ",");
  const execPct = ((s.executed_deals / s.deals) * 100).toFixed(1).replace(".", ",");
  document.getElementById("kpiGrid").innerHTML = `
    <div class="kpi-card">
      <div class="kpi-label">${uz ? "Reyestrdagi jami bitimlar" : "Всего сделок в реестре"}</div>
      <div class="kpi-value">${fmtNum(s.deals)}</div>
      <div class="kpi-sub">${minDate} — ${maxDate}</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">${uz ? "Umumiy aylanma (so‘mda)" : "Общий оборот (в сумах)"}</div>
      <div class="kpi-value">${trln} ${uz ? "trln" : "трлн"}</div>
      <div class="kpi-sub">${fmtNum(Math.round(totalUzs))} ${sumUnit}</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">${uz ? "Bajarilgan bitimlar" : "Исполненные сделки"}</div>
      <div class="kpi-value">${fmtNum(s.executed_deals)}</div>
      <div class="kpi-sub">${execPct}% ${uz ? "barcha bitimlardan" : "от всех сделок реестра"}</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">${uz ? "Shartnomalar / Mahsulotlar" : "Контракты / Товары"}</div>
      <div class="kpi-value">${fmtNum(s.contracts)} / ${s.products}</div>
      <div class="kpi-sub">${uz ? "133 ta shartnomada bitim yo‘q" : "133 контракта без сделок"}</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">${uz ? "Ishtirokchilar / Brokerlar" : "Участники / Брокеры"}</div>
      <div class="kpi-value">${fmtNum(s.participants)} / ${s.brokers}</div>
      <div class="kpi-sub">${
        uz ? "392 sotuvchi · 14 000 xaridor" : "392 продавца · 14 000 покупателей"
      }</div>
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
      const q = uz
        ? `${y.year}-yilda nechta bitim tuzilgan va eng ko‘p sotilgan top-5 mahsulot qaysilar?`
        : `Сколько сделок было в ${y.year} году и какие топ-5 товаров продавались больше всего?`;
      return `
        <div class="bar-item" data-ask="${escapeHtml(q)}">
          <div class="bar-top">
            <span class="bar-name">${y.year}-${uz ? "yil" : "год"}</span>
            <span class="bar-meta">${fmtNum(cnt)} ${dealWord} · <b>${tr} ${trlnUnit}</b></span>
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
        const q = uz
          ? `${st.status} holatidagi bitimlar haqida batafsil ma’lumot bering`
          : `Расскажи подробно о сделках со статусом ${st.status}`;
        return `
          <div class="bar-item" data-ask="${escapeHtml(q)}">
            <div class="bar-top">
              <span class="bar-name">${escapeHtml(st.status)} (${share}%)</span>
              <span class="bar-meta">${fmtNum(cnt)} ${dealWord} · <b>${tr} ${trlnUnit}</b></span>
            </div>
            <div class="bar-track"><div class="bar-fill" style="width:${pct}%"></div></div>
          </div>
        `;
      })
      .join("") +
    `<div class="bar-item" data-ask="${
      uz
        ? "Qancha bitim bo‘yicha to‘lov va yetkazib berish muddati kechikkan?"
        : "По скольким сделкам была просрочена оплата, а по скольким — поставка?"
    }">
      <div class="bar-top">
        <span class="bar-name">⏱️ ${
          uz ? "Intizom: Yetkazib berish va to‘lov kechikishi" : "Дисциплина: Просрочка поставки / оплаты"
        }</span>
        <span class="bar-meta"><b>17 805</b> ${
          uz ? "yetkazib berish · <b>0</b> to‘lov" : "просрочек поставки · <b>0</b> оплаты"
        }</span>
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
      const name = uz && pUz ? `${pUz} (${pRu})` : pRu;
      const q = uz
        ? `${pUz || pRu} bo‘yicha umumiy bitimlar soni, summasi va o‘rtacha narxi qanday?`
        : `Какова статистика сделок, объём и средняя цена по товару «${pRu}»?`;
      return `
        <div class="bar-item" data-ask="${escapeHtml(q)}">
          <div class="bar-top">
            <span class="bar-name">${escapeHtml(name)}</span>
            <span class="bar-meta">${fmtNum(cnt)} ${dealWord} · <b>${tr} ${trlnUnit}</b></span>
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
      const name = uz ? r.region : r.region_ru || r.region;
      const q = uz
        ? `${r.region} bo‘yicha jami bitimlar soni, summasi va top mahsulotlar qaysilar?`
        : `Сколько сделок, на какую сумму и по каким товарам было заключено в регионе «${r.region_ru || r.region}»?`;
      return `
        <div class="bar-item" data-ask="${escapeHtml(q)}">
          <div class="bar-top">
            <span class="bar-name">${escapeHtml(name)}</span>
            <span class="bar-meta">${fmtNum(cnt)} ${dealWord} · <b>${tr} ${trlnUnit}</b></span>
          </div>
          <div class="bar-track"><div class="bar-fill" style="width:${pct}%"></div></div>
        </div>
      `;
    })
    .join("");

  // Top Sellers & Buyers tables
  document.getElementById("sellersContainer").innerHTML = renderEntityTable(
    d.top_sellers || [],
    uz ? "Sotuvchi" : "Продавец"
  );
  document.getElementById("buyersContainer").innerHTML = renderEntityTable(
    d.top_buyers || [],
    uz ? "Xaridor" : "Покупатель"
  );

  // Bind click-to-ask
  document.querySelectorAll("[data-ask]").forEach((el) => {
    el.addEventListener("click", () => askQuestion(el.dataset.ask));
  });
}

function renderEntityTable(rows, roleLabel) {
  const uz = currentLang === "uz";
  const body = rows
    .map((r, i) => {
      const uzs = r.turnover_uzs || r.amount_uzs || 0;
      const cnt = r.deals_count || r.deals || 0;
      const reg = uz ? r.region || r.region_ru || "" : r.region_ru || r.region || "";
      const mlrd = (uzs / 1e9).toFixed(2).replace(".", ",");
      const q = uz
        ? `${r.inn} STIR raqamli (${r.name}) kompaniya nechta bitim va qancha summaga savdo qilgan?`
        : `Сколько сделок и на какую сумму совершила компания с ИНН ${r.inn} (${r.name})?`;
      return `
        <tr class="bar-item" data-ask="${escapeHtml(q)}" style="cursor:pointer">
          <td>${i + 1}</td>
          <td><b>${escapeHtml(r.name)}</b><br><span style="font-size:11px;color:var(--muted)">${
        uz ? "STIR" : "ИНН"
      }: ${escapeHtml(r.inn)} · ${escapeHtml(reg)}</span></td>
          <td>${fmtNum(cnt)}</td>
          <td><b>${mlrd} ${uz ? "mlrd so‘m" : "млрд сум"}</b></td>
        </tr>
      `;
    })
    .join("");
  return `
    <table class="sql-table">
      <thead>
        <tr><th>#</th><th>${roleLabel}</th><th>${uz ? "Bitimlar" : "Сделок"}</th><th>${
    uz ? "Aylanma" : "Оборот"
  }</th></tr>
      </thead>
      <tbody>${body}</tbody>
    </table>
  `;
}

document.getElementById("refreshDashBtn")?.addEventListener("click", () => {
  dashLoaded = false;
  cachedDash = null;
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
