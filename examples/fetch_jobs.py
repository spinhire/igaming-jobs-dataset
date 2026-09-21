"""Fetch live iGaming jobs from the SpinHire API. No key required.

    python3 examples/fetch_jobs.py "kafka" remote
"""
import sys
import urllib.parse
import urllib.request
import json

API = "https://spinhire.io/api/jobs"


def fetch(query: str = "", fmt: str = "", limit: int = 50, lang: str = "en") -> list[dict]:
    params = {"limit": limit, "lang": lang}
    if query:
        params["q"] = query
    if fmt:
        params["fmt"] = fmt          # remote | hybrid | office
    url = f"{API}?{urllib.parse.urlencode(params)}"
    with urllib.request.urlopen(url, timeout=60) as response:
        return json.load(response)["jobs"]


if __name__ == "__main__":
    query = sys.argv[1] if len(sys.argv) > 1 else "backend"
    fmt = sys.argv[2] if len(sys.argv) > 2 else ""
    for job in fetch(query, fmt):
        print(f"{job['title']} | {job['company']} | {job['location']} | {job['salary']}")
        print(f"  {job['url']}")
