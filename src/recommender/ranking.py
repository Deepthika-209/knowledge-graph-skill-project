from src.recommender.skill_candidates import get_candidate_skills
from src.recommender.scoring import calculate_skill_score

from src.recommender.project_candidates import get_project_candidates
from src.recommender.project_scoring import calculate_project_score


# --------------------------------------------------
# SKILL RANKING
# --------------------------------------------------

def rank_skills(student_id):

    # Get candidate skills
    candidates = get_candidate_skills(student_id)

    scored_skills = []

    # Calculate score for every candidate
    for skill_name, relatedness in candidates:

        result = calculate_skill_score(
            student_id,
            skill_name,
            relatedness
        )

        scored_skills.append(result)

    # Sort skills by score from highest to lowest
    ranked_skills = sorted(
        scored_skills,
        key=lambda x: x["score"],
        reverse=True
    )

    return ranked_skills


# --------------------------------------------------
# PROJECT RANKING
# --------------------------------------------------

def rank_projects(student_id):

    # Get candidate projects
    candidates = get_project_candidates(student_id)

    scored_projects = []

    # Calculate score for every project
    for candidate in candidates:


        result = calculate_project_score(
            student_id,candidate
        )

        scored_projects.append(result)

     

    # Sort projects by score from highest to lowest
    ranked_projects = sorted(
        scored_projects,
        key=lambda x: x["score"],
        reverse=True
    )

    return ranked_projects


# --------------------------------------------------
# TEST SKILL AND PROJECT RANKING
# --------------------------------------------------

if __name__ == "__main__":

    student_id = "S01"

    # --------------------------------------------------
    # SKILL RANKING
    # --------------------------------------------------

    print("=" * 60)
    print("SKILL RANKING")
    print("=" * 60)

    ranked_skills = rank_skills(student_id)

    print(f"\nStudent: {student_id}")

    print("\nRanked Skill Recommendations:")

    for rank, result in enumerate(
        ranked_skills,
        start=1
    ):

        print(
            f"{rank}. {result['skill']} "
            f"| Score: {result['score']:.3f}"
        )

        if result["missing_prerequisites"]:

            print(
                f"   Missing Prerequisites: "
                f"{result['missing_prerequisites']}"
            )

    print("\n" + "=" * 60)
    print("SKILL RANKING COMPLETED")
    print("=" * 60)


    # --------------------------------------------------
    # PROJECT RANKING
    # --------------------------------------------------

    print("\n")
    print("=" * 60)
    print("PROJECT RANKING")
    print("=" * 60)

    ranked_projects = rank_projects(student_id)

    print(f"\nStudent: {student_id}")

    print("\nRanked Project Recommendations:")

    for rank, result in enumerate(
        ranked_projects,
        start=1
    ):

        print(
            f"{rank}. {result['project']} "
            f"| Score: {result['score']:.3f}"
        )

        if result["missing_skills"]:

            print(
                f"   Missing Skills: "
                f"{result['missing_skills']}"
            )

    print("\n" + "=" * 60)
    print("PROJECT RANKING COMPLETED")
    print("=" * 60)