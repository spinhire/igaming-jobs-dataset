# iGaming Jobs Dataset

Open snapshot of the **iGaming job market** — online casino, sports betting, game studios, affiliates, payments and compliance — collected by [SpinHire](https://spinhire.io).

[![License: CC BY 4.0](https://img.shields.io/badge/data%20license-CC%20BY%204.0-blue.svg)](LICENSE)
[![Jobs](https://img.shields.io/badge/open%20jobs-6%2C744-3cf0c2)](https://spinhire.io/en/jobs)
[![Companies](https://img.shields.io/badge/companies-444-ff5fc1)](https://spinhire.io/en/companies)
[![Updated](https://img.shields.io/badge/snapshot-2026--09--21-lightgrey)](data/jobs.csv)

The live index behind this dataset refreshes every 6 hours and is also available as a **public API without a key**, plus XML and RSS feeds and an MCP server for AI assistants.

---

## What is in here

| File | Rows | What it is |
|---|---|---|
| [`data/jobs.csv`](data/jobs.csv) | 6,744 | One row per open vacancy, snapshot of 2026-09-21 |
| [`data/jobs.jsonl`](data/jobs.jsonl) | 6,744 | The same records as JSON Lines |
| [`data/market_monthly.csv`](data/market_monthly.csv) | monthly | Open jobs, hiring companies, new postings and the share with a published salary |
| [`data/market_daily.csv`](data/market_daily.csv) | daily | Daily snapshots kept since September 2026 |

No job descriptions, contact details or personal data are included.

## Schema

| Column | Example | Notes |
|---|---|---|
| `id` | `13967` | SpinHire job id |
| `title` | `Senior Backend Engineer` | as published by the employer |
| `company`, `company_slug` | `Evolution`, `evolution` | `Компания не указана` means the source hid the employer |
| `location` | `St Julian's, Malta` | raw string from the source, not normalized |
| `country` | `Malta`, `Remote`, `Not specified` | normalized; `Remote` is its own value |
| `format` | `office` / `remote` / `hybrid` | derived from the location and the first lines of the posting |
| `category` | `Casino operations` | 11 departments, see below |
| `salary` | `€4,500–8,000` | raw string; empty or "on request" when the employer published nothing |
| `salary_min`, `salary_max`, `salary_currency`, `salary_unit` | `4500`, `8000`, `EUR`, `MONTH` | parsed only when the posting states pay |
| `employment_type` | `FULL_TIME` | schema.org values |
| `languages` | `English, German` | working languages required by the posting |
| `tags` | `retention` | free-form tags |
| `posted_at`, `valid_through` | `2026-09-15` | dates as published |
| `url`, `source_url` | links | SpinHire page and the original posting |

**Departments:** Casino operations · Game development · Marketing & CRM · Executive · Affiliates & media buying · Player support · Compliance & AML · Payments & anti-fraud · Data & BI · Finance, legal & HR · Betting & trading

## What the snapshot shows

- **8.5%** of postings state a salary (575 of 6,744). Most of the market still writes "competitive".
- **23%** of roles are remote or hybrid (1,715 of 6,744).
- Biggest markets after remote: United Kingdom 642, USA 570, Malta 541, Bulgaria 241, Greece 194, Poland 173.
- Biggest employers in the snapshot: Aristocrat 292, Evolution 288, Playtech 245, Entain 237.

## Quickstart

```bash
# the live API, no key required
curl "https://spinhire.io/api/jobs?q=backend&fmt=remote&lang=en&limit=20"
```

```python
import pandas as pd

jobs = pd.read_csv("data/jobs.csv")

# where the money is visible
paid = jobs.dropna(subset=["salary_min"])
print(paid.groupby("country")["salary_min"].median().sort_values(ascending=False).head())

# remote share by department
print(jobs.assign(remote=jobs["format"].eq("remote")).groupby("category")["remote"].mean().mul(100).round(1))
```

More in [`examples/`](examples): a plain API client, a pandas notebook-style script and a shell one-liner.

## Live data

| What | Where |
|---|---|
| Jobs API (no key, CC BY 4.0) | `https://spinhire.io/api/jobs` · [docs](https://spinhire.io/en/docs) |
| Indeed-style XML feed | `https://spinhire.io/feed/jobs.xml` |
| RSS feed | `https://spinhire.io/feed/rss.xml` |
| MCP server for AI assistants | `https://spinhire.io/mcp` |
| Quarterly market report | [spinhire.io/en/market/2026-q3](https://spinhire.io/en/market/2026-q3) |
| Salary benchmarks, 35 professions | [spinhire.io/en/professions](https://spinhire.io/en/professions) |

Parameters for `/api/jobs`: `q`, `category`, `country`, `fmt`, `page`, `limit`, `lang`.

## How the data is collected

Vacancies come from employer career pages, public ATS endpoints (Greenhouse, Lever, SmartRecruiters, BambooHR), industry feeds and public channels. The crawler runs every 6 hours; postings that disappear at the source are archived, so the index reflects live demand rather than an archive. Duplicates across sources are merged conservatively — a normalized title plus company plus location key, keeping the longest posting.

Rebuild the export yourself:

```bash
python3 scripts/export_dataset.py     # writes data/ from the public API
```

## Caveats

- `location` is the raw string from the source and can be messy. Use `country` when you need something normalized.
- Around 10% of postings are probable cross-source duplicates; headline shares move by no more than ~3 points because of them.
- Salary parsing is conservative: when the period is unclear the value is dropped rather than guessed.
- A snapshot is a point in time. For anything live, use the API.

## License and citation

Data: **[CC BY 4.0](LICENSE)** — free to use, including commercially, with attribution.

```
SpinHire (2026). iGaming Jobs Dataset. https://spinhire.io — CC BY 4.0
```

Found an error in the data? [Open an issue](../../issues) — corrections go into the live index too.
