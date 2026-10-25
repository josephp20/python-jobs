"""Create basic figures and counts from collected job data."""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
csv_file = ROOT / 'data' / 'orlando_jobs.csv'
if not csv_file.exists():
    raise SystemExit('Dataset missing. Run collect_jobs.py first.')
df = pd.read_csv(csv_file).fillna('')
print('Total job postings:', len(df))
print('Jobs with nonempty salary:', (df['salary'].astype(str).str.strip() != '').sum())
for field in ['search_keyword', 'company', 'type']:
    counts = df.loc[df[field].astype(str).str.strip() != '', field].value_counts().head(10)
    print(f'\nTop {field}:\n{counts.to_string()}')
    if counts.empty:
        continue
    plt.figure(figsize=(9, 4.5))
    counts.sort_values().plot.barh()
    plt.title(f'Top {field.replace("_", " ").title()} in Collected Jooble Data')
    plt.xlabel('Number of collected postings')
    plt.tight_layout()
    plt.savefig(ROOT / 'data' / f'{field}_counts.png', dpi=160)
    plt.close()
