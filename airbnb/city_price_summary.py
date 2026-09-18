"""Pull Airbnb listings for a city and dates, then print nightly-price stats by room type.

    python airbnb/city_price_summary.py "Lisbon, Portugal" 2026-11-06 2026-11-09

Writes every listing to airbnb_listings.csv. Costs $1.20 per 1,000 listings.
"""
import csv
import statistics
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from apify_run import run_actor  # noqa: E402

city, check_in, check_out = (sys.argv[1:4] + [None, None, None])[:3]
city = city or "Porto, Portugal"
actor_input = {"locations": [city], "maxItems": 300, "exhaustive": True, "currency": "USD"}
if check_in and check_out:
    actor_input.update(checkIn=check_in, checkOut=check_out)

listings = run_actor("feedsmith/airbnb-listings-scraper", actor_input, timeout_secs=600)

fields = ["id", "name", "roomType", "priceNightly", "priceTotal", "nights", "rating", "reviewsCount", "latitude", "longitude", "url"]
with open("airbnb_listings.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
    writer.writeheader()
    writer.writerows(listings)

by_type = defaultdict(list)
for listing in listings:
    if listing.get("priceNightly"):
        by_type[listing.get("roomType") or "unknown"].append(listing["priceNightly"])

print(f"{len(listings)} listings in {city} -> airbnb_listings.csv")
if len(listings) >= actor_input["maxItems"]:
    # Exhaustive mode walks the city price band by price band, so a run cut off by maxItems is not a
    # representative sample. Raise maxItems until the run finishes below it before trusting these stats.
    print(f"  NOTE: stopped at maxItems={actor_input['maxItems']}; the stats below cover a partial, price-skewed sample.")
for room_type, prices in sorted(by_type.items(), key=lambda kv: -len(kv[1])):
    print(f"  {room_type:14s} n={len(prices):4d}  median ${statistics.median(prices):7.2f}/night  "
          f"p25 ${statistics.quantiles(prices, n=4)[0]:7.2f}  p75 ${statistics.quantiles(prices, n=4)[2]:7.2f}"
          if len(prices) >= 2 else f"  {room_type:14s} n={len(prices)}")
