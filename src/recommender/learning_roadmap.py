from src.knowledge_graph import build_knowledge_graph


# --------------------------------------------------
# LEARNING ROADMAP
# --------------------------------------------------

def generate_learning_roadmap(student_id, target_skill):
    """
    Generate a prerequisite-based learning roadmap
    for a student targeting a particular skill.
    """

    kg = build_knowledge_graph()

    student_node = f"student:{student_id}"
    target_node = f"skill:{target_skill}"

    # --------------------------------------------------
    # VALIDATION
    # --------------------------------------------------

    if student_node not in kg:
        return {
            "student_id": student_id,
            "target_skill": target_skill,
            "roadmap": [],
            "ready": False,
            "message": "Student not found in the Knowledge Graph."
        }

    if target_node not in kg:
        return {
            "student_id": student_id,
            "target_skill": target_skill,
            "roadmap": [],
            "ready": False,
            "message": "Target skill not found in the Knowledge Graph."
        }

    # --------------------------------------------------
    # GET CURRENT SKILLS
    # --------------------------------------------------

    known_skills = set()

    for _, skill_node, edge_data in kg.out_edges(
        student_node,
        data=True
    ):

        if edge_data.get("relation") != "HAS_SKILL":
            continue

        skill_name = kg.nodes[skill_node].get("name")

        if skill_name:
            known_skills.add(skill_name)

    # --------------------------------------------------
    # FIND ALL PREREQUISITES
    # --------------------------------------------------

    required_skills = set()

    def collect_prerequisites(skill_node):

        if skill_node in required_skills:
            return

        skill_name = kg.nodes[skill_node].get("name")

        if skill_name:
            required_skills.add(skill_name)

        for prerequisite_node in kg.predecessors(
            skill_node
        ):

            edge_data = kg.get_edge_data(
                prerequisite_node,
                skill_node
            )

            if not edge_data:
                continue

            for _, relationship in edge_data.items():

                if (
                    relationship.get("relation")
                    == "PREREQUISITE_OF"
                ):

                    collect_prerequisites(
                        prerequisite_node
                    )

    collect_prerequisites(target_node)

    # --------------------------------------------------
    # FIND MISSING SKILLS
    # --------------------------------------------------

    missing_skills = (
        required_skills - known_skills
    )

    # --------------------------------------------------
    # BUILD DEPENDENCY GRAPH
    # --------------------------------------------------

    dependency_graph = {}

    for skill_name in missing_skills:

        skill_node = f"skill:{skill_name}"

        dependency_graph[skill_name] = []

        if skill_node not in kg:
            continue

        for prerequisite_node in kg.predecessors(
            skill_node
        ):

            edge_data = kg.get_edge_data(
                prerequisite_node,
                skill_node
            )

            if not edge_data:
                continue

            for _, relationship in edge_data.items():

                if (
                    relationship.get("relation")
                    == "PREREQUISITE_OF"
                ):

                    prerequisite_name = kg.nodes[
                        prerequisite_node
                    ].get("name")

                    if (
                        prerequisite_name
                        in missing_skills
                    ):

                        dependency_graph[
                            skill_name
                        ].append(
                            prerequisite_name
                        )

    # --------------------------------------------------
    # TOPOLOGICAL SORT
    # --------------------------------------------------

    roadmap = []
    completed = set(known_skills)

    remaining = set(missing_skills)

    while remaining:

        progress = False

        for skill_name in sorted(remaining):

            prerequisites = dependency_graph.get(
                skill_name,
                []
            )

            # Skill can be learned when all of its
            # missing prerequisites are already completed.
            if all(
                prerequisite in completed
                for prerequisite in prerequisites
            ):

                roadmap.append(skill_name)

                completed.add(skill_name)

                remaining.remove(skill_name)

                progress = True

                break

        # Prevent infinite loops if invalid/cyclic
        # prerequisite data exists.
        if not progress:
            roadmap.extend(
                sorted(remaining)
            )
            break

    # --------------------------------------------------
    # READINESS
    # --------------------------------------------------

    ready = len(roadmap) == 0

    if ready:

        message = (
            f"You are already ready to learn "
            f"{target_skill}."
        )

    else:

        message = (
            f"Complete the skills in this order "
            f"to prepare for {target_skill}."
        )

    # --------------------------------------------------
    # RETURN RESULT
    # --------------------------------------------------

    return {
        "student_id": student_id,
        "target_skill": target_skill,
        "known_skills": sorted(known_skills),
        "missing_skills": sorted(missing_skills),
        "roadmap": roadmap,
        "ready": ready,
        "message": message
    }


# --------------------------------------------------
# TEST
# --------------------------------------------------

if __name__ == "__main__":

    student_id = "S01"
    target_skill = "Deep Learning"

    result = generate_learning_roadmap(
        student_id,
        target_skill
    )

    print()
    print("=" * 60)
    print("PERSONALIZED LEARNING ROADMAP")
    print("=" * 60)

    print(
        "\nStudent:",
        result["student_id"]
    )

    print(
        "Target Skill:",
        result["target_skill"]
    )

    print(
        "\nCurrent Skills:"
    )

    for skill in result["known_skills"]:
        print("  ✓", skill)

    print(
        "\nRecommended Learning Order:"
    )

    if result["roadmap"]:

        for index, skill in enumerate(
            result["roadmap"],
            start=1
        ):

            print(
                f"  {index}. {skill}"
            )

    else:

        print("  No additional skills required.")

    print(
        "\nReady:",
        result["ready"]
    )

    print(
        "\nMessage:",
        result["message"]
    )

    print("=" * 60)