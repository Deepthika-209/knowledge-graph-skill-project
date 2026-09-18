from src.recommender.recommendation_engine import get_recommendations


def evaluate_recommendations():

    student_ids = [
        f"S{i:02d}"
        for i in range(1, 26)
    ]

    total_students = len(student_ids)

    students_with_skill_recommendations = 0
    students_with_project_recommendations = 0

    total_skill_recommendations = 0
    total_project_recommendations = 0

    zero_score_projects = 0

    print("\n")
    print("=" * 60)
    print("RECOMMENDATION SYSTEM EVALUATION")
    print("=" * 60)

    for student_id in student_ids:

        result = get_recommendations(
            student_id,
            top_n=5
        )

        skills = result["skills"]
        projects = result["projects"]

        skill_count = len(skills)
        project_count = len(projects)

        total_skill_recommendations += skill_count
        total_project_recommendations += project_count

        if skill_count > 0:
            students_with_skill_recommendations += 1

        if project_count > 0:
            students_with_project_recommendations += 1

        for project in projects:
            if project["score"] == 0:
                zero_score_projects += 1

        print(
            f"{student_id} | "
            f"Skills: {skill_count} | "
            f"Projects: {project_count}"
        )

    skill_coverage = (
        students_with_skill_recommendations
        / total_students
    ) * 100

    project_coverage = (
        students_with_project_recommendations
        / total_students
    ) * 100

    average_skills = (
        total_skill_recommendations
        / total_students
    )

    average_projects = (
        total_project_recommendations
        / total_students
    )

    print("\n")
    print("=" * 60)
    print("EVALUATION SUMMARY")
    print("=" * 60)

    print(
        f"Total Students Tested       : "
        f"{total_students}"
    )

    print(
        f"Students with Skill Recs    : "
        f"{students_with_skill_recommendations}"
    )

    print(
        f"Skill Recommendation Coverage: "
        f"{skill_coverage:.2f}%"
    )

    print(
        f"Average Skill Recommendations: "
        f"{average_skills:.2f}"
    )

    print(
        f"Students with Project Recs  : "
        f"{students_with_project_recommendations}"
    )

    print(
        f"Project Recommendation Coverage: "
        f"{project_coverage:.2f}%"
    )

    print(
        f"Average Project Recommendations: "
        f"{average_projects:.2f}"
    )

    print(
        f"Zero-score Projects Returned: "
        f"{zero_score_projects}"
    )

    print("\n")
    print("=" * 60)
    print("EVALUATION COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    evaluate_recommendations()