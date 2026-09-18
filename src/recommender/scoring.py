from src.knowledge_graph import build_knowledge_graph
from src.recommender.skill_candidates import get_candidate_skills
from src.recommender.prerequisites import check_prerequisites


# Build the Knowledge Graph
kg = build_knowledge_graph()


def calculate_skill_score(student_id, skill_name, relatedness):
    """
    Calculate the initial score of a skill
    using Relatedness, Readiness, and Domain Fit.
    """

    # Check whether the student is ready for this skill
    prerequisite_result = check_prerequisites(
        student_id,
        skill_name
    )

    # -----------------------------
    # 1. Relatedness Score
    # -----------------------------

    relatedness_score = relatedness

    # -----------------------------
    # 2. Readiness Score
    # -----------------------------

    if prerequisite_result["ready"]:
        readiness_score = 1.0
    else:
        readiness_score = 0.0

    # -----------------------------
    # 3. Domain Fit Score
    # -----------------------------

    student_node = f"student:{student_id}"

    # Get domains the student is interested in
    interested_domains = set()

    for _, domain_node, data in kg.out_edges(
        student_node,
        data=True
    ):
        if data["relation"] == "INTERESTED_IN":
            interested_domains.add(
                kg.nodes[domain_node]["name"]
            )

    # Find the direct domain of the skill
    skill_node = f"skill:{skill_name}"
    skill_domain = None

    for _, domain_node, data in kg.out_edges(
        skill_node,
        data=True
    ):
        if data["relation"] == "BELONGS_TO":
            skill_domain = domain_node
            break

    # Check domain fit
    domain_fit_score = 0.0

    if skill_domain is not None:

        skill_domain_name = kg.nodes[skill_domain]["name"]

        # Direct domain match
        if skill_domain_name in interested_domains:
            domain_fit_score = 1.0

        else:

            # Check whether the skill's domain
            # is a subdomain of an interested domain
            for _, parent_node, data in kg.out_edges(
                skill_domain,
                data=True
            ):
                if data["relation"] == "SUBDOMAIN_OF":

                    parent_domain_name = kg.nodes[
                        parent_node
                    ]["name"]

                    if parent_domain_name in interested_domains:
                        domain_fit_score = 1.0
                        break

    # -----------------------------
    # Final Initial Score
    # -----------------------------

    score = (
        0.30 * relatedness_score
        + 0.25 * readiness_score
        + 0.45 * domain_fit_score
    )

    return {
        "skill": skill_name,
        "relatedness": relatedness_score,
        "readiness": readiness_score,
        "domain_fit": domain_fit_score,
        "score": score,
        "missing_prerequisites":
            prerequisite_result["missing_prerequisites"]
    }


if __name__ == "__main__":

    print("\nDOMAIN HIERARCHY CHECK")

    for node, data in kg.nodes(data=True):

        if data.get("label") == "Domain":

            for _, target, edge_data in kg.out_edges(
                node,
                data=True
            ):
                if edge_data["relation"] == "SUBDOMAIN_OF":
                    print(
                        f"{data['name']} "
                        f"SUBDOMAIN_OF "
                        f"{kg.nodes[target]['name']}"
                    )

    student_id = "S01"

    print("=" * 60)
    print("SKILL SCORING - INITIAL VERSION")
    print("=" * 60)

    candidates = get_candidate_skills(student_id)

    for skill, relatedness in candidates:

        result = calculate_skill_score(
            student_id,
            skill,
            relatedness
        )

        print(f"\nSkill: {result['skill']}")
        print(f"Relatedness: {result['relatedness']}")
        print(f"Readiness: {result['readiness']}")
        print(f"Domain Fit: {result['domain_fit']}")
        print(
            f"Missing Prerequisites: "
            f"{result['missing_prerequisites']}"
        )
        print(f"Initial Score: {result['score']:.3f}")

    print("\n" + "=" * 60)
    print("INITIAL SKILL SCORING COMPLETED")
    print("=" * 60)