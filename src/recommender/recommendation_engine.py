from src.recommender.ranking import rank_skills, rank_projects
from src.recommender.explanations import (
    explain_skill_recommendation,
    explain_project_recommendation
)


def get_recommendations(student_id, top_n=5):
    """
    Generate complete skill and project recommendations
    with scores and explanations for a student.
    """

    # ----------------------------------------
    # 1. Get ranked skill recommendations
    # ----------------------------------------
    ranked_skills = rank_skills(student_id)

    skill_recommendations = []

    for skill in ranked_skills[:top_n]:

        explanation = explain_skill_recommendation(
            student_id,
            skill["skill"]
        )

        skill_recommendations.append({
            "skill": skill["skill"],
            "score": skill["score"],
            "missing_prerequisites": skill["missing_prerequisites"],
            "explanation": explanation["explanation"]
        })

    # ----------------------------------------
    # 2. Get ranked project recommendations
    # ----------------------------------------
    ranked_projects = rank_projects(student_id)

    project_recommendations = []
    positive_projects = [
    project
    for project in ranked_projects
    if project["score"] > 0
    ]

    for project in positive_projects[:top_n]:

        explanation = explain_project_recommendation(
            student_id,
            project["project"]
        )

        project_recommendations.append({
            "project": project["project"],
            "score": project["score"],
            "domain": project["domain"],
            "known_skills": project["known_skills"],
            "missing_skills": project["missing_skills"],
            "explanation": explanation["explanation"]
        })

    # ----------------------------------------
    # 3. Return complete result
    # ----------------------------------------
    return {
        "student_id": student_id,
        "skills": skill_recommendations,
        "projects": project_recommendations
    }


# ----------------------------------------
# Test all sample students
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

        result = get_recommendations(
            student_id,
            top_n=5
        )

        print("\n")
        print("========================================")
        print(f"STUDENT: {student_id}")
        print("========================================")

        # ----------------------------------------
        # Skill recommendations
        # ----------------------------------------

        print("\nSKILL RECOMMENDATIONS")
        print("----------------------------------------")

        if len(result["skills"]) == 0:
            print("No skill recommendations found.")

        else:
            for index, skill in enumerate(
                result["skills"],
                start=1
            ):

                print(
                    f"{index}. "
                    f"{skill['skill']} | "
                    f"Score: {skill['score']:.3f}"
                )

                if skill["missing_prerequisites"]:
                    print(
                        "   Missing Prerequisites:",
                        skill["missing_prerequisites"]
                    )

        # ----------------------------------------
        # Project recommendations
        # ----------------------------------------

        print("\nPROJECT RECOMMENDATIONS")
        print("----------------------------------------")

        if len(result["projects"]) == 0:
            print("No project recommendations found.")

        else:
            for index, project in enumerate(
                result["projects"],
                start=1
            ):

                print(
                    f"{index}. "
                    f"{project['project']} | "
                    f"Score: {project['score']:.3f}"
                )

                print(
                    f"   Domain: {project['domain']}"
                )

                if project["known_skills"]:
                    print(
                        "   Known Skills:",
                        project["known_skills"]
                    )

                if project["missing_skills"]:
                    print(
                        "   Missing Skills:",
                        project["missing_skills"]
                    )