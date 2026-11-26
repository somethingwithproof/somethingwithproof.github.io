// SPDX-FileCopyrightText: 2026 Thomas Vincent <thomasvincent@gmail.com>
// SPDX-License-Identifier: MIT

export const SUPPORTED_LOCALES = [
  "en", "de", "es", "fr", "it", "pt-BR", "nl", "ru", "uk",
  "ja", "ko", "zh-CN", "zh-TW", "ar", "hi", "pl", "tr", "sv", "vi", "id",
  "af-ZA", "am-ET", "ar-EG", "ar-MA", "fr-MA", "fr-SN", "ha-NG", "ig-NG",
  "mg-MG", "rw-RW", "so-SO", "sw-KE", "xh-ZA", "yo-NG", "zu-ZA",
  "bn", "fa", "he", "mr", "ta", "te", "th", "ur", "ms", "fil",
  "bs", "hr", "sr",
];

const RTL_LOCALES = new Set(["ar", "ar-EG", "ar-MA", "fa", "he", "ur"]);

const BASE_ALIASES = {
  af: "af-ZA",
  am: "am-ET",
  ha: "ha-NG",
  ig: "ig-NG",
  in: "id",
  iw: "he",
  mg: "mg-MG",
  pt: "pt-BR",
  rw: "rw-RW",
  so: "so-SO",
  sw: "sw-KE",
  tl: "fil",
  xh: "xh-ZA",
  yo: "yo-NG",
  zu: "zu-ZA",
};

const FALLBACK = {
  "search.empty": "No pages match.",
  "nav.home": "Home",
  "code.copy": "Copy",
  "code.copied": "Copied",
  "code.press_copy": "Press Cmd+C",
  "home.projects_shown": "{count} projects shown",
};

const cache = new Map();
let activeLocale = "en";
let activeCatalog = FALLBACK;
let applySeq = 0;

export function isRtl(locale) {
  return RTL_LOCALES.has(resolveLocale(locale));
}

export function resolveLocale(tag) {
  if (!tag || typeof tag !== "string") return "en";
  const clean = tag.trim().split(/[.@]/)[0].replaceAll("_", "-");
  const lower = clean.toLowerCase();
  if (!lower || lower === "c" || lower === "posix") return "en";
  if (["zh-tw", "zh-hk", "zh-mo", "zh-hant"].includes(lower) || lower.startsWith("zh-hant-")) return "zh-TW";
  if (["zh", "zh-cn", "zh-sg", "zh-hans"].includes(lower) || lower.startsWith("zh-hans-")) return "zh-CN";
  const exact = SUPPORTED_LOCALES.find((loc) => loc.toLowerCase() === lower);
  if (exact) return exact;
  const base = lower.split("-")[0];
  if (base === "zh") {
    if (lower.includes("-hans")) return "zh-CN";
    return /-hant|-tw|-hk|-mo/.test(lower) ? "zh-TW" : "zh-CN";
  }
  if (Object.hasOwn(BASE_ALIASES, base)) return BASE_ALIASES[base];
  return SUPPORTED_LOCALES.find((loc) => loc.toLowerCase() === base) || "en";
}

export function detectLocale() {
  try {
    const param = new URLSearchParams(location.search).get("lang");
    if (param) return resolveLocale(param);
  } catch { /* ignore */ }
  try {
    const saved = localStorage.getItem("lang");
    if (saved) return resolveLocale(saved);
  } catch { /* storage blocked */ }
  const langs = Array.isArray(navigator.languages) ? navigator.languages : [navigator.language];
  for (const cand of langs) {
    if (!cand) continue;
    const resolved = resolveLocale(cand);
    const low = String(cand).toLowerCase();
    if (resolved !== "en" || low === "en" || low.startsWith("en-")) return resolved;
  }
  return "en";
}

export function t(key, params = null) {
  let out = activeCatalog[key] ?? FALLBACK[key] ?? key;
  if (params) {
    for (const [k, v] of Object.entries(params)) {
      out = out.replaceAll(`{${k}}`, String(v));
    }
  }
  return out;
}

async function fetchCatalog(locale) {
  if (cache.has(locale)) return cache.get(locale);
  const res = await fetch(`/assets/locales/${locale}.json`);
  if (!res.ok) return FALLBACK;
  const data = await res.json();
  cache.set(locale, data);
  return data;
}

function applyTranslations(catalog) {
  for (const el of document.querySelectorAll("[data-i18n]")) {
    const key = el.dataset.i18n;
    if (catalog[key]) el.textContent = catalog[key];
  }
  for (const el of document.querySelectorAll("[data-i18n-placeholder]")) {
    const key = el.dataset.i18nPlaceholder;
    if (catalog[key]) el.setAttribute("placeholder", catalog[key]);
  }
  for (const el of document.querySelectorAll("[data-i18n-aria-label]")) {
    const key = el.dataset.i18nAriaLabel;
    if (catalog[key]) el.setAttribute("aria-label", catalog[key]);
  }
}

export async function applyLocale(locale, { persist = true } = {}) {
  const target = resolveLocale(locale);
  const seq = ++applySeq;
  let catalog = FALLBACK;
  try {
    catalog = await fetchCatalog(target);
  } catch { /* offline or file:// fallback keeps static HTML intact */ }
  if (seq !== applySeq) return;
  activeLocale = target;
  activeCatalog = catalog;
  document.documentElement.lang = activeLocale;
  document.documentElement.dir = isRtl(activeLocale) ? "rtl" : "ltr";
  if (persist) {
    try { localStorage.setItem("lang", activeLocale); } catch { /* ignore */ }
  }
  const select = document.querySelector("[data-lang-select]");
  if (select) select.value = activeLocale;
  applyTranslations(activeCatalog);
  document.dispatchEvent(new CustomEvent("localechange", { detail: { locale: activeLocale } }));
}

export function initI18n() {
  const select = document.querySelector("[data-lang-select]");
  const initial = detectLocale();
  if (select) {
    select.value = initial;
    select.addEventListener("change", () => {
      applyLocale(select.value, { persist: true }).catch(() => {});
    });
  }
  if (initial !== document.documentElement.lang || initial !== "en") {
    applyLocale(initial, { persist: false }).catch(() => {});
  }
}
