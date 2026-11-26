# SPDX-FileCopyrightText: 2026 Thomas Vincent <thomasvincent@gmail.com>
# SPDX-License-Identifier: MIT

import json
import re
import tempfile
import unittest
from pathlib import Path

import build

PLACEHOLDER_RE = re.compile(r"\{[a-zA-Z0-9_]+\}")


def extract_placeholders(value: str) -> list[str]:
    return sorted(PLACEHOLDER_RE.findall(value))


class TestI18nCatalogs(unittest.TestCase):
    def test_all_20_tier1_locales_have_key_and_placeholder_parity(self):
        self.assertEqual(len(build.SUPPORTED_LOCALES), 20)
        catalogs = build.validate_locales()
        en = catalogs["en"]
        self.assertGreater(len(en), 0)

        for loc in build.SUPPORTED_LOCALES:
            self.assertIn(loc, build.LOCALE_NAMES)
            cat = catalogs[loc]
            self.assertEqual(set(cat.keys()), set(en.keys()), f"key mismatch for {loc}")
            for key, en_val in en.items():
                loc_val = cat[key]
                self.assertIsInstance(loc_val, str)
                self.assertTrue(loc_val.strip(), f"empty value for {loc}.{key}")
                self.assertEqual(
                    extract_placeholders(loc_val),
                    extract_placeholders(en_val),
                    f"placeholder mismatch for {loc}.{key}",
                )

    def test_locale_resolution_and_rtl(self):
        self.assertEqual(build.resolve_locale(""), "en")
        self.assertEqual(build.resolve_locale("C"), "en")
        self.assertEqual(build.resolve_locale("POSIX"), "en")
        self.assertEqual(build.resolve_locale("pt_BR.UTF-8"), "pt-BR")
        self.assertEqual(build.resolve_locale("zh-CN"), "zh-CN")
        self.assertEqual(build.resolve_locale("zh-Hant-TW"), "zh-TW")
        self.assertEqual(build.resolve_locale("ar-SA"), "ar")
        self.assertEqual(build.resolve_locale("hi-IN"), "hi")
        self.assertEqual(build.resolve_locale("unknown"), "en")

        for loc in build.SUPPORTED_LOCALES:
            self.assertEqual(build.is_rtl(loc), loc == "ar")

    def test_build_outputs_locales_switcher_and_rtl(self):
        orig_cache = build.CACHE
        orig_out = build.OUT
        try:
            with tempfile.TemporaryDirectory() as tmp:
                tmp_path = Path(tmp)
                cache_dir = tmp_path / "cache"
                out_dir = tmp_path / "_site"
                cache_dir.mkdir()
                build.CACHE = cache_dir
                build.OUT = out_dir

                (cache_dir / "_user.json").write_text(json.dumps({
                    "login": "somethingwithproof",
                    "avatar_url": "https://avatars.githubusercontent.com/u/1",
                    "html_url": "https://github.com/somethingwithproof",
                    "created_at": "2020-01-01T00:00:00Z",
                    "public_repos": 1,
                }))
                (cache_dir / "demo.json").write_text(json.dumps({
                    "name": "demo",
                    "description": "Demo repo",
                    "language": "Python",
                    "html_url": "https://github.com/somethingwithproof/demo",
                    "private": False,
                    "archived": False,
                    "fork": False,
                    "pushed_at": "2026-01-01T00:00:00Z",
                    "default_branch": "main",
                    "topics": [],
                    "stargazers_count": 1,
                    "license": "MIT",
                    "created_at": "2025-01-01T00:00:00Z",
                    "homepage": None,
                    "open_issues_count": 0,
                    "parent": None,
                    "release": None,
                    "milestones": [],
                    "docs": [],
                    "commits": [],
                }))
                (cache_dir / "demo.html").write_text("<p>Demo README</p>")

                site = {
                    "owner": "somethingwithproof",
                    "title": "somethingwithproof",
                    "tagline": "Test tagline.",
                    "intro": "Test intro.",
                    "sections": [
                        {
                            "slug": "tools",
                            "name": "Tools",
                            "blurb": "Tooling.",
                            "topics": [
                                {
                                    "slug": "demo",
                                    "name": "Demo",
                                    "blurb": "Demo topic.",
                                    "pages": [{"repo": "demo"}],
                                }
                            ],
                        }
                    ],
                }

                build.build(site, locale="en")
                home_en = (out_dir / "index.html").read_text(encoding="utf-8")
                self.assertIn('<html lang="en">', home_en)
                self.assertIn('data-lang-select', home_en)
                self.assertIn('<option value="ar">العربية</option>', home_en)
                for loc in build.SUPPORTED_LOCALES:
                    self.assertTrue((out_dir / "assets" / "locales" / f"{loc}.json").is_file())

                build.build(site, locale="ar")
                home_ar = (out_dir / "index.html").read_text(encoding="utf-8")
                self.assertIn('<html lang="ar" dir="rtl">', home_ar)
        finally:
            build.CACHE = orig_cache
            build.OUT = orig_out


if __name__ == "__main__":
    unittest.main()
