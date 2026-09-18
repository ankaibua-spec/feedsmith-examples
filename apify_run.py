"""Tiny helper: run an Apify Actor synchronously and return its dataset items.

Needs one environment variable, APIFY_TOKEN (Apify Console > Settings > API & Integrations).
The free Apify plan includes monthly credit, enough to run every example here several times.
"""
import os
import sys

import requests


def run_actor(actor_id: str, actor_input: dict, timeout_secs: int = 300) -> list[dict]:
    token = os.environ.get("APIFY_TOKEN")
    if not token:
        sys.exit("Set APIFY_TOKEN first: export APIFY_TOKEN=apify_api_...")
    url = f"https://api.apify.com/v2/acts/{actor_id.replace('/', '~')}/run-sync-get-dataset-items"
    response = requests.post(
        url,
        params={"timeout": timeout_secs},
        headers={"Authorization": f"Bearer {token}"},
        json=actor_input,
        timeout=timeout_secs + 30,
    )
    response.raise_for_status()
    return response.json()
