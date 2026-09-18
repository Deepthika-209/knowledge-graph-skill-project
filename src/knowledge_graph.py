import pandas as pd
import networkx as nx
from pathlib import Path


# --------------------------------------------------
# PROJECT PATH
# --------------------------------------------------

DATA_DIR = Path("data")


# --------------------------------------------------
# CREATE KNOWLEDGE GRAPH
# --------------------------------------------------

def build_knowledge_graph():

    # MultiDiGraph allows multiple types of relationships
    # between the same pair of nodes.
    graph = nx.MultiDiGraph()


    # --------------------------------------------------
    # 1. LOAD DATASETS
    # --------------------------------------------------

    domains = pd.read_csv(DATA_DIR / "domains.csv")
    skills = pd.read_csv(DATA_DIR / "skills.csv")
    skill_domains = pd.read_csv(DATA_DIR / "skill_domains.csv")
    prerequisites = pd.read_csv(DATA_DIR / "skill_prerequisites.csv")
    related = pd.read_csv(DATA_DIR / "skill_related.csv")
    projects = pd.read_csv(DATA_DIR / "projects.csv")
    project_skills = pd.read_csv(DATA_DIR / "project_skills.csv")
    students = pd.read_csv(DATA_DIR / "sample_students.csv")


    # --------------------------------------------------
    # 2. CREATE DOMAIN NODES
    # --------------------------------------------------

    for _, row in domains.iterrows():

        graph.add_node(
            f"domain:{row['name']}",
            label="Domain",
            name=row["name"],
            description=row["description"]
        )


    # --------------------------------------------------
    # 2A. DOMAIN HIERARCHY
    # --------------------------------------------------

    for _, row in domains.iterrows():

        if pd.notna(row["parent_domain"]) and row["parent_domain"] != "":

            graph.add_edge(
                f"domain:{row['name']}",
                f"domain:{row['parent_domain']}",
                relation="SUBDOMAIN_OF"
            )


    # --------------------------------------------------
    # 3. CREATE SKILL NODES
    # --------------------------------------------------

    for _, row in skills.iterrows():

        graph.add_node(
            f"skill:{row['name']}",
            label="Skill",
            name=row["name"],
            type=row["type"],
            difficulty=int(row["difficulty"]),
            description=row["description"],
            is_technology=bool(row["is_technology"])
        )


    # --------------------------------------------------
    # 4. CREATE PROJECT NODES
    # --------------------------------------------------

    for _, row in projects.iterrows():

        graph.add_node(
            f"project:{row['title']}",
            label="Project",
            title=row["title"],
            domain=row["domain"],
            difficulty=int(row["difficulty"]),
            type=row["type"],
            description=row["description"]
        )


    # --------------------------------------------------
    # 5. CREATE STUDENT NODES
    # --------------------------------------------------

    for _, row in students.iterrows():

        graph.add_node(
            f"student:{row['student_id']}",
            label="Student",
            student_id=row["student_id"],
            name=row["name"],
            level=row["level"]
        )


    # --------------------------------------------------
    # 6. SKILL -> DOMAIN
    # --------------------------------------------------

    for _, row in skill_domains.iterrows():

        graph.add_edge(
            f"skill:{row['skill']}",
            f"domain:{row['domain']}",
            relation="BELONGS_TO",
            relevance=float(row["relevance"])
        )


    # --------------------------------------------------
    # 7. SKILL -> SKILL PREREQUISITE
    # --------------------------------------------------

    for _, row in prerequisites.iterrows():

        graph.add_edge(
            f"skill:{row['prerequisite']}",
            f"skill:{row['skill']}",
            relation="PREREQUISITE_OF",
            strength=float(row["strength"])
        )


    # --------------------------------------------------
    # 8. SKILL <-> SKILL RELATED
    # --------------------------------------------------

    for _, row in related.iterrows():

        graph.add_edge(
            f"skill:{row['skill_a']}",
            f"skill:{row['skill_b']}",
            relation="RELATED_TO",
            strength=float(row["strength"])
        )

        # RELATED_TO is treated as bidirectional.
        graph.add_edge(
            f"skill:{row['skill_b']}",
            f"skill:{row['skill_a']}",
            relation="RELATED_TO",
            strength=float(row["strength"])
        )


    # --------------------------------------------------
    # 9. PROJECT -> DOMAIN
    # --------------------------------------------------

    for _, row in projects.iterrows():

        graph.add_edge(
            f"project:{row['title']}",
            f"domain:{row['domain']}",
            relation="PART_OF"
        )


    # --------------------------------------------------
    # 10. PROJECT -> SKILL
    # --------------------------------------------------

    for _, row in project_skills.iterrows():

        graph.add_edge(
            f"project:{row['project']}",
            f"skill:{row['skill']}",
            relation="REQUIRES",
            importance=row["importance"]
        )


    # --------------------------------------------------
    # 11. STUDENT -> SKILLS
    # --------------------------------------------------

    for _, row in students.iterrows():

        if pd.isna(row["skills"]):
            continue

        skill_list = row["skills"].split(";")
        proficiency_list = row["proficiencies"].split(";")

        for skill_name, proficiency in zip(
            skill_list,
            proficiency_list
        ):

            graph.add_edge(
                f"student:{row['student_id']}",
                f"skill:{skill_name}",
                relation="HAS_SKILL",
                proficiency=int(proficiency)
            )


    # --------------------------------------------------
    # 12. STUDENT -> INTERESTS
    # --------------------------------------------------

    for _, row in students.iterrows():

        interest_list = row["interests"].split(";")

        for interest in interest_list:

            graph.add_edge(
                f"student:{row['student_id']}",
                f"domain:{interest}",
                relation="INTERESTED_IN",
                weight=1.0
            )


    return graph


# --------------------------------------------------
# TEST THE KNOWLEDGE GRAPH
# --------------------------------------------------

if __name__ == "__main__":

    kg = build_knowledge_graph()

    print("=" * 60)
    print("KNOWLEDGE GRAPH CREATED")
    print("=" * 60)

    print("Total nodes:", kg.number_of_nodes())
    print("Total relationships:", kg.number_of_edges())

    print("\nNode types:")

    node_counts = {}

    for _, data in kg.nodes(data=True):

        label = data["label"]

        node_counts[label] = node_counts.get(label, 0) + 1

    for label, count in node_counts.items():

        print(f"{label}: {count}")

    print("\nRelationship types:")

    relationship_counts = {}

    for _, _, data in kg.edges(data=True):

        relation = data["relation"]

        relationship_counts[relation] = (
            relationship_counts.get(relation, 0) + 1
        )

    for relation, count in relationship_counts.items():

        print(f"{relation}: {count}")

    print("\nSample nodes:")

    for node, data in list(kg.nodes(data=True))[:5]:

        print(node, "->", data)

    print("\n" + "=" * 60)
    print("GRAPH BUILDING COMPLETED")
    print("=" * 60)