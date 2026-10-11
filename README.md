# parentrecap.com

The homepage of [Kinlace Parent Recap](https://github.com/kinlace/parent-recap): one static `index.html`, no build step, no third-party requests.

Pushing to `main` deploys it to GitHub Pages (`.github/workflows/pages.yml`). Preview locally with `python3 -m http.server` and open `http://localhost:8000/?lang=fi` (`fi`, `en` or `zh`).

Facts about installing, privacy and what the AI sees belong to the [parent-recap README](https://github.com/kinlace/parent-recap#readme); the page links there instead of repeating them.

## DNS

`parentrecap.com` is registered at Porkbun. `dns.py` sets the records below through Porkbun's API, with the key in `PORKBUN_API_KEY` and `PORKBUN_SECRET_API_KEY` (API access must be on for the domain in Porkbun). It only prints the plan until run with `--apply`; `--challenge <value>` also adds GitHub's `_github-pages-challenge-kinlace` TXT record.

| Name | Type | Value |
| --- | --- | --- |
| `parentrecap.com` | A | `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153` |
| `parentrecap.com` | AAAA | `2606:50c0:8000::153`, `2606:50c0:8001::153`, `2606:50c0:8002::153`, `2606:50c0:8003::153` |
| `www` | CNAME | `kinlace.github.io` |

`gateway.parentrecap.com` points at the gateway server and is not part of this site.
