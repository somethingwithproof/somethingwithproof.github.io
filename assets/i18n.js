// SPDX-FileCopyrightText: 2026 Thomas Vincent <thomasvincent@gmail.com>
// SPDX-License-Identifier: MIT

export const SUPPORTED_LOCALES = [
  "en", "de", "es", "fr", "it", "pt-BR", "nl", "ru", "uk",
  "ja", "ko", "zh-CN", "zh-TW", "ar", "hi", "pl", "tr", "sv", "vi", "id",
];

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

export function isRtl(locale) {
  return resolveLocale(locale) === "ar";
}

export function resolveLocale(tag) {
  if (!tag || typeof tag !== "string") return "en";
  const clean = tag.trim().split(/[.@]/)[0].replaceAll("_", "-");
  const lower = clean.toLowerCase();
  if (!lower || lower === "c" || lower === "posix") return "en";
  if (["zh-tw", "zh-hk", "zh-mo", "zh-hant"].includes(lower) || lower.startsWith("zh-hant-")) return "zh-TW";
  if (["zh", "zh-cn", "zh-sg", "zh-hans"].includes(lower) || lower.startsWith("zh-hans-")) return "zh-CN";
  if (lower === "pt" || lower === "pt-br") return "pt-BR";
  const exact = SUPPORTED_LOCALES.find((loc) => loc.toLowerCase() === lower);
  if (exact) return exact;
  const base = lower.split("-")[0];
  if (base === "zh") return /hant|-tw|-hk|-mo/.test(lower) ? "zh-TW" : "zh-CN";
  if (base === "pt") return "pt-BR";
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
  activeLocale = resolveLocale(locale);
  document.documentElement.lang = activeLocale;
  document.documentElement.dir = isRtl(activeLocale) ? "rtl" : "ltr";
  if (persist) {
    try { localStorage.setItem("lang", activeLocale); } catch { /* ignore */ }
  }
  const select = document.querySelector("[data-lang-select]");
  if (select) select.value = activeLocale;
  try {
    activeCatalog = await fetchCatalog(activeLocale);
    applyTranslations(activeCatalog);
  } catch { /* offline or file:// fallback keeps static HTML intact */ }
  document.dispatchEvent(new CustomEvent("localechange", { detail: { locale: activeLocale } }));
}

export function initI18n() {
  const select = document.querySelector("[data-lang-select]");
  const initial = detectLocale();
  if (select) {
    select.value = initial;
    select.addEventListener("change", () => {
      applyLocale(select.value, { persist: true });
    });
  }
  if (initial !== document.documentElement.lang) {
    applyLocale(initial, { persist: false });
  }
}
