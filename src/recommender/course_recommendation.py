from src.knowledge_graph import build_knowledge_graph
from src.recommender.learning_roadmap import generate_learning_roadmap


def get_course_recommendations(student_id, target_skill, top_n=5):
    """
    Recommend courses based on the student's
    missing skills and personalized learning roadmap.
    """

    # --------------------------------------------------
    # 1. BUILD FRESH KNOWLEDGE GRAPH
    # --------------------------------------------------

    kg = build_knowledge_graph()

    student_node = f"student:{student_id}"
    target_node = f"skill:{target_skill}"

    # --------------------------------------------------
    # 2. VALIDATE STUDENT
    # --------------------------------------------------

    if student_node not in kg:

        return {
            "student_id": student_id,
            "target_skill": target_skill,
            "missing_skills": [],
            "courses": [],
            "message": "Student not found."
        }

    # --------------------------------------------------
    # 3. VALIDATE TARGET SKILL
    # --------------------------------------------------

    if target_node not in kg:

        return {
            "student_id": student_id,
            "target_skill": target_skill,
            "missing_skills": [],
            "courses": [],
            "message": "Target skill not found."
        }

    # --------------------------------------------------
    # 4. GET PERSONALIZED LEARNING ROADMAP
    # --------------------------------------------------

    roadmap_result = generate_learning_roadmap(
        student_id,
        target_skill
    )

    missing_skills = roadmap_result.get(
        "missing_skills",
        []
    )

    missing_skill_set = set(missing_skills)

    # --------------------------------------------------
    # 5. FIND COURSES
    # --------------------------------------------------

    course_recommendations = []

    for course_node, course_data in kg.nodes(data=True):

        # Our graph uses "label" for node type
        if course_data.get("label") != "Course":
            continue

        covered_skills = []

        # --------------------------------------------------
        # 6. CHECK COURSE SUCCESSORS
        # --------------------------------------------------

        for skill_node in kg.successors(course_node):

            # Only consider Skill nodes
            if kg.nodes[skill_node].get("label") != "Skill":
                continue

            # Get edge information
            edge_data = kg.get_edge_data(
                course_node,
                skill_node
            )

            if not edge_data:
                continue

            # NetworkX MultiDiGraph structure:
            # {0: {"relation": "DEVELOPS", "relevance": 1.0}}
            for _, relationship in edge_data.items():

                if relationship.get("relation") != "DEVELOPS":
                    continue

                skill_name = kg.nodes[skill_node].get(
                    "name"
                )

                if skill_name:
                    covered_skills.append(
                        {
                            "name": skill_name,
                            "relevance": relationship.get(
                                "relevance",
                                1.0
                            )
                        }
                    )

        # --------------------------------------------------
        # 7. FIND MISSING SKILLS COVERED BY COURSE
        # --------------------------------------------------

        missing_covered = [
            skill
            for skill in covered_skills
            if skill["name"] in missing_skill_set
        ]

        # Skip courses that do not help the student
        if not missing_covered:
            continue

        # --------------------------------------------------
        # 8. CALCULATE SCORE
        # --------------------------------------------------

        score = 0.0

        # Contribution from every missing skill covered
        for skill in missing_covered:

            score += (
                0.50 *
                skill["relevance"]
            )

        # Direct target-skill bonus
        target_skill_covered = any(
            skill["name"] == target_skill
            for skill in missing_covered
        )

        if target_skill_covered:
            score += 0.40

        # Beginner / intermediate accessibility bonus
        level = str(
            course_data.get("level", "")
        ).lower()

        if level == "beginner":
            score += 0.10

        elif level == "intermediate":
            score += 0.05

        # --------------------------------------------------
        # 9. GET SKILL NAMES
        # --------------------------------------------------

        skill_names = [
            skill["name"]
            for skill in missing_covered
        ]

        skills_text = ", ".join(skill_names)

        # --------------------------------------------------
        # 10. GENERATE EXPLANATION
        # --------------------------------------------------

        if target_skill_covered:

            explanation = (
                f"This course directly develops "
                f"{skills_text}, including your target "
                f"skill {target_skill}."
            )

        else:

            explanation = (
                f"This course develops "
                f"{skills_text}, which are missing "
                f"from your current skill profile."
            )

        # --------------------------------------------------
        # 11. STORE COURSE
        # --------------------------------------------------

        course_recommendations.append({

            "course_id": course_data.get(
                "course_id"
            ),

            "title": course_data.get(
                "title"
            ),

            "platform": course_data.get(
                "platform"
            ),

            "domain": course_data.get(
                "domain"
            ),

            "level": course_data.get(
                "level"
            ),

            "duration_hours": course_data.get(
                "duration_hours"
            ),

            "url": course_data.get(
                "url"
            ),

            "skills_covered": skill_names,

            "score": round(
                score,
                3
            ),

            "explanation": explanation
        })

    # --------------------------------------------------
    # 12. SORT BY SCORE
    # --------------------------------------------------

    course_recommendations.sort(
        key=lambda course: course["score"],
        reverse=True
    )

    # --------------------------------------------------
    # 13. RETURN TOP COURSES
    # --------------------------------------------------

    course_recommendations = (
        course_recommendations[:top_n]
    )

    return {

        "student_id": student_id,

        "target_skill": target_skill,

        "missing_skills": missing_skills,

        "courses": course_recommendations,

        "message": (
            f"Found "
            f"{len(course_recommendations)} "
            f"recommended course(s)."
            if course_recommendations
            else "No suitable courses found."
        )
    }


# ==========================================================
# TEST
# ==========================================================

if __name__ == "__main__":

    student_id = "S01"

    target_skill = "Deep Learning"

    result = get_course_recommendations(
        student_id,
        target_skill,
        top_n=5
    )

    print()
    print("=" * 60)
    print("COURSE RECOMMENDATION ENGINE")
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
        "\nMissing Skills:"
    )

    for skill in result["missing_skills"]:

        print(
            "  -",
            skill
        )

    print(
        "\nRecommended Courses:"
    )

    if result["courses"]:

        for index, course in enumerate(
            result["courses"],
            start=1
        ):

            print()
            print(
                f"{index}. "
                f"{course['title']}"
            )

            print(
                f"   Course ID: "
                f"{course['course_id']}"
            )

            print(
                f"   Platform: "
                f"{course['platform']}"
            )

            print(
                f"   Level: "
                f"{course['level']}"
            )

            print(
                f"   Duration: "
                f"{course['duration_hours']} hours"
            )

            print(
                f"   Skills Covered: "
                f"{', '.join(course['skills_covered'])}"
            )

            print(
                f"   Score: "
                f"{course['score']}"
            )

            print(
                f"   Explanation: "
                f"{course['explanation']}"
            )

            print(
                f"   URL: "
                f"{course['url']}"
            )

    else:

        print(
            "  No suitable courses found."
        )

    print()
    print(
        "Message:",
        result["message"]
    )

    print("=" * 60)
    print(
        "COURSE RECOMMENDATION TEST COMPLETED"
    )
    print("=" * 60)