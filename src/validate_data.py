import pandas as pd
from pathlib import Path
import networkx as nx

DATA_DIR = Path("data")

# Load all datasets
domains = pd.read_csv(DATA_DIR / "domains.csv")
skills = pd.read_csv(DATA_DIR / "skills.csv")
skill_domains = pd.read_csv(DATA_DIR / "skill_domains.csv")
prerequisites = pd.read_csv(DATA_DIR / "skill_prerequisites.csv")
related = pd.read_csv(DATA_DIR / "skill_related.csv")
projects = pd.read_csv(DATA_DIR / "projects.csv")
project_skills = pd.read_csv(DATA_DIR / "project_skills.csv")

print("=" * 60)
print("KNOWLEDGE GRAPH RELATIONSHIP VALIDATION")
print("=" * 60)


# --------------------------------------------------
# 1. Check skill -> domain references
# --------------------------------------------------

skill_names = set(skills["name"])
domain_names = set(domains["name"])
project_names = set(projects["title"])

invalid_skill_domains = skill_domains[
    ~skill_domains["skill"].isin(skill_names)
]

invalid_domains = skill_domains[
    ~skill_domains["domain"].isin(domain_names)
]

print("\n1. SKILL-DOMAIN REFERENCES")
print("Invalid skills:", len(invalid_skill_domains))
print("Invalid domains:", len(invalid_domains))


# --------------------------------------------------
# 2. Check prerequisite references
# --------------------------------------------------

invalid_prerequisite = prerequisites[
    (~prerequisites["prerequisite"].isin(skill_names))
    | (~prerequisites["skill"].isin(skill_names))
]

print("\n2. PREREQUISITE REFERENCES")
print("Invalid references:", len(invalid_prerequisite))


# --------------------------------------------------
# 3. Check related-skill references
# --------------------------------------------------

invalid_related = related[
    (~related["skill_a"].isin(skill_names))
    | (~related["skill_b"].isin(skill_names))
]

print("\n3. RELATED-SKILL REFERENCES")
print("Invalid references:", len(invalid_related))


# --------------------------------------------------
# 4. Check project -> skill references
# --------------------------------------------------

invalid_project_skills = project_skills[
    (~project_skills["project"].isin(project_names))
    | (~project_skills["skill"].isin(skill_names))
]

print("\n4. PROJECT-SKILL REFERENCES")
print("Invalid references:", len(invalid_project_skills))


# --------------------------------------------------
# 5. Check project domains
# --------------------------------------------------

invalid_project_domains = projects[
    ~projects["domain"].isin(domain_names)
]

print("\n5. PROJECT-DOMAIN REFERENCES")
print("Invalid domains:", len(invalid_project_domains))


# --------------------------------------------------
# 6. Check prerequisite cycles
# --------------------------------------------------

graph = nx.DiGraph()

for _, row in prerequisites.iterrows():
    graph.add_edge(
        row["prerequisite"],
        row["skill"]
    )

has_cycle = not nx.is_directed_acyclic_graph(graph)

print("\n6. PREREQUISITE CYCLE CHECK")
print("Cycle detected:", has_cycle)

if has_cycle:
    cycles = list(nx.simple_cycles(graph))

    print("Cycles found:")
    for cycle in cycles:
        print(" -> ".join(cycle))


# --------------------------------------------------
# 7. Check duplicate RELATED_TO pairs
# --------------------------------------------------

related_pairs = set()
duplicate_related = []

for _, row in related.iterrows():

    pair = tuple(sorted([
        row["skill_a"],
        row["skill_b"]
    ]))

    if pair in related_pairs:
        duplicate_related.append(pair)
    else:
        related_pairs.add(pair)

print("\n7. RELATED-SKILL DUPLICATE CHECK")
print("Duplicate pairs:", len(duplicate_related))


# --------------------------------------------------
# 8. Check every skill belongs to a domain
# --------------------------------------------------

skills_with_domain = set(skill_domains["skill"])

skills_without_domain = skill_names - skills_with_domain

print("\n8. SKILL DOMAIN COVERAGE")
print("Skills without a domain:", len(skills_without_domain))

if skills_without_domain:
    print("Skills:", skills_without_domain)


# --------------------------------------------------
# 9. Check every project has skills
# --------------------------------------------------

projects_with_skills = set(project_skills["project"])

projects_without_skills = project_names - projects_with_skills

print("\n9. PROJECT SKILL COVERAGE")
print("Projects without skills:", len(projects_without_skills))

if projects_without_skills:
    print("Projects:", projects_without_skills)
# --------------------------------------------------
# 10. Check self-related skills
# --------------------------------------------------

self_related = related[
    related["skill_a"] == related["skill_b"]
]

print("\n10. SELF-RELATED SKILL CHECK")
print("Self-related pairs:", len(self_related))

if len(self_related) > 0:
    print("\nSelf-related skills found:")
    print(self_related.to_string(index=False))

# --------------------------------------------------
# FINAL RESULT
# --------------------------------------------------

all_valid = (
    len(invalid_skill_domains) == 0
    and len(invalid_domains) == 0
    and len(invalid_prerequisite) == 0
    and len(invalid_related) == 0
    and len(invalid_project_skills) == 0
    and len(invalid_project_domains) == 0
    and not has_cycle
    and len(duplicate_related) == 0
    and len(skills_without_domain) == 0
    and len(projects_without_skills) == 0
)

print("\n" + "=" * 60)

if all_valid:
    print("RESULT: DATASET RELATIONSHIPS ARE VALID")
else:
    print("RESULT: SOME ISSUES WERE FOUND")

print("=" * 60)