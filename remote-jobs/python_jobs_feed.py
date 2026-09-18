"""Remote jobs matching keywords from 7 job boards, de-duplicated, newest first.

    python remote-jobs/python_jobs_feed.py python "data engineer"

Costs $1.80 per 1,000 jobs saved; duplicates and filtered-out jobs are free.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from apify_run import run_actor  # noqa: E402

keywords = sys.argv[1:] or ["python"]
jobs = run_actor("feedsmith/remote-jobs-aggregator", {
    "keywords": keywords,
    "postedWithinDays": 7,
    "includeDescription": False,
    "maxItems": 100,
})

print(f"{len(jobs)} remote jobs posted in the last 7 days matching {keywords}")
for job in jobs[:20]:
    salary = f"  [{job['salaryText']}]" if job.get("salaryText") else ""
    print(f"  {job['postedAt'][:10]}  {job['title'][:48]:48s} @ {(job['company'] or '?')[:24]:24s} ({job['source']}){salary}")
