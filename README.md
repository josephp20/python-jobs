# Orlando Job Market Analysis Using the Jooble API

Student project analyzing a small sample of real job postings returned by Jooble for Orlando, Florida. Data will only exist after running the collector with a valid API key. The dataset is a sample, not a census of all Orlando jobs.

## Setup (Windows PowerShell)

1. Install Python and Git if needed.
2. Open this folder in VS Code or PowerShell.
3. Run:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

4. Create a free US-region key at https://jooble.org/api/about and paste it in `.env` (never upload `.env` to GitHub).
5. Run:

```powershell
python collect_jobs.py
python analyze_jobs.py
```

The collector searches three job categories, requests up to 20 postings per category, and deduplicates by job ID/link. It writes real results to `data/orlando_jobs.csv`. The analysis writes basic PNG charts to `data/`.

## Data fields

`id`, `search_keyword`, `title`, `company`, `location`, `salary`, `type`, `source`, `updated`, `link`, `snippet`, `collected_at_utc`.

## Upload to GitHub

After collecting, check that `data/orlando_jobs.csv` exists and contains real records. Then:

```powershell
git init
git add .
git commit -m "Initial Jooble API data collection and analysis"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/orlando-job-market-analysis.git
git push -u origin main
```

Create the empty public repository on GitHub before pushing. Replace `YOUR_USERNAME` with your GitHub username. Do not upload API credentials.

## Notes & limitations

- Jooble's free US REST key has a lifetime limit of 500 requests (documentation checked October 2026).
- Not every posting discloses a salary; do not calculate an average salary without inspecting currency, units, and comparability.
- 'Employment type' and 'company' can be missing.
- Multiple keyword searches overlap; the collector deduplicates returned postings.
- Observed counts are numbers of **collected postings**, not total Orlando employment or labor demand.
- Documentation: https://help.jooble.org/en/support/solutions/articles/60001448238-rest-api-documentation
