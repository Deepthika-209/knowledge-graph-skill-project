from src.knowledge_graph import build_knowledge_graph


kg = build_knowledge_graph()


# --------------------------------------------------
# SKILL EXPLANATION
# --------------------------------------------------

def explain_skill_recommendation(student_id, skill_name):

    student_node = f"student:{student_id}"
    skill_node = f"skill:{skill_name}"

    # ----------------------------------------------
    # 1. Find student's known skills
    # ----------------------------------------------

    known_skills = set()

    for _, node, data in kg.out_edges(
        student_node,
        data=True
    ):

        if data["relation"] == "HAS_SKILL":

            known_skill = kg.nodes[node]["name"]

            known_skills.add(known_skill)

    # ----------------------------------------------
    # 2. Find skills related to the recommended skill
    # ----------------------------------------------

    related_known_skills = []

    for node, _, data in kg.in_edges(
        skill_node,
        data=True
    ):

        if data["relation"] == "RELATED_TO":

            related_skill = kg.nodes[node]["name"]

            if related_skill in known_skills:

                related_known_skills.append(
                    related_skill
                )

    # ----------------------------------------------
    # 3. Find prerequisites
    # ----------------------------------------------

    prerequisites = []

    for node, _, data in kg.in_edges(
        skill_node,
        data=True
    ):

        if data["relation"] == "PREREQUISITE_OF":

            prerequisite = kg.nodes[node]["name"]

            prerequisites.append(
                prerequisite
            )

    # ----------------------------------------------
    # 4. Check known prerequisites
    # ----------------------------------------------

    known_prerequisites = []

    missing_prerequisites = []

    for prerequisite in prerequisites:

        if prerequisite in known_skills:

            known_prerequisites.append(
                prerequisite
            )

        else:

            missing_prerequisites.append(
                prerequisite
            )

    # ----------------------------------------------
    # 5. Find skill's domain
    # ----------------------------------------------

    skill_domain = None

    for _, node, data in kg.out_edges(
        skill_node,
        data=True
    ):

        if data["relation"] == "BELONGS_TO":

            skill_domain = kg.nodes[node]["name"]

            break

    # ----------------------------------------------
    # 6. Find student's interested domains
    # ----------------------------------------------

    interests = []

    for _, node, data in kg.out_edges(
        student_node,
        data=True
    ):

        if data["relation"] == "INTERESTED_IN":

            domain_name = kg.nodes[node]["name"]

            interests.append(
                domain_name
            )

    # ----------------------------------------------
    # 7. Check domain match
    # ----------------------------------------------

    domain_match = False
    matched_interest_domain = None

    # Direct domain match
    if skill_domain in interests:

        domain_match = True
        matched_interest_domain = skill_domain

    # Subdomain match
    elif skill_domain is not None:

        skill_domain_node = f"domain:{skill_domain}"

        for _, parent_node, data in kg.out_edges(
            skill_domain_node,
            data=True
        ):

            if data["relation"] == "SUBDOMAIN_OF":

                parent_domain = kg.nodes[
                    parent_node
                ]["name"]

                if parent_domain in interests:

                    domain_match = True
                    matched_interest_domain = parent_domain

                    break

    # ----------------------------------------------
    # 8. Build explanation
    # ----------------------------------------------

    explanation_parts = []

    # Existing skill relationship
    if related_known_skills:

        explanation_parts.append(
            "It is related to your existing skill(s): "
            + ", ".join(related_known_skills)
            + "."
        )

    # Known prerequisites
    if known_prerequisites:

        explanation_parts.append(
            "You already know the prerequisite skill(s): "
            + ", ".join(known_prerequisites)
            + "."
        )

    # Missing prerequisites
    if missing_prerequisites:

        explanation_parts.append(
            "You are missing prerequisite skill(s): "
            + ", ".join(missing_prerequisites)
            + "."
        )

    # Domain relationship
    if domain_match and skill_domain:

        if skill_domain == matched_interest_domain:

            explanation_parts.append(
                "It belongs to your interested domain: "
                + skill_domain
                + "."
            )

        else:

            explanation_parts.append(
                "It belongs to the "
                + skill_domain
                + " subdomain of your interested domain: "
                + matched_interest_domain
                + "."
            )

    elif skill_domain:

        explanation_parts.append(
            "It belongs to the "
            + skill_domain
            + " domain."
        )

    # ----------------------------------------------
    # 9. Final fallback
    # ----------------------------------------------

    if not explanation_parts:

        explanation_parts.append(
            "The skill is connected to your profile "
            "through the knowledge graph."
        )

    return {
        "skill": skill_name,
        "explanation": " ".join(
            explanation_parts
        ),
        "related_skills": related_known_skills,
        "prerequisites": prerequisites,
        "known_prerequisites": known_prerequisites,
        "missing_prerequisites": missing_prerequisites,
        "skill_domain": skill_domain,
        "interests": interests,
        "domain_match": domain_match,
        "matched_interest_domain": matched_interest_domain
    }


# --------------------------------------------------
# PROJECT EXPLANATION
# --------------------------------------------------

def explain_project_recommendation(
    student_id,
    project_name
):

    student_node = f"student:{student_id}"
    project_node = f"project:{project_name}"

    # ----------------------------------------------
    # 1. Find student's known skills
    # ----------------------------------------------

    known_skills = set()

    for _, node, data in kg.out_edges(
        student_node,
        data=True
    ):

        if data["relation"] == "HAS_SKILL":

            skill_name = kg.nodes[node]["name"]

            known_skills.add(skill_name)

    # ----------------------------------------------
    # 2. Find project required skills
    # ----------------------------------------------

    required_skills = []

    known_required_skills = []

    missing_skills = []

    for _, skill_node, data in kg.out_edges(
        project_node,
        data=True
    ):

        if data["relation"] != "REQUIRES":
            continue

        skill_name = kg.nodes[skill_node]["name"]

        required_skills.append(
            skill_name
        )

        if skill_name in known_skills:

            known_required_skills.append(
                skill_name
            )

        else:

            missing_skills.append(
                skill_name
            )

    # ----------------------------------------------
    # 3. Find project domain
    # ----------------------------------------------

    project_domain = kg.nodes[
        project_node
    ]["domain"]

    # ----------------------------------------------
    # 4. Find student's interests
    # ----------------------------------------------

    interests = []

    for _, node, data in kg.out_edges(
        student_node,
        data=True
    ):

        if data["relation"] == "INTERESTED_IN":

            domain_name = kg.nodes[node]["name"]

            interests.append(
                domain_name
            )

    # ----------------------------------------------
    # 5. Check project domain match
    # ----------------------------------------------

    domain_match = False
    matched_interest_domain = None

    # Direct domain match
    if project_domain in interests:

        domain_match = True
        matched_interest_domain = project_domain

    # Subdomain match
    elif project_domain is not None:

        project_domain_node = f"domain:{project_domain}"

        for _, parent_node, data in kg.out_edges(
            project_domain_node,
            data=True
        ):

            if data["relation"] == "SUBDOMAIN_OF":

                parent_domain = kg.nodes[
                    parent_node
                ]["name"]

                if parent_domain in interests:

                    domain_match = True
                    matched_interest_domain = parent_domain

                    break

    # ----------------------------------------------
    # 6. Build explanation
    # ----------------------------------------------

    explanation_parts = []

    # Known required skills
    if known_required_skills:

        explanation_parts.append(
            "You already know "
            + ", ".join(known_required_skills)
            + ", which are required for this project."
        )

    # Missing required skills
    if missing_skills:

        explanation_parts.append(
            "You are missing "
            + ", ".join(missing_skills)
            + ", which are additional skills needed for the project."
        )

    # Domain relationship
    if domain_match and project_domain:

        if project_domain == matched_interest_domain:

            explanation_parts.append(
                "The project belongs to your interested domain: "
                + project_domain
                + "."
            )

        else:

            explanation_parts.append(
                "The project belongs to the "
                + project_domain
                + " subdomain of your interested domain: "
                + matched_interest_domain
                + "."
            )

    elif project_domain:

        explanation_parts.append(
            "The project belongs to the "
            + project_domain
            + " domain, which is outside your selected interest area."
        )

    # ----------------------------------------------
    # 7. Final fallback
    # ----------------------------------------------

    if not explanation_parts:

        explanation_parts.append(
            "The project is connected to your profile "
            "through the knowledge graph."
        )

    return {
        "project": project_name,
        "domain": project_domain,
        "required_skills": required_skills,
        "known_skills": known_required_skills,
        "missing_skills": missing_skills,
        "interests": interests,
        "domain_match": domain_match,
        "matched_interest_domain": matched_interest_domain,
        "explanation": " ".join(
            explanation_parts
        )
    }


# --------------------------------------------------
# TEST SKILL AND PROJECT EXPLANATIONS
# --------------------------------------------------

if __name__ == "__main__":

    student_id = "S01"

    # ==================================================
    # SKILL EXPLANATION TEST
    # ==================================================

    skill_name = "OOP"

    result = explain_skill_recommendation(
        student_id,
        skill_name
    )

    print("=" * 60)
    print("SKILL EXPLANATION")
    print("=" * 60)

    print("\nStudent:", student_id)

    print(
        "Recommended Skill:",
        result["skill"]
    )

    print("\nExplanation:")
    print(result["explanation"])

    print("\nRelated Existing Skills:")
    print(result["related_skills"])

    print("\nPrerequisites:")
    print(result["prerequisites"])

    print("\nKnown Prerequisites:")
    print(result["known_prerequisites"])

    print("\nMissing Prerequisites:")
    print(result["missing_prerequisites"])

    print("\nSkill Domain:")
    print(result["skill_domain"])

    print("\nStudent Interests:")
    print(result["interests"])

    print("\nDomain Match:")
    print(result["domain_match"])

    print("\nMatched Interest Domain:")
    print(result["matched_interest_domain"])

    print("\n" + "=" * 60)
    print("SKILL EXPLANATION COMPLETED")
    print("=" * 60)


    # ==================================================
    # PROJECT EXPLANATION TEST
    # ==================================================

    project_name = "Personal Portfolio Website"

    project_result = explain_project_recommendation(
        student_id,
        project_name
    )

    print("\n")
    print("=" * 60)
    print("PROJECT EXPLANATION")
    print("=" * 60)

    print("\nStudent:", student_id)

    print(
        "Recommended Project:",
        project_result["project"]
    )

    print(
        "Domain:",
        project_result["domain"]
    )

    print("\nExplanation:")
    print(project_result["explanation"])

    print("\nRequired Skills:")
    print(project_result["required_skills"])

    print("\nKnown Required Skills:")
    print(project_result["known_skills"])

    print("\nMissing Skills:")
    print(project_result["missing_skills"])

    print("\nStudent Interests:")
    print(project_result["interests"])

    print("\nDomain Match:")
    print(project_result["domain_match"])

    print("\nMatched Interest Domain:")
    print(project_result["matched_interest_domain"])

    print("\n" + "=" * 60)
    print("PROJECT EXPLANATION COMPLETED")
    print("=" * 60)