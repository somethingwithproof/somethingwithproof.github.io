# somethingwithproof.github.io

Source for https://somethingwithproof.github.io: a gallery of public projects with a documentation page for each repository.

## Build

Python 3.12 and the GitHub CLI, no other dependencies.

```sh
python3 build.py --fetch   # refresh cache/ from GitHub, then build _site/
python3 build.py           # build from cache/
python3 -m http.server -d _site 8765
```

`content/sitemap.json` defines the sections, topics and which repositories appear. Hand-written pages live in `content/pages/`. Project pages are generated from each repository's README, filtered through an allowlist sanitizer.

The build stops if a listed repository is private, or if any text colour pair falls below 4.5:1 contrast.

## Deploy

`.github/workflows/pages.yml` builds and deploys on every push to `main` and once a day.
