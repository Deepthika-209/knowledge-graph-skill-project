import sys
from pathlib import Path

# --------------------------------------------------
# PROJECT PATH
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.knowledge_graph import build_knowledge_graph


# --------------------------------------------------
# INTERNSHIP RECOMMENDATION ENGINE
# --------------------------------------------------

def get_internship_recommendations(student_id, top_n=5):
    """
    Generate internship recommendations for a student
    based on connected skills in the Knowledge Graph.
    """

    # Always build a fresh graph
    graph = build_knowledge_graph()

    student_node = f"student:{student_id}"

    # --------------------------------------------------
    # CHECK STUDENT
    # --------------------------------------------------

    if student_node not in graph:
        return {
            "student_id": student_id,
            "internships": [],
            "message": "Student not found in the Knowledge Graph."
        }

    # --------------------------------------------------
    # GET STUDENT KNOWN SKILLS
    # --------------------------------------------------

    known_skills = set()

    for _, target, data in graph.out_edges(
        student_node,
        data=True
    ):

        if data.get("relation") == "HAS_SKILL":

            skill_name = graph.nodes[target].get("name")

            if skill_name:
                known_skills.add(skill_name)

    # --------------------------------------------------
    # GET STUDENT INTERESTED DOMAINS
    # --------------------------------------------------

    interested_domains = set()

    for _, target, data in graph.out_edges(
        student_node,
        data=True
    ):

        if data.get("relation") == "INTERESTED_IN":

            domain_name = graph.nodes[target].get("name")

            if domain_name:
                interested_domains.add(domain_name)

    # --------------------------------------------------
    # FIND INTERNSHIPS
    # --------------------------------------------------

    internship_nodes = [
        node
        for node, data in graph.nodes(data=True)
        if data.get("label") == "Internship"
    ]

    recommendations = []

    for internship_node in internship_nodes:

        internship_data = graph.nodes[internship_node]

        internship_title = internship_data.get("title")

        # --------------------------------------------------
        # REQUIRED SKILLS
        # --------------------------------------------------

        required_skills = set()

        for _, skill_node, edge_data in graph.out_edges(
            internship_node,
            data=True
        ):

            if edge_data.get("relation") != "REQUIRES":
                continue

            skill_name = graph.nodes[skill_node].get("name")

            if skill_name:
                required_skills.add(skill_name)

        # --------------------------------------------------
        # MATCHING SKILLS
        # --------------------------------------------------

        matched_skills = sorted(
            known_skills.intersection(required_skills)
        )

        missing_skills = sorted(
            required_skills - known_skills
        )

        # --------------------------------------------------
        # CALCULATE SKILL MATCH SCORE
        # --------------------------------------------------

        if required_skills:

            skill_match_score = (
                len(matched_skills)
                / len(required_skills)
            )

        else:

            skill_match_score = 0.0

        # --------------------------------------------------
        # DOMAIN MATCH
        # --------------------------------------------------

        internship_domain = internship_data.get("domain")

        domain_match = (
            internship_domain in interested_domains
        )

        # --------------------------------------------------
        # FINAL SCORE
        # --------------------------------------------------

        final_score = skill_match_score

        if domain_match:
            final_score += 0.20

        # Cap score at 1.0
        final_score = min(final_score, 1.0)

        # --------------------------------------------------
        # EXPLANATION
        # --------------------------------------------------

        if matched_skills and domain_match:

            explanation = (
                f"This internship matches your "
                f"{len(matched_skills)} known skill(s) "
                f"and belongs to your interested domain."
            )

        elif matched_skills:

            explanation = (
                f"This internship matches your "
                f"{len(matched_skills)} known skill(s)."
            )

        elif domain_match:

            explanation = (
                "This internship belongs to your "
                "interested domain, but you need to "
                "develop the required skills."
            )

        else:

            explanation = (
                "This internship requires skills that "
                "are not yet present in your profile."
            )

        # --------------------------------------------------
        # STORE RESULT
        # --------------------------------------------------

        recommendations.append({

            "internship_id":
                internship_data.get("internship_id"),

            "title":
                internship_title,

            "company":
                internship_data.get("company"),

            "domain":
                internship_domain,

            "level":
                internship_data.get("level"),

            "duration_months":
                internship_data.get("duration_months"),

            "location":
                internship_data.get("location"),

            "mode":
                internship_data.get("mode"),

            "url":
                internship_data.get("url"),

            "required_skills":
                sorted(required_skills),

            "matched_skills":
                matched_skills,

            "missing_skills":
                missing_skills,

            "skill_match_score":
                round(skill_match_score, 3),

            "domain_match":
                domain_match,

            "score":
                round(final_score, 3),

            "explanation":
                explanation
        })

    # --------------------------------------------------
    # RANK INTERNSHIPS
    # --------------------------------------------------

    recommendations.sort(
        key=lambda item: (
            item["score"],
            item["skill_match_score"]
        ),
        reverse=True
    )

    # --------------------------------------------------
    # RETURN TOP RESULTS
    # --------------------------------------------------

    return {
        "student_id": student_id,
        "known_skills": sorted(known_skills),
        "interested_domains": sorted(interested_domains),
        "internships": recommendations[:top_n],
        "message": (
            f"Found {min(top_n, len(recommendations))} "
            "internship recommendation(s)."
        )
    }


# --------------------------------------------------
# TEST
# --------------------------------------------------

if __name__ == "__main__":

    STUDENT_ID = "S01"

    result = get_internship_recommendations(
        STUDENT_ID,
        top_n=5
    )

    print("=" * 60)
    print("INTERNSHIP RECOMMENDATION ENGINE")
    print("=" * 60)

    print(
        f"\nStudent: {result['student_id']}"
    )

    print("\nKnown Skills:")

    for skill in result["known_skills"]:

        print(f"  ✓ {skill}")

    print("\nInterested Domains:")

    for domain in result["interested_domains"]:

        print(f"  • {domain}")

    print("\nRecommended Internships:")

    for index, internship in enumerate(
        result["internships"],
        start=1
    ):

        print(
            f"\n{index}. "
            f"{internship['title']}"
        )

        print(
            f"   Internship ID: "
            f"{internship['internship_id']}"
        )

        print(
            f"   Company: "
            f"{internship['company']}"
        )

        print(
            f"   Domain: "
            f"{internship['domain']}"
        )

        print(
            f"   Level: "
            f"{internship['level']}"
        )

        print(
            f"   Duration: "
            f"{internship['duration_months']} months"
        )

        print(
            f"   Mode: "
            f"{internship['mode']}"
        )

        print(
            f"   Matched Skills: "
            f"{', '.join(internship['matched_skills'])}"
        )

        print(
            f"   Missing Skills: "
            f"{', '.join(internship['missing_skills'])}"
        )

        print(
            f"   Skill Match: "
            f"{internship['skill_match_score']}"
        )

        print(
            f"   Final Score: "
            f"{internship['score']}"
        )

        print(
            f"   Explanation: "
            f"{internship['explanation']}"
        )

        print(
            f"   URL: "
            f"{internship['url']}"
        )

    print(
        f"\nMessage: {result['message']}"
    )

    print("=" * 60)
    print("INTERNSHIP RECOMMENDATION TEST COMPLETED")
    print("=" * 60)