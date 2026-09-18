from src.knowledge_graph import build_knowledge_graph


# Build the Knowledge Graph
kg = build_knowledge_graph()


def get_candidate_skills(student_id):
    """
    Find new skill candidates for a student.

    Primary method:
    Use RELATED_TO relationships from the student's
    existing skills.

    Fallback method:
    If no related candidates are found, use skills
    belonging to the student's interested domain.
    """

    student_node = f"student:{student_id}"

    # ----------------------------------------
    # Step 1: Get skills the student already knows
    # ----------------------------------------
    known_skills = set()

    for _, skill_node, data in kg.out_edges(
        student_node,
        data=True
    ):

        if data["relation"] == "HAS_SKILL":

            skill_name = kg.nodes[skill_node]["name"]

            known_skills.add(skill_name)

    # ----------------------------------------
    # Step 2: Get student's interested domains
    # ----------------------------------------
    interested_domains = set()

    for _, domain_node, data in kg.out_edges(
        student_node,
        data=True
    ):

        if data["relation"] == "INTERESTED_IN":

            domain_name = kg.nodes[domain_node]["name"]

            interested_domains.add(domain_name)

    # ----------------------------------------
    # Step 3: Find RELATED_TO candidates
    # ----------------------------------------
    candidates = {}

    for skill_name in known_skills:

        skill_node = f"skill:{skill_name}"

        for _, related_node, data in kg.out_edges(
            skill_node,
            data=True
        ):

            if data["relation"] != "RELATED_TO":
                continue

            related_skill = kg.nodes[related_node]["name"]

            strength = data["strength"]

            # Do not recommend skills already known
            if related_skill in known_skills:
                continue

            # ----------------------------------------
            # Find candidate skill's domain
            # ----------------------------------------
            related_skill_domain = None

            for _, domain_node, domain_data in kg.out_edges(
                related_node,
                data=True
            ):

                if domain_data["relation"] == "BELONGS_TO":

                    related_skill_domain = domain_node

                    break

            # ----------------------------------------
            # Check domain relevance
            # ----------------------------------------
            domain_match = False

            if related_skill_domain is not None:

                related_domain_name = kg.nodes[
                    related_skill_domain
                ]["name"]

                # Direct domain match
                if related_domain_name in interested_domains:

                    domain_match = True

                else:

                    # Check subdomain hierarchy
                    for _, parent_node, hierarchy_data in kg.out_edges(
                        related_skill_domain,
                        data=True
                    ):

                        if hierarchy_data["relation"] == "SUBDOMAIN_OF":

                            parent_domain_name = kg.nodes[
                                parent_node
                            ]["name"]

                            if parent_domain_name in interested_domains:

                                domain_match = True

                                break

            # ----------------------------------------
            # Keep only domain-relevant candidates
            # ----------------------------------------
            if not domain_match:
                continue

            # ----------------------------------------
            # Keep strongest relationship
            # ----------------------------------------
            if (
                related_skill not in candidates
                or strength > candidates[related_skill]
            ):

                candidates[related_skill] = strength

    # ----------------------------------------
    # Step 4: Domain-based fallback
    # ----------------------------------------
    if len(candidates) == 0:

        for skill_node, skill_data in kg.nodes(data=True):

            if skill_data.get("label") != "Skill":
                continue

            skill_name = skill_data["name"]

            # Do not recommend already-known skills
            if skill_name in known_skills:
                continue

            # Find skill's domain
            skill_domain = None

            for _, domain_node, domain_data in kg.out_edges(
                skill_node,
                data=True
            ):

                if domain_data["relation"] == "BELONGS_TO":

                    skill_domain = domain_node

                    break

            if skill_domain is None:
                continue

            skill_domain_name = kg.nodes[
                skill_domain
            ]["name"]

            # ----------------------------------------
            # Direct domain match
            # ----------------------------------------
            if skill_domain_name in interested_domains:

                candidates[skill_name] = 0.50

                continue

            # ----------------------------------------
            # Subdomain match
            # ----------------------------------------
            for _, parent_node, hierarchy_data in kg.out_edges(
                skill_domain,
                data=True
            ):

                if hierarchy_data["relation"] == "SUBDOMAIN_OF":

                    parent_domain_name = kg.nodes[
                        parent_node
                    ]["name"]

                    if parent_domain_name in interested_domains:

                        candidates[skill_name] = 0.50

                        break

    # ----------------------------------------
    # Step 5: Sort candidates
    # ----------------------------------------
    result = sorted(
        candidates.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return result


# ----------------------------------------
# Test candidate generation
# ----------------------------------------

if __name__ == "__main__":

    student_ids = [
        "S01",
        "S02",
        "S03",
        "S04",
        "S05",
        "S06"
    ]

    for student_id in student_ids:

        print("\n" + "=" * 60)
        print(f"STUDENT: {student_id}")
        print("=" * 60)

        candidates = get_candidate_skills(student_id)

        print("\nDomain-Relevant Skill Candidates:")

        if len(candidates) == 0:

            print("No domain-relevant skill candidates found.")

        else:

            for skill, strength in candidates:

                print(
                    f"- {skill} | "
                    f"Candidate Strength: {strength}"
                )

    print("\n" + "=" * 60)
    print("DOMAIN-AWARE CANDIDATE GENERATION COMPLETED")
    print("=" * 60)