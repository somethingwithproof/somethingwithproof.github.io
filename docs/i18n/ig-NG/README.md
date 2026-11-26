> [English](../../../README.md)

# somethingwithproof.github.io

Isi mmalite maka https://somethingwithproof.github.io: ebe ngosi kwụ ọtọ nke ebe nchekwa ọha nwere peeji akwụkwọ ntụziaka e mepụtara.

## Mwube

Chọrọ Python 3.12 na GitHub CLI (`gh`), na-enweghị ndabere Python sitere na ndị ọzọ:

```sh
python3 build.py --fetch   # refresh cache/ from GitHub, then build _site/
python3 build.py           # build from cache/
python3 -m http.server -d _site 8765
```

`content/sitemap.json` na-akọwa ngalaba, isiokwu, na ebe nchekwa. Peeji e ji aka dee dị na `content/pages/`. A na-emepụta peeji ọrụ site na README ebe nchekwa ndị gafere n'ime ihe nhicha HTML nke ndepụta e kwere. Mwube na-ada ma ọ bụrụ na ebe nchekwa ọ bụla e depụtara bụ nkeonwe ma ọ bụ ma ọ bụrụ na ọdịiche agba ọ bụla e mepụtara daa n'okpuru 4.5:1.

## Nkwado asụsụ obodo

Ihu njikọ UI, igodo, nchọta, na akara na-abịa n'asụsụ obodo 45 n'okpuru `locales/` (asụsụ Tier 1 20, asụsụ Afrịka 15, na asụsụ Eshia 10).

- HTML kwụ ọtọ na-amalite na Bekee ma enwere ike iwu ya n'asụsụ obodo ọ bụla site na `python3 build.py --lang <locale>`.
- Isi peeji na-enye mgbanwe asụsụ nke `/assets/locales/*.json` na-akwado nwere nchọpụta asụsụ ihe nchọgharị akpaaka na nkwado `dir="rtl"` maka asụsụ obodo RTL (`ar`, `ar-EG`, `ar-MA`, `fa`, `he`, `ur`).
- Nyochaa n'ime kọmputa gị site na `python3 -m unittest discover -s tests`.

## Ntinye n'ọrụ na Ikikere

`.github/workflows/pages.yml` na-ewu ma na-etinye n'ọrụ na GitHub Pages na ntinye ọ bụla na `main` yana kwa ụbọchị. Lee [README Bekee](../../../README.md) na [LICENSE](../../../LICENSE).
