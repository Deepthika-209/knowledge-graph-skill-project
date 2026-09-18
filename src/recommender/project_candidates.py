from src.knowledge_graph import build_knowledge_graph


# --------------------------------------------------
# BUILD KNOWLEDGE GRAPH
# --------------------------------------------------

kg = build_knowledge_graph()


# --------------------------------------------------
# PROJECT CANDIDATE GENERATION
# --------------------------------------------------

def get_project_candidates(student_id):

    student_node = f"student:{student_id}"

    # --------------------------------------------------
    # 1. GET STUDENT'S KNOWN SKILLS
    # --------------------------------------------------

    known_skills = set()

    for _, skill_node, data in kg.out_edges(
        student_node,
        data=True
    ):

        if data["relation"] == "HAS_SKILL":

            skill_name = kg.nodes[skill_node]["name"]

            known_skills.add(skill_name)


    # --------------------------------------------------
    # 2. CHECK ALL PROJECTS
    # --------------------------------------------------

    candidates = []

    for project_node, project_data in kg.nodes(data=True):

        if project_data["label"] != "Project":
            continue

        project_title = project_data["title"]
        project_domain = project_data["domain"]

        required_skills = []
        known_required_skills = []
        missing_skills = []

        # --------------------------------------------------
        # 3. FIND SKILLS REQUIRED BY THE PROJECT
        # --------------------------------------------------

        for _, skill_node, edge_data in kg.out_edges(
            project_node,
            data=True
        ):

            if edge_data["relation"] == "REQUIRES":

                skill_name = kg.nodes[skill_node]["name"]

                required_skills.append(skill_name)

                if skill_name in known_skills:
                    known_required_skills.append(skill_name)
                else:
                    missing_skills.append(skill_name)


        # --------------------------------------------------
        # 4. CALCULATE BASIC COVERAGE
        # --------------------------------------------------

        total_required = len(required_skills)
        total_known = len(known_required_skills)

        if total_required == 0:
            coverage = 0.0
        else:
            coverage = total_known / total_required


        # --------------------------------------------------
        # 5. ADD PROJECT AS CANDIDATE
        # --------------------------------------------------

        candidates.append({
            "project": project_title,
            "domain": project_domain,
            "required_skills": required_skills,
            "known_skills": known_required_skills,
            "missing_skills": missing_skills,
            "coverage": coverage
        })


    return candidates


# --------------------------------------------------
# TEST PROJECT CANDIDATE GENERATION
# --------------------------------------------------

if __name__ == "__main__":

    student_id = "S01"

    print("=" * 60)
    print("PROJECT CANDIDATE GENERATION")
    print("=" * 60)

    candidates = get_project_candidates(student_id)

    print(f"\nStudent: {student_id}")

    for candidate in candidates:

        print(f"\nProject: {candidate['project']}")
        print(f"Domain: {candidate['domain']}")

        print(
            f"Required Skills: "
            f"{candidate['required_skills']}"
        )

        print(
            f"Known Skills: "
            f"{candidate['known_skills']}"
        )

        print(
            f"Missing Skills: "
            f"{candidate['missing_skills']}"
        )

        print(
            f"Skill Coverage: "
            f"{candidate['coverage']:.2f}"
        )

    print("\n" + "=" * 60)
    print("PROJECT CANDIDATE GENERATION COMPLETED")
    print("=" * 60)