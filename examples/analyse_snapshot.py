"""Answer four questions from the snapshot in data/jobs.csv.

    pip install pandas
    python3 examples/analyse_snapshot.py
"""
import pandas as pd

jobs = pd.read_csv("data/jobs.csv")
print(f"{len(jobs):,} open jobs from {jobs['company'].nunique():,} companies\n")

# 1. Who publishes salaries at all
paid = jobs.dropna(subset=["salary_min"])
print(f"postings with a salary: {len(paid):,} ({len(paid) / len(jobs):.1%})\n")

# 2. Median monthly pay where it is published, by country
monthly = paid[paid["salary_unit"] == "MONTH"]
by_country = monthly.groupby("country")["salary_min"].agg(["count", "median"])
print("median advertised minimum, monthly roles:")
print(by_country[by_country["count"] >= 5].sort_values("median", ascending=False).head(10), "\n")

# 3. Remote share by department
remote = jobs.assign(is_remote=jobs["format"].eq("remote"))
print("remote share by department, %:")
print(remote.groupby("category")["is_remote"].mean().mul(100).round(1).sort_values(ascending=False), "\n")

# 4. Which working languages employers ask for
languages = jobs["languages"].fillna("").str.split(", ").explode()
print("top working languages:")
print(languages[languages != ""].value_counts().head(10))
