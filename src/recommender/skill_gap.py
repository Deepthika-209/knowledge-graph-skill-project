from src.knowledge_graph import build_knowledge_graph


# --------------------------------------------------
# SKILL GAP ANALYSIS
# --------------------------------------------------

def get_skill_gap(student_id, target_skill):
    """
    Find the skills a student is missing
    in order to learn a target skill.
    """

    kg = build_knowledge_graph()

    student_node = f"student:{student_id}"
    target_node = f"skill:{target_skill}"

    # --------------------------------------------------
    # CHECK STUDENT
    # --------------------------------------------------

    if student_node not in kg:

        return {
            "student_id": student_id,
            "target_skill": target_skill,
            "known_skills": [],
            "required_skills": [],
            "missing_skills": [],
            "ready": False,
            "message": "Student not found in the Knowledge Graph."
        }

    # --------------------------------------------------
    # CHECK TARGET SKILL
    # --------------------------------------------------

    if target_node not in kg:

        return {
            "student_id": student_id,
            "target_skill": target_skill,
            "known_skills": [],
            "required_skills": [],
            "missing_skills": [],
            "ready": False,
            "message": "Target skill not found in the Knowledge Graph."
        }

    # --------------------------------------------------
    # GET CURRENT STUDENT SKILLS
    # --------------------------------------------------

    known_skills = set()

    for _, skill_node, edge_data in kg.out_edges(
        student_node,
        data=True
    ):

        if edge_data.get("relation") != "HAS_SKILL":
            continue

        if skill_node.startswith("skill:"):

            skill_name = kg.nodes[skill_node].get("name")

            if skill_name:
                known_skills.add(skill_name)

    # --------------------------------------------------
    # FIND ALL REQUIRED SKILLS
    # --------------------------------------------------

    required_skills = set()

    visited = set()

    def collect_prerequisites(skill_node):

        if skill_node in visited:
            return

        visited.add(skill_node)

        if skill_node not in kg:
            return

        skill_name = kg.nodes[skill_node].get("name")

        if skill_name:
            required_skills.add(skill_name)

        for prerequisite_node in kg.predecessors(
            skill_node
        ):

            edge_data_list = kg.get_edge_data(
                prerequisite_node,
                skill_node
            )

            if not edge_data_list:
                continue

            for _, edge_data in edge_data_list.items():

                if (
                    edge_data.get("relation")
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
    # ORDER RESULTS
    # --------------------------------------------------

    ordered_required_skills = []

    for skill in required_skills:

        if skill not in ordered_required_skills:

            ordered_required_skills.append(skill)

    ordered_missing_skills = []

    for skill in missing_skills:

        if skill not in ordered_missing_skills:

            ordered_missing_skills.append(skill)

    # Put the target skill last if it is missing.
    if (
        target_skill in ordered_missing_skills
        and target_skill != target_skill
    ):
        ordered_missing_skills.remove(
            target_skill
        )
        ordered_missing_skills.append(
            target_skill
        )

    # --------------------------------------------------
    # READINESS
    # --------------------------------------------------

    ready = len(ordered_missing_skills) == 0

    # --------------------------------------------------
    # MESSAGE
    # --------------------------------------------------

    if ready:

        message = (
            f"You already have all required skills "
            f"for {target_skill}."
        )

    else:

        message = (
            f"You are missing "
            f"{len(ordered_missing_skills)} skill(s) "
            f"for {target_skill}."
        )

    return {
        "student_id": student_id,
        "target_skill": target_skill,
        "known_skills": sorted(known_skills),
        "required_skills": sorted(
            required_skills
        ),
        "missing_skills": sorted(
            missing_skills
        ),
        "ready": ready,
        "message": message
    }


# --------------------------------------------------
# TEST
# --------------------------------------------------

if __name__ == "__main__":

    student_id = "S01"
    target_skill = "Deep Learning"

    result = get_skill_gap(
        student_id,
        target_skill
    )

    print("\n")
    print("=" * 60)
    print("SKILL GAP ANALYSIS")
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
        "\nKnown Skills:"
    )

    for skill in result["known_skills"]:
        print("  ✓", skill)

    print(
        "\nRequired Skills:"
    )

    for skill in result["required_skills"]:
        print("  •", skill)

    print(
        "\nMissing Skills:"
    )

    if result["missing_skills"]:

        for skill in result["missing_skills"]:
            print("  ✗", skill)

    else:

        print("  None")

    print(
        "\nReady:",
        result["ready"]
    )

    print(
        "\nMessage:",
        result["message"]
    )

    print("=" * 60)