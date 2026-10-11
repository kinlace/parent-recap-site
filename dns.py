#!/usr/bin/env python3
"""Point parentrecap.com and www at GitHub Pages through Porkbun's API.

Reads PORKBUN_API_KEY and PORKBUN_SECRET_API_KEY from the environment.
Prints the plan and changes nothing unless run with --apply. Only the apex
and www address records are touched: gateway, MX and TXT records stay.
Pass --challenge <value> to also add GitHub's domain verification TXT record.
"""

import json
import os
import sys
import urllib.request

DOMAIN = "parentrecap.com"
API = "https://api.porkbun.com/api/json/v3"
ORG = "kinlace"

A = ["185.199.108.153", "185.199.109.153", "185.199.110.153", "185.199.111.153"]
AAAA = ["2606:50c0:8000::153", "2606:50c0:8001::153", "2606:50c0:8002::153", "2606:50c0:8003::153"]
# Record types that would clash with the new apex and www records
ADDRESS_TYPES = {"A", "AAAA", "ALIAS", "CNAME"}


def call(path, **body):
    body["apikey"] = os.environ["PORKBUN_API_KEY"]
    body["secretapikey"] = os.environ["PORKBUN_SECRET_API_KEY"]
    req = urllib.request.Request(
        f"{API}/{path}",
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req) as resp:
        out = json.load(resp)
    if out.get("status") != "SUCCESS":
        sys.exit(f"{path}: {out.get('message', out)}")
    return out


def show(records):
    for r in sorted(records, key=lambda r: (r["name"], r["type"], r["content"])):
        print(f"  {r['name']:<40} {r['type']:<6} {r['content']}")


def main():
    args = sys.argv[1:]
    apply = "--apply" in args
    challenge = args[args.index("--challenge") + 1] if "--challenge" in args else None

    records = call(f"dns/retrieve/{DOMAIN}")["records"]
    print("Zone now:")
    show(records)

    targets = {DOMAIN, f"www.{DOMAIN}"}
    drop = [r for r in records if r["name"] in targets and r["type"] in ADDRESS_TYPES]
    add = [("", "A", ip) for ip in A] + [("", "AAAA", ip) for ip in AAAA]
    add.append(("www", "CNAME", f"{ORG}.github.io"))
    if challenge:
        add.append((f"_github-pages-challenge-{ORG}", "TXT", challenge))

    print("\nDelete:")
    show(drop)
    print("Create:")
    for name, rtype, content in add:
        print(f"  {(name + '.' if name else '') + DOMAIN:<40} {rtype:<6} {content}")

    if not apply:
        print("\nDry run. Re-run with --apply to make these changes.")
        return

    for r in drop:
        call(f"dns/delete/{DOMAIN}/{r['id']}")
    for name, rtype, content in add:
        call(f"dns/create/{DOMAIN}", name=name, type=rtype, content=content, ttl="600")

    print("\nZone after:")
    show(call(f"dns/retrieve/{DOMAIN}")["records"])


if __name__ == "__main__":
    main()
