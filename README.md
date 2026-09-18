# feedsmith examples

Small, runnable Python examples for the [feedsmith](https://apify.com/feedsmith) data Actors on Apify.
Each script is under 60 lines, uses only `requests`, and writes a CSV you can open in Excel or Google Sheets.

| Example | What you get | Actor | Price |
| --- | --- | --- | --- |
| [`tech-stack/find_shopify_klaviyo.py`](tech-stack/find_shopify_klaviyo.py) | Which sites in your list run Shopify **and** Klaviyo (swap in any technologies) | [Tech Stack Detector](https://apify.com/feedsmith/tech-stack-detector), a Wappalyzer / BuiltWith alternative | $0.02 per site |
| [`polymarket/top_markets_to_csv.py`](polymarket/top_markets_to_csv.py) | Most traded open Polymarket markets with implied probability, 24h volume, liquidity | [Polymarket API](https://apify.com/feedsmith/polymarket-markets-scraper) | $1.50 per 1,000 markets |
| [`airbnb/city_price_summary.py`](airbnb/city_price_summary.py) | Airbnb listings for a city and dates + nightly price stats by room type | [Airbnb API](https://apify.com/feedsmith/airbnb-listings-scraper) | $1.20 per 1,000 listings |
| [`remote-jobs/python_jobs_feed.py`](remote-jobs/python_jobs_feed.py) | Remote jobs matching keywords from 7 job boards, de-duplicated | [Remote Jobs API](https://apify.com/feedsmith/remote-jobs-aggregator) | $1.80 per 1,000 jobs |

## Run

```bash
pip install -r requirements.txt
export APIFY_TOKEN=apify_api_...   # Apify Console > Settings > API & Integrations
python tech-stack/find_shopify_klaviyo.py tech-stack/sample_domains.txt matches.csv
python polymarket/top_markets_to_csv.py bitcoin
python airbnb/city_price_summary.py "Lisbon, Portugal" 2026-11-06 2026-11-09
python remote-jobs/python_jobs_feed.py python "data engineer"
```

A free Apify account includes monthly platform credit, which covers several runs of every example.
All calls go through [`apify_run.py`](apify_run.py), which uses Apify's `run-sync-get-dataset-items` endpoint:
one HTTP request starts the Actor, waits for it to finish and returns the results as JSON.

## Real output (captured 2026-09-18)

```text
$ python tech-stack/find_shopify_klaviyo.py tech-stack/sample_domains.txt matches.csv
13 sites analysed, 4 run both Shopify and Klaviyo -> matches.csv
   www.glossier.com
   kyliecosmetics.com
   www.taylorstitch.com
   www.tentree.com

$ python polymarket/top_markets_to_csv.py bitcoin
   98.9%  Will the price of Bitcoin be above $76,000 on September 18?
   69.5%  Will Bitcoin reach $80,000 in September?

$ python remote-jobs/python_jobs_feed.py python
  2026-09-18  AI Engineer        @ Imaginary Cloud   (himalayas)  [€25,470 - €65,785 / yearly]
  2026-09-15  Senior Backend Developer (Python) @ Proxify AB (weworkremotely)
```

## Notes

- Each Actor's page documents every input field, the full output schema and its limits.
- Tech Stack Detector reads a site's HTML and headers without a browser, so technologies that only appear after
  JavaScript runs are not detected, and sites that block non-browser clients return few signals.
- Remote job listings keep a link back to the original posting (`url`, `source`); follow each board's terms if you
  republish them.
- Not affiliated with Polymarket, Airbnb, Shopify, Klaviyo, Wappalyzer or BuiltWith.

MIT licensed.
