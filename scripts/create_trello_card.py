#!/usr/bin/env python3
"""
Create a Trello card (with checklists and check items) from a JSON spec.

The JSON spec follows the shape we agreed on in chat:
  [
    {
      "name": "Audit methodology",
      "desc": "...",
      "labels": [{"name": "Methodology", "color": "green"}, ...],
      "checklists": [
        {"name": "Content and substance", "checkItems": [
          {"name": "...", "state": "complete" | "incomplete"}, ...
        ]},
        ...
      ]
    }
  ]

Usage:
  Create a .env file in the same directory with:
    TRELLO_API_KEY=your-api-key
    TRELLO_TOKEN=your-token
  Then:
    python3 create_trello_card.py path/to/trello-audit-methodology-card.json

  Alternatively, export the variables in the shell:
    export TRELLO_API_KEY="..."
    export TRELLO_TOKEN="..."
    python3 create_trello_card.py path/to/card.json

  Shell-exported variables take precedence over .env values, useful for
  one-off overrides without editing the file.

  .env should NEVER be committed to git. If running this from inside a repo,
  add `.env` to .gitignore.

Get your API key + token from https://trello.com/power-ups/admin :
  1. Create a Power-Up (any workspace where you are admin, any name — it's
     just the container the API key gets tied to; you're not publishing
     anything).
  2. Open the Power-Up, "API key" tab → "Generate a new API Key" → that's
     your TRELLO_API_KEY.
  3. On the same page, click the "Token" link next to the API key → authorize
     your Power-Up to access your account → that's your TRELLO_TOKEN.

Note: an Atlassian API token (from id.atlassian.com) is NOT a Trello token —
Trello uses its own auth system even though it's owned by Atlassian.
"""

import json
import os
import sys
import time
from urllib.parse import urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

# ---------------------------------------------------------------------------
# Destination on the Eticas - Strategic Priorities board.
# These IDs come from the existing "Risk taxonomy" card. Change IDLIST if you
# want the new card to land in a different list on the same board.
# ---------------------------------------------------------------------------
IDBOARD = "69d406e1bd24d10e900236c2"
IDLIST = "69d406e1bd24d10e900236c0"

# Labels available on the board, keyed by name as they appear in the JSON.
# Same IDs as the taxonomy card uses.
LABEL_IDS = {
    "Methodology": "69e877e6ffdeadec4cc80e22",
    "Product": "69d406e1bd24d10e90023803",
}

TRELLO_API = "https://api.trello.com/1"


def load_dotenv(path=".env"):
    """Minimal .env loader. Parses KEY=value lines into os.environ.
    Already-exported shell variables take precedence (not overwritten)."""
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
            "Either create a .env file in this directory with:\n"
            "  TRELLO_API_KEY=your-api-key\n"
            "  TRELLO_TOKEN=your-token\n"
            "or export them in your shell.\n\n"
            "Get them from https://trello.com/power-ups/admin (create a Power-Up,\n"
            "go to its 'API key' tab to generate the key, then click the Token\n"
            "link on the same page to authorize and get the token).\n"
            "Note: an Atlassian API token from id.atlassian.com is NOT a Trello\n"
            "token — Trello uses a separate auth system."
        )
    return {"key": key, "token": token}


def trello_post(path, params):
    """POST to the Trello API. Auth params are added automatically."""
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


def create_card_from_spec(spec):
    # Resolve label IDs by name
    id_labels = []
    for label in spec.get("labels", []):
        name = label["name"]
        if name in LABEL_IDS:
            id_labels.append(LABEL_IDS[name])
        else:
            print(f"  warning: no known label ID for '{name}' — skipping")

    print(f"\nCreating card: {spec['name']}")
    card = trello_post("/cards", {
        "idList": IDLIST,
        "name": spec["name"],
        "desc": spec.get("desc", ""),
        "idLabels": ",".join(id_labels),
        "pos": "bottom",
    })
    print(f"  → {card['shortUrl']}")
    id_card = card["id"]

    for cl in spec.get("checklists", []):
        print(f"\n  Checklist: {cl['name']}")
        checklist = trello_post("/checklists", {
            "idCard": id_card,
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
            time.sleep(0.05)  # gentle pacing — Trello rate limits are generous but no need to push them

    return card


def main():
    if len(sys.argv) < 2:
        sys.exit("Usage: python3 create_trello_card.py path/to/card.json")
    with open(sys.argv[1]) as f:
        data = json.load(f)

    cards = data if isinstance(data, list) else [data]
    print(f"Found {len(cards)} card spec(s) in {sys.argv[1]}")
    for spec in cards:
        card = create_card_from_spec(spec)
    print(f"\nDone. Card URL: {card['shortUrl']}")


if __name__ == "__main__":
    main()
