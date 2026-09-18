import pandas as pd
from pathlib import Path

# Path to the data folder
DATA_DIR = Path("data")

# All CSV files in our dataset
files = [
    "domains.csv",
    "skills.csv",
    "skill_domains.csv",
    "skill_prerequisites.csv",
    "skill_related.csv",
    "projects.csv",
    "project_skills.csv",
    "sample_students.csv"
]

print("=" * 60)
print("KNOWLEDGE GRAPH DATASET INSPECTION")
print("=" * 60)

for file in files:
    path = DATA_DIR / file
    df = pd.read_csv(path)

    print("\n" + "-" * 60)
    print(f"FILE: {file}")
    print("-" * 60)

    print("Rows:", len(df))
    print("Columns:", list(df.columns))

    print("\nFirst 3 rows:")
    print(df.head(3).to_string(index=False))

    print("\nMissing values:")
    print(df.isnull().sum().to_dict())

    print("Duplicate rows:", df.duplicated().sum())

print("\n" + "=" * 60)
print("INSPECTION COMPLETED")
print("=" * 60)