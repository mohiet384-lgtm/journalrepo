"""
fetch_indicator.py — Month 1 scaffold

Reads sources.yaml and fetches real indicator data. Deliberately REFUSES
to fetch anything marked verified: false, so the pipeline can never
silently populate the dataset with an unchecked or guessed URL.

Usage:
    python fetch_indicator.py --id 16 --out ../../data/raw/

Extend `fetch_api`, `fetch_bulk_download`, `fetch_scrape` per source as you
verify each one. This file intentionally ships with only ONE working
example (OpenAlex, id=16) since it's a free, no-auth-required API — use it
as the template for the rest.
"""
import argparse
import sys
from pathlib import Path

import requests
import yaml

SOURCES_FILE = Path(__file__).parent / "sources.yaml"


def load_sources():
    with open(SOURCES_FILE) as f:
        return yaml.safe_load(f)["indicators"]


def fetch_openalex_works(state_query: str, year: int) -> dict:
    """Example WORKING fetcher: counts India-affiliated works mentioning
    'artificial intelligence' for a given state name and year, via the
    free OpenAlex API (no key required). This is a real network call —
    it will fail in offline/sandboxed environments; run it in an
    environment with internet access."""
    params = {
        "search": f"artificial intelligence {state_query}",
        "filter": f"institutions.country_code:IN,publication_year:{year}",
        "per_page": 1,
    }
    r = requests.get("https://api.openalex.org/works", params=params, timeout=30)
    r.raise_for_status()
    data = r.json()
    return {"state": state_query, "year": year, "count": data.get("meta", {}).get("count")}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--id", type=int, required=True, help="indicator id from sources.yaml")
    ap.add_argument("--out", type=str, default="../../data/raw/")
    args = ap.parse_args()

    sources = load_sources()
    entry = next((s for s in sources if s["id"] == args.id), None)
    if entry is None:
        sys.exit(f"No entry for id={args.id} in sources.yaml")

    if not entry["verified"]:
        sys.exit(
            f"REFUSING to fetch indicator '{entry['name']}': marked verified: false "
            f"in sources.yaml. Open {entry.get('url') or '(no url yet)'} by hand, "
            f"confirm it is the correct dataset, then set verified: true."
        )

    if entry["name"] == "ai_research_output":
        print("Fetching a small real example from OpenAlex (id=16)...")
        sample = fetch_openalex_works("Kerala", 2023)
        print(sample)
    else:
        sys.exit(
            f"No fetcher implemented yet for '{entry['name']}'. "
            f"Add a fetch_* function for access_type={entry['access_type']}."
        )


if __name__ == "__main__":
    main()
