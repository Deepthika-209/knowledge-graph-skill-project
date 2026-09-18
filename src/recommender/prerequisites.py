from src.knowledge_graph import build_knowledge_graph
from src.recommender.skill_candidates import get_candidate_skills


# Build the Knowledge Graph
kg = build_knowledge_graph()


def check_prerequisites(student_id, skill_name):
    """
    Check whether a student has the prerequisites
    required for a particular skill.
    """

    student_node = f"student:{student_id}"
    skill_node = f"skill:{skill_name}"

    # Step 1: Get the student's known skills
    known_skills = set()

    for _, node, data in kg.out_edges(student_node, data=True):
        if data["relation"] == "HAS_SKILL":
            known_skills.add(kg.nodes[node]["name"])

    # Step 2: Find prerequisites of the candidate skill
    prerequisites = []

    for prerequisite_node, _, data in kg.in_edges(skill_node, data=True):
        if data["relation"] == "PREREQUISITE_OF":
            prerequisite_name = kg.nodes[prerequisite_node]["name"]
            prerequisites.append(prerequisite_name)

    # Step 3: Compare prerequisites with known skills
    known_prerequisites = []
    missing_prerequisites = []

    for prerequisite in prerequisites:
        if prerequisite in known_skills:
            known_prerequisites.append(prerequisite)
        else:
            missing_prerequisites.append(prerequisite)

    # Step 4: Decide readiness
    if len(prerequisites) == 0:
        ready = True
    else:
        ready = len(missing_prerequisites) == 0

    return {
        "skill": skill_name,
        "prerequisites": prerequisites,
        "known_prerequisites": known_prerequisites,
        "missing_prerequisites": missing_prerequisites,
        "ready": ready
    }


if __name__ == "__main__":

    student_id = "S01"

    print("=" * 60)
    print("PREREQUISITE REASONING")
    print("=" * 60)

    candidates = get_candidate_skills(student_id)

    for skill, strength in candidates:

        result = check_prerequisites(student_id, skill)

        print(f"\nSkill: {result['skill']}")
        print(f"Prerequisites: {result['prerequisites']}")
        print(f"Known: {result['known_prerequisites']}")
        print(f"Missing: {result['missing_prerequisites']}")
        print(f"Ready: {result['ready']}")

    print("\n" + "=" * 60)
    print("PREREQUISITE CHECK COMPLETED")
    print("=" * 60)