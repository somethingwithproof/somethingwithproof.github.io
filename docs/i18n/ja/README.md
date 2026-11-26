> [English](../../../README.md)

# somethingwithproof.github.io

https://somethingwithproof.github.io のソースコードです。生成されたドキュメントページを備えた公開リポジトリの静的ギャラリーを提供します。

## ビルド

Python 3.12 と GitHub CLI (`gh`) が必要です（サードパーティの Python 依存関係は不要です）。

```sh
python3 build.py --fetch   # refresh cache/ from GitHub, then build _site/
python3 build.py           # build from cache/
python3 -m http.server -d _site 8765
```

`content/sitemap.json` はセクション、トピック、リポジトリを定義します。手書きのページは `content/pages/` に配置されます。プロジェクトページは、許可リスト方式の HTML サニタイザーを通したリポジトリの README から生成されます。記載されたリポジトリのいずれかがプライベートである場合、または生成された色のコントラスト比が 4.5:1 を下回る場合、ビルドは失敗します。

## ローカライズ

UI クローム、ナビゲーション、検索、およびラベルは `locales/` 配下に 45 ロケール（Tier 1 が 20、アフリカ地域が 15、アジア地域が 10）で同梱されています。

- 静的 HTML のデフォルトは英語であり、`python3 build.py --lang <locale>` で任意のロケール向けにビルドできます。
- ヘッダーには `/assets/locales/*.json` を参照する言語スイッチャーが備わっており、ブラウザ言語の自動検出および RTL ロケール（`ar`、`ar-EG`、`ar-MA`、`fa`、`he`、`ur`）の `dir="rtl"` をサポートします。
- ローカルでの検証は `python3 -m unittest discover -s tests` で行います。

## デプロイとライセンス

`.github/workflows/pages.yml` は `main` へのプッシュごと、および毎日 GitHub Pages へのビルドとデプロイを実行します。詳細は[英語版 README](../../../README.md)および [LICENSE](../../../LICENSE) を参照してください。
