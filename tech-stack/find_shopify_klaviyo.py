"""Find which websites in a list run Shopify AND Klaviyo, and save them to a CSV.

    python tech-stack/find_shopify_klaviyo.py domains.txt matches.csv

domains.txt: one domain or URL per line. Costs $0.02 per analysed site (failed sites are free).
"""
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from apify_run import run_actor  # noqa: E402

REQUIRED = {"Shopify", "Klaviyo"}

domains_file = sys.argv[1] if len(sys.argv) > 1 else "tech-stack/sample_domains.txt"
out_file = sys.argv[2] if len(sys.argv) > 2 else "shopify_klaviyo.csv"
domains = [line.strip() for line in open(domains_file) if line.strip() and not line.startswith("#")]

sites = run_actor("feedsmith/tech-stack-detector", {
    "urls": domains,
    "technologies": sorted(REQUIRED),  # only report these two technologies
    "maxConcurrency": 10,
})

matches = [s for s in sites if s["status"] == "ok" and REQUIRED <= set(s["technologyNames"])]
with open(out_file, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["domain", "final_url", "title"])
    for s in matches:
        writer.writerow([s["domain"], s["finalUrl"], s.get("title") or ""])

print(f"{len(sites)} sites analysed, {len(matches)} run both Shopify and Klaviyo -> {out_file}")
for s in matches:
    print("  ", s["domain"])
