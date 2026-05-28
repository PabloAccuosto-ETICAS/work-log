#!/usr/bin/env python3
"""
Replace all checklists on an existing Trello card with new ones from a JSON spec.

Companion to create_trello_card.py. Use this when a card already exists and
you want to refresh its checklist structure without touching the card's
identity (name, description, labels, comments, members are all preserved).

The JSON spec follows the same shape as create_trello_card.py — card-level
fields (name, desc, labels) are read but ignored, so the same spec file can
be used for either operation if convenient. Minimal shape:

  {
    "checklists": [
      {"name": "Content and substance", "checkItems": [
        {"name": "...", "state": "complete" | "incomplete"}, ...
      ]},
      ...
    ]
  }

Usage:
  Create a .env file in the same directory with:
    TRELLO_API_KEY=your-api-key
    TRELLO_TOKEN=your-token
  Then:
    python3 update_trello_card_checklists.py <card-shortLink-or-url> path/to/spec.json

  Examples:
    python3 update_trello_card_checklists.py kQBODkHQ leaflet-card-spec.json
    python3 update_trello_card_checklists.py https://trello.com/c/kQBODkHQ/6-ai-leaflet leaflet-card-spec.json

By default the script lists the existing checklists and asks for confirmation
before deleting them. Pass --no-confirm to skip the prompt (e.g., in scripted
contexts).

See create_trello_card.py for the API key + token generation flow.
"""

import json
import os
import re
import sys
import time
from urllib.parse import urlencode, urlparse
from urllib.request import urlopen, Request
from urllib.error import HTTPError

TRELLO_API = "https://api.trello.com/1"


def load_dotenv(path=".env"):
    """Minimal .env loader. Shell-exported variables take precedence."""
    if not os.path.exists(path):
        return
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                continue
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key and key not in os.environ:
                os.environ[key] = value


def get_auth():
    load_dotenv()
    key = os.environ.get("TRELLO_API_KEY")
    token = os.environ.get("TRELLO_TOKEN")
    if not key or not token:
        sys.exit(
            "ERROR: TRELLO_API_KEY and TRELLO_TOKEN not found.\n"
            "See create_trello_card.py docstring for the credentials flow."
        )
    return {"key": key, "token": token}


def parse_card_ref(ref):
    """Extract the shortLink from a card URL, or accept a bare shortLink."""
    if ref.startswith("http"):
        parsed = urlparse(ref)
        parts = parsed.path.strip("/").split("/")
        if len(parts) >= 2 and parts[0] == "c":
            return parts[1]
        sys.exit(f"Could not parse card URL: {ref}")
    if re.match(r"^[A-Za-z0-9]+$", ref):
        return ref
    sys.exit(f"Invalid card reference: {ref}")


def trello_get(path, params=None):
    auth = get_auth()
    qs = urlencode({**(params or {}), **auth})
    url = f"{TRELLO_API}{path}?{qs}"
    req = Request(url, method="GET")
    try:
        with urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        sys.exit(f"  HTTP {e.code} GET {path}\n  Response: {body}")


def trello_post(path, params):
    auth = get_auth()
    url = f"{TRELLO_API}{path}"
    data = urlencode({**params, **auth}).encode("utf-8")
    req = Request(url, data=data, method="POST")
    try:
        with urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        sys.exit(f"  HTTP {e.code} POST {path}\n  Response: {body}")


def trello_delete(path):
    auth = get_auth()
    qs = urlencode(auth)
    url = f"{TRELLO_API}{path}?{qs}"
    req = Request(url, method="DELETE")
    try:
        with urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        sys.exit(f"  HTTP {e.code} DELETE {path}\n  Response: {body}")


def update_card(card_ref, spec, no_confirm=False):
    short_link = parse_card_ref(card_ref)
    print(f"\nFetching card: {short_link}")
    card = trello_get(f"/cards/{short_link}", {"checklists": "all"})
    print(f"  → {card['name']} ({card['shortUrl']})")

    existing = card.get("checklists", [])
    if existing:
        print(f"\nExisting checklists ({len(existing)}):")
        for cl in existing:
            n = len(cl.get("checkItems", []))
            print(f"  - {cl['name']} ({n} items)")
        if not no_confirm:
            ans = input("\nDelete these and replace with the new spec? [y/N] ").strip().lower()
            if ans not in ("y", "yes"):
                sys.exit("Aborted.")
        for cl in existing:
            trello_delete(f"/checklists/{cl['id']}")
            print(f"  deleted: {cl['name']}")
            time.sleep(0.05)

    new_lists = spec.get("checklists", [])
    print(f"\nCreating {len(new_lists)} new checklist(s):")
    for cl in new_lists:
        print(f"\n  Checklist: {cl['name']}")
        checklist = trello_post("/checklists", {
            "idCard": card["id"],
            "name": cl["name"],
            "pos": "bottom",
        })
        id_checklist = checklist["id"]
        for item in cl.get("checkItems", []):
            checked = "true" if item.get("state") == "complete" else "false"
            trello_post(f"/checklists/{id_checklist}/checkItems", {
                "name": item["name"],
                "checked": checked,
                "pos": "bottom",
            })
            mark = "✓" if checked == "true" else "·"
            truncated = item["name"][:80] + ("…" if len(item["name"]) > 80 else "")
            print(f"    {mark} {truncated}")
            time.sleep(0.05)  # gentle pacing

    print(f"\nDone. Card URL: {card['shortUrl']}")


def main():
    args = [a for a in sys.argv[1:] if a != "--no-confirm"]
    no_confirm = "--no-confirm" in sys.argv[1:]
    if len(args) < 2:
        sys.exit(
            "Usage: python3 update_trello_card_checklists.py "
            "<card-shortLink-or-url> path/to/spec.json [--no-confirm]"
        )
    card_ref, spec_path = args[0], args[1]
    with open(spec_path) as f:
        spec = json.load(f)
    # If the spec is the list shape used by create_trello_card.py, unwrap it.
    if isinstance(spec, list):
        spec = spec[0] if spec else {}
    update_card(card_ref, spec, no_confirm=no_confirm)


if __name__ == "__main__":
    main()
