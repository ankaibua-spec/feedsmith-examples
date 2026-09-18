"""Save the most traded open Polymarket markets (odds, volume, liquidity) to a CSV.

    python polymarket/top_markets_to_csv.py [search words]

Examples: `python polymarket/top_markets_to_csv.py` (top 50 by 24h volume),
          `python polymarket/top_markets_to_csv.py bitcoin` (only markets mentioning bitcoin).
"""
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from apify_run import run_actor  # noqa: E402

search = " ".join(sys.argv[1:]) or None
actor_input = {"status": "open", "maxItems": 50, "minVolume": 1000}
if search:
    actor_input["search"] = search

markets = run_actor("feedsmith/polymarket-markets-scraper", actor_input)

with open("polymarket_markets.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["question", "yes_probability", "volume_24h_usd", "liquidity_usd", "closes", "url"])
    for m in markets:
        writer.writerow([m["question"], m["impliedProbability"], round(m["volume24h"] or 0),
                         round(m["liquidity"] or 0), m["closeTime"], m["url"]])

print(f"{len(markets)} markets -> polymarket_markets.csv")
for m in markets[:10]:
    p = m["impliedProbability"]
    print(f"  {p * 100:5.1f}%  {m['question'][:80]}" if p is not None else f"    n/a  {m['question'][:80]}")
