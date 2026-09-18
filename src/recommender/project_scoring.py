
from src.knowledge_graph import build_knowledge_graph
from src.recommender.project_candidates import get_project_candidates


# --------------------------------------------------
# BUILD KNOWLEDGE GRAPH
# --------------------------------------------------

kg = build_knowledge_graph()


# --------------------------------------------------
# PROJECT SCORING
# --------------------------------------------------

def calculate_project_score(student_id, candidate):

    # --------------------------------------------------
    # 1. GET PROJECT INFORMATION
    # --------------------------------------------------

    project_name = candidate["project"]
    project_domain = candidate["domain"]

    required_skills = candidate["required_skills"]
    known_skills = candidate["known_skills"]
    missing_skills = candidate["missing_skills"]

    # --------------------------------------------------
    # 2. FULL COVERAGE
    # --------------------------------------------------
    # Measures how many of the project's required
    # skills are already known by the student.

    if len(required_skills) == 0:

        full_coverage = 0.0

    else:

        full_coverage = (
            len(known_skills) /
            len(required_skills)
        )

    # --------------------------------------------------
    # 3. CORE COVERAGE
    # --------------------------------------------------
    # Core skills are the important skills required
    # by the project.
    #
    # The dataset represents importance using values
    # such as "core" and "supporting".

    project_node = f"project:{project_name}"

    core_skills = []
    known_core_skills = []

    for _, skill_node, edge_data in kg.out_edges(
        project_node,
        data=True
    ):

        if edge_data["relation"] != "REQUIRES":
            continue

        importance = str(
            edge_data["importance"]
        ).strip().lower()

        skill_name = kg.nodes[skill_node]["name"]

        if importance == "core":

            core_skills.append(skill_name)

            if skill_name in known_skills:

                known_core_skills.append(skill_name)

    if len(core_skills) == 0:

        core_coverage = 0.0

    else:

        core_coverage = (
            len(known_core_skills) /
            len(core_skills)
        )

    # --------------------------------------------------
    # 4. LEARNING VALUE
    # --------------------------------------------------
    # Learning value represents how much useful new
    # learning the project can provide.
    #
    # It is only a supporting factor and should not
    # overpower domain relevance and skill coverage.

    missing_count = len(missing_skills)

    if missing_count == 0:

        learning_value = 0.20

    elif missing_count <= 2:

        learning_value = 0.60

    elif missing_count <= 4:

        learning_value = 0.80

    else:

        learning_value = 0.50

    # --------------------------------------------------
    # 5. DOMAIN MATCH
    # --------------------------------------------------
    # A project gets a domain match when:
    #
    # 1. Its domain directly matches an interested
    #    student domain, OR
    #
    # 2. Its domain is a subdomain of an interested
    #    student domain.

    student_node = f"student:{student_id}"

    interested_domains = set()

    for _, domain_node, edge_data in kg.out_edges(
        student_node,
        data=True
    ):

        if edge_data["relation"] == "INTERESTED_IN":

            interested_domains.add(
                kg.nodes[domain_node]["name"]
            )

    domain_match = 0.0

    # Direct domain match
    if project_domain in interested_domains:

        domain_match = 1.0

    else:

        # Check whether project domain is a subdomain
        # of one of the student's interested domains.

        domain_node = f"domain:{project_domain}"

        for _, parent_node, edge_data in kg.out_edges(
            domain_node,
            data=True
        ):

            if edge_data["relation"] == "SUBDOMAIN_OF":

                parent_domain = kg.nodes[
                    parent_node
                ]["name"]

                if parent_domain in interested_domains:

                    domain_match = 1.0
                    break

    # --------------------------------------------------
    # 6. DIFFICULTY FIT
    # --------------------------------------------------

    project_data = kg.nodes[
        project_node
    ]

    project_difficulty = project_data["difficulty"]

    student_data = kg.nodes[
        student_node
    ]

    student_level = student_data["level"]

    # Convert student level into numeric level.

    level_values = {
        "Beginner": 1,
        "Intermediate": 2,
        "Advanced": 3
    }

    student_difficulty = level_values.get(
        student_level,
        1
    )

    # Calculate difficulty difference.

    difficulty_difference = abs(
        project_difficulty -
        student_difficulty
    )

    if difficulty_difference == 0:

        difficulty_fit = 1.0

    elif difficulty_difference == 1:

        difficulty_fit = 0.7

    else:

        difficulty_fit = 0.3

    # --------------------------------------------------
    # 7. BASE PROJECT SCORE
    # --------------------------------------------------
    #
    # Core Coverage  -> 30%
    # Full Coverage  -> 25%
    # Domain Match   -> 30%
    # Learning Value -> 10%
    # Difficulty Fit -> 5%
    #
    # Total = 100%
    #
    # Domain relevance and skill compatibility are
    # therefore the strongest factors.

    score = (
        0.30 * core_coverage
        + 0.25 * full_coverage
        + 0.30 * domain_match
        + 0.10 * learning_value
        + 0.05 * difficulty_fit
    )

    # --------------------------------------------------
    # 8. CROSS-DOMAIN RELEVANCE PENALTY
    # --------------------------------------------------
    # If the project does not match the student's
    # interested domain, it should not outrank a
    # domain-relevant project merely because of one
    # generic overlapping skill.
    #
    # A cross-domain project with no skill coverage
    # receives zero.
    #
    # A cross-domain project with some skill coverage
    # remains possible, but its score is reduced.

    if domain_match == 0.0:

        if full_coverage == 0.0:

            score = 0.0

        else:

            score = score * 0.40

    # --------------------------------------------------
    # 9. RETURN RESULT
    # --------------------------------------------------

    return {
        "project": project_name,
        "domain": project_domain,
        "core_coverage": core_coverage,
        "full_coverage": full_coverage,
        "learning_value": learning_value,
        "domain_match": domain_match,
        "difficulty_fit": difficulty_fit,
        "score": score,
        "known_skills": known_skills,
        "missing_skills": missing_skills
    }


# --------------------------------------------------
# TEST PROJECT SCORING
# --------------------------------------------------

if __name__ == "__main__":

    student_id = "S01"

    print("=" * 60)
    print("PROJECT SCORING")
    print("=" * 60)

    candidates = get_project_candidates(
        student_id
    )

    for candidate in candidates:

        result = calculate_project_score(
            student_id,
            candidate
        )

        print(f"\nProject: {result['project']}")
        print(f"Domain: {result['domain']}")

        print(
            f"Core Coverage: "
            f"{result['core_coverage']:.2f}"
        )

        print(
            f"Full Coverage: "
            f"{result['full_coverage']:.2f}"
        )

        print(
            f"Learning Value: "
            f"{result['learning_value']:.2f}"
        )

        print(
            f"Domain Match: "
            f"{result['domain_match']:.2f}"
        )

        print(
            f"Difficulty Fit: "
            f"{result['difficulty_fit']:.2f}"
        )

        print(
            f"Known Skills: "
            f"{result['known_skills']}"
        )

        print(
            f"Missing Skills: "
            f"{result['missing_skills']}"
        )

        print(
            f"Project Score: "
            f"{result['score']:.3f}"
        )

    print("\n" + "=" * 60)
    print("PROJECT SCORING COMPLETED")
    print("=" * 60)
