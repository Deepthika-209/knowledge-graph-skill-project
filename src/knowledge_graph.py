import sys
from pathlib import Path

import pandas as pd
import networkx as nx


# --------------------------------------------------
# PROJECT PATHS
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "data"

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from database.database import get_connection


# --------------------------------------------------
# CREATE KNOWLEDGE GRAPH
# --------------------------------------------------

def build_knowledge_graph():

    # MultiDiGraph allows multiple relationship
    # types between the same pair of nodes.
    graph = nx.MultiDiGraph()

    # --------------------------------------------------
    # 1. LOAD STATIC DATASETS
    # --------------------------------------------------

    domains = pd.read_csv(DATA_DIR / "domains.csv")
    skills = pd.read_csv(DATA_DIR / "skills.csv")
    skill_domains = pd.read_csv(
        DATA_DIR / "skill_domains.csv"
    )
    prerequisites = pd.read_csv(
        DATA_DIR / "skill_prerequisites.csv"
    )
    related = pd.read_csv(
        DATA_DIR / "skill_related.csv"
    )
    projects = pd.read_csv(
        DATA_DIR / "projects.csv"
    )
    project_skills = pd.read_csv(
        DATA_DIR / "project_skills.csv"
    )
    students = pd.read_csv(
        DATA_DIR / "sample_students.csv"
    )

    # --------------------------------------------------
    # COURSES / RESOURCES
    # --------------------------------------------------

    courses = pd.read_csv(
        DATA_DIR / "courses.csv"
    )

    course_skills = pd.read_csv(
        DATA_DIR / "course_skills.csv"
    )

    # --------------------------------------------------
    # INTERNSHIPS
    # --------------------------------------------------

    internships = pd.read_csv(
        DATA_DIR / "internships.csv"
    )

    internship_skills = pd.read_csv(
        DATA_DIR / "internship_skills.csv"
    )

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

        if (
            pd.notna(row["parent_domain"])
            and str(row["parent_domain"]).strip() != ""
        ):

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
    # 5. CREATE CSV STUDENT NODES
    # --------------------------------------------------

    for _, row in students.iterrows():

        graph.add_node(
            f"student:{row['student_id']}",
            label="Student",
            student_id=row["student_id"],
            name=row["name"],
            level=row["level"],
            source="csv"
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

    # ==================================================
    # COURSE / RESOURCE LAYER
    # ==================================================

    # --------------------------------------------------
    # 11. COURSE NODES
    # --------------------------------------------------

    for _, row in courses.iterrows():

        course_id = str(
            row["course_id"]
        ).strip()

        graph.add_node(
            f"course:{course_id}",
            label="Course",
            course_id=course_id,
            title=row["title"],
            platform=row["platform"],
            domain=row["domain"],
            level=row["level"],
            duration_hours=float(
                row["duration_hours"]
            ),
            url=row["url"]
        )

    # --------------------------------------------------
    # 12. PLATFORM NODES
    # --------------------------------------------------

    for _, row in courses.iterrows():

        platform = str(
            row["platform"]
        ).strip()

        if not platform:
            continue

        graph.add_node(
            f"platform:{platform}",
            label="Platform",
            name=platform
        )

        graph.add_edge(
            f"course:{row['course_id']}",
            f"platform:{platform}",
            relation="OFFERED_BY"
        )

    # --------------------------------------------------
    # 13. COURSE -> DOMAIN
    # --------------------------------------------------

    for _, row in courses.iterrows():

        domain = str(
            row["domain"]
        ).strip()

        domain_node = f"domain:{domain}"

        if domain_node not in graph:
            continue

        graph.add_edge(
            f"course:{row['course_id']}",
            domain_node,
            relation="BELONGS_TO"
        )

    # --------------------------------------------------
    # 14. COURSE -> SKILL
    # --------------------------------------------------

    for _, row in course_skills.iterrows():

        course_name = str(
            row["course"]
        ).strip()

        skill_name = str(
            row["skill"]
        ).strip()

        course_match = courses[
            courses["title"].astype(str).str.strip()
            == course_name
        ]

        if course_match.empty:
            continue

        course_id = str(
            course_match.iloc[0]["course_id"]
        ).strip()

        course_node = f"course:{course_id}"
        skill_node = f"skill:{skill_name}"

        if skill_node not in graph:
            continue

        graph.add_edge(
            course_node,
            skill_node,
            relation="DEVELOPS",
            relevance=float(
                row["relevance"]
            )
        )

    # ==================================================
    # INTERNSHIP LAYER
    # ==================================================

    # --------------------------------------------------
    # 15. INTERNSHIP NODES
    # --------------------------------------------------
    #
    # Each internship becomes a graph entity.
    #
    # Example:
    #
    # Internship
    #   |
    #   +---- company
    #   +---- domain
    #   +---- level
    #   +---- duration
    #   +---- location
    #   +---- mode
    #   +---- url
    #
    # --------------------------------------------------

    for _, row in internships.iterrows():

        internship_id = str(
            row["internship_id"]
        ).strip()

        graph.add_node(
            f"internship:{internship_id}",
            label="Internship",
            internship_id=internship_id,
            title=row["title"],
            company=row["company"],
            domain=row["domain"],
            level=row["level"],
            duration_months=float(
                row["duration_months"]
            ),
            location=row["location"],
            mode=row["mode"],
            url=row["url"]
        )

    # --------------------------------------------------
    # 16. INTERNSHIP -> DOMAIN
    # --------------------------------------------------
    #
    # Internship
    #      |
    #      +---- BELONGS_TO ----> Domain
    #
    # --------------------------------------------------

    for _, row in internships.iterrows():

        internship_id = str(
            row["internship_id"]
        ).strip()

        domain = str(
            row["domain"]
        ).strip()

        internship_node = (
            f"internship:{internship_id}"
        )

        domain_node = f"domain:{domain}"

        if domain_node not in graph:
            continue

        graph.add_edge(
            internship_node,
            domain_node,
            relation="BELONGS_TO"
        )

    # --------------------------------------------------
    # 17. INTERNSHIP -> SKILL
    # --------------------------------------------------
    #
    # Internship
    #      |
    #      +---- REQUIRES ----> Skill
    #
    # relevance tells us how important the skill
    # is for that internship.
    #
    # --------------------------------------------------

    for _, row in internship_skills.iterrows():

        internship_title = str(
            row["internship"]
        ).strip()

        skill_name = str(
            row["skill"]
        ).strip()

        # Find internship using title.
        internship_match = internships[
            internships["title"].astype(str).str.strip()
            == internship_title
        ]

        if internship_match.empty:
            continue

        internship_id = str(
            internship_match.iloc[0]["internship_id"]
        ).strip()

        internship_node = (
            f"internship:{internship_id}"
        )

        skill_node = f"skill:{skill_name}"

        # Ignore skills that do not exist
        # in the Knowledge Graph.
        if skill_node not in graph:
            continue

        graph.add_edge(
            internship_node,
            skill_node,
            relation="REQUIRES",
            relevance=float(
                row["relevance"]
            )
        )

    # ==================================================
    # STUDENT LAYER
    # ==================================================

    # --------------------------------------------------
    # 18. CSV STUDENT -> SKILLS
    # --------------------------------------------------

    for _, row in students.iterrows():

        if pd.isna(row["skills"]):
            continue

        skill_list = [
            skill.strip()
            for skill in str(
                row["skills"]
            ).split(";")
            if skill.strip()
        ]

        proficiency_list = [
            proficiency.strip()
            for proficiency in str(
                row["proficiencies"]
            ).split(";")
            if proficiency.strip()
        ]

        for skill_name, proficiency in zip(
            skill_list,
            proficiency_list
        ):

            skill_node = f"skill:{skill_name}"

            if skill_node not in graph:
                continue

            graph.add_edge(
                f"student:{row['student_id']}",
                skill_node,
                relation="HAS_SKILL",
                proficiency=int(
                    proficiency
                )
            )

    # --------------------------------------------------
    # 19. CSV STUDENT -> INTERESTS
    # --------------------------------------------------

    for _, row in students.iterrows():

        if pd.isna(row["interests"]):
            continue

        interest_list = [
            interest.strip()
            for interest in str(
                row["interests"]
            ).split(";")
            if interest.strip()
        ]

        for interest in interest_list:

            domain_node = f"domain:{interest}"

            if domain_node not in graph:
                continue

            graph.add_edge(
                f"student:{row['student_id']}",
                domain_node,
                relation="INTERESTED_IN",
                weight=1.0
            )

    # ==================================================
    # DYNAMIC STUDENTS FROM SQLITE
    # ==================================================

    # --------------------------------------------------
    # 20. LOAD DYNAMIC STUDENTS
    # --------------------------------------------------

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            sp.id,
            sp.user_id,
            sp.student_id,
            sp.name,
            sp.college,
            sp.branch,
            sp.graduation_year,
            sp.target_domain
        FROM student_profiles sp
        """
    )

    dynamic_students = cursor.fetchall()

    # --------------------------------------------------
    # 21. ADD DYNAMIC STUDENT NODES
    # --------------------------------------------------

    for student in dynamic_students:

        student_id = student["student_id"]

        if not student_id:
            continue

        student_node = f"student:{student_id}"

        graph.add_node(
            student_node,
            label="Student",
            student_id=student_id,
            name=student["name"],
            level="beginner",
            college=student["college"],
            branch=student["branch"],
            graduation_year=student["graduation_year"],
            target_domain=student["target_domain"],
            source="sqlite"
        )

    # --------------------------------------------------
    # 22. DYNAMIC STUDENT -> SKILLS
    # --------------------------------------------------

    cursor.execute(
        """
        SELECT
            ss.user_id,
            ss.skill_name,
            ss.proficiency
        FROM student_skills ss
        """
    )

    dynamic_skills = cursor.fetchall()

    for student_skill in dynamic_skills:

        user_id = student_skill["user_id"]
        skill_name = student_skill["skill_name"]

        cursor.execute(
            """
            SELECT student_id
            FROM student_profiles
            WHERE user_id = ?
            """,
            (user_id,)
        )

        profile = cursor.fetchone()

        if profile is None:
            continue

        student_id = profile["student_id"]

        if not student_id:
            continue

        student_node = f"student:{student_id}"
        skill_node = f"skill:{skill_name}"

        if skill_node not in graph:
            continue

        graph.add_edge(
            student_node,
            skill_node,
            relation="HAS_SKILL",
            proficiency=int(
                student_skill["proficiency"]
            )
        )

    # --------------------------------------------------
    # 23. DYNAMIC STUDENT -> INTERESTS
    # --------------------------------------------------

    cursor.execute(
        """
        SELECT
            si.user_id,
            si.domain_name
        FROM student_interests si
        """
    )

    dynamic_interests = cursor.fetchall()

    for student_interest in dynamic_interests:

        user_id = student_interest["user_id"]
        domain_name = student_interest["domain_name"]

        cursor.execute(
            """
            SELECT student_id
            FROM student_profiles
            WHERE user_id = ?
            """,
            (user_id,)
        )

        profile = cursor.fetchone()

        if profile is None:
            continue

        student_id = profile["student_id"]

        if not student_id:
            continue

        student_node = f"student:{student_id}"
        domain_node = f"domain:{domain_name}"

        if domain_node not in graph:
            continue

        graph.add_edge(
            student_node,
            domain_node,
            relation="INTERESTED_IN",
            weight=1.0
        )

    # --------------------------------------------------
    # 24. TARGET DOMAIN FROM STUDENT PROFILE
    # --------------------------------------------------

    for student in dynamic_students:

        student_id = student["student_id"]
        target_domain = student["target_domain"]

        if not student_id:
            continue

        if not target_domain:
            continue

        student_node = f"student:{student_id}"
        domain_node = f"domain:{target_domain}"

        if domain_node not in graph:
            continue

        graph.add_edge(
            student_node,
            domain_node,
            relation="INTERESTED_IN",
            weight=1.0
        )

    # --------------------------------------------------
    # CLOSE DATABASE
    # --------------------------------------------------

    connection.close()

    return graph


# --------------------------------------------------
# TEST THE KNOWLEDGE GRAPH
# --------------------------------------------------

if __name__ == "__main__":

    kg = build_knowledge_graph()

    print("=" * 60)
    print("KNOWLEDGE GRAPH CREATED")
    print("=" * 60)

    print(
        "Total nodes:",
        kg.number_of_nodes()
    )

    print(
        "Total relationships:",
        kg.number_of_edges()
    )

    print("\nNode types:")

    node_counts = {}

    for _, data in kg.nodes(data=True):

        label = data["label"]

        node_counts[label] = (
            node_counts.get(label, 0) + 1
        )

    for label, count in node_counts.items():

        print(
            f"{label}: {count}"
        )

    print("\nRelationship types:")

    relationship_counts = {}

    for _, _, data in kg.edges(data=True):

        relation = data["relation"]

        relationship_counts[relation] = (
            relationship_counts.get(relation, 0) + 1
        )

    for relation, count in relationship_counts.items():

        print(
            f"{relation}: {count}"
        )

    print("\nStudent nodes:")

    for node, data in kg.nodes(data=True):

        if data.get("label") == "Student":

            print(
                f"{node} -> "
                f"{data.get('name')} "
                f"| Source: {data.get('source')}"
            )

    print("\nCourse nodes:")

    for node, data in kg.nodes(data=True):

        if data.get("label") == "Course":

            print(
                f"{node} -> "
                f"{data.get('title')} "
                f"| Platform: "
                f"{data.get('platform')}"
            )

    print("\nInternship nodes:")

    for node, data in kg.nodes(data=True):

        if data.get("label") == "Internship":

            print(
                f"{node} -> "
                f"{data.get('title')} "
                f"| Company: "
                f"{data.get('company')}"
            )

    print("\n" + "=" * 60)
    print("GRAPH BUILDING COMPLETED")
    print("=" * 60)