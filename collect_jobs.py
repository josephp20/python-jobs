"""Collect a small Orlando-area jobs dataset from the Jooble REST API."""
import csv
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import requests
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent
DATA = ROOT / 'data'
FIELDS = ['id','search_keyword','title','company','location','salary','type','source','updated','link','snippet','collected_at_utc']


def main():
    load_dotenv(ROOT / '.env')
    key = os.getenv('JOOBLE_API_KEY', '').strip()
    if not key:
        sys.exit('Missing JOOBLE_API_KEY. Copy .env.example to .env and add your API key.')
    DATA.mkdir(exist_ok=True)
    now = datetime.now(timezone.utc).isoformat()
    records = {}
    keywords = ['software developer', 'data analyst', 'customer service']
    for keyword in keywords:
        payload = {'keywords': keyword, 'location': 'Orlando, FL', 'radius': '16', 'page': 1, 'ResultOnPage': 20}
        try:
            response = requests.post(f'https://jooble.org/api/{key}', json=payload, timeout=30)
            response.raise_for_status()
            data = response.json()
        except (requests.RequestException, ValueError) as exc:
            print(f'Failed for {keyword}: {exc}', file=sys.stderr)
            continue
        print(f"{keyword}: received {len(data.get('jobs', []))} jobs (reported total {data.get('totalCount', 'unknown')})")
        for job in data.get('jobs', []):
            if not isinstance(job, dict):
                continue
            ident = str(job.get('id') or job.get('link') or f"{job.get('title')}:{job.get('company')}")
            if ident in records:
                continue
            record = {field: job.get(field, '') for field in FIELDS}
            record['id'] = job.get('id', '')
            record['search_keyword'] = keyword
            record['collected_at_utc'] = now
            records[ident] = record
    if not records:
        sys.exit('No records collected. Check your API key and query responses; no dataset created.')
    out = DATA / 'orlando_jobs.csv'
    with out.open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(records.values())
    print(f'Saved {len(records)} unique job listings to {out}')


if __name__ == '__main__':
    main()
