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
# FIND SKILL FROM QUESTION
# --------------------------------------------------

def detect_skill(question, graph):
    """
    Detect the most appropriate Skill mentioned
    in the user's question.

    Longer skill names are checked first so that
    JavaScript is detected before Java.
    """

    normalized_question = question.lower()

    skill_names = []

    for node, data in graph.nodes(data=True):

        if data.get("label") != "Skill":
            continue

        skill_name = str(
            data.get("name", "")
        ).strip()

        if skill_name:
            skill_names.append(skill_name)

    # --------------------------------------------------
    # IMPORTANT:
    # Check longer names first.
    #
    # Example:
    # JavaScript before Java
    # Deep Learning before Learning
    # --------------------------------------------------

    skill_names.sort(
        key=len,
        reverse=True
    )

    for skill_name in skill_names:

        if skill_name.lower() in normalized_question:

            return skill_name

    return None


# --------------------------------------------------
# NATURAL LANGUAGE KNOWLEDGE GRAPH QUERY
# --------------------------------------------------

def query_knowledge_graph(question, student_id=None):
    """
    Process a natural-language question and retrieve
    relevant information from the Knowledge Graph.
    """

    graph = build_knowledge_graph()

    question = question.strip()

    if not question:

        return {
            "question": question,
            "intent": "unknown",
            "answer": "Please enter a question.",
            "results": []
        }

    normalized_question = question.lower()

    # --------------------------------------------------
    # DETECT SKILL
    # --------------------------------------------------

    detected_skill = detect_skill(
        question,
        graph
    )

    # ==================================================
    # INTENT 1
    # PREREQUISITES
    # ==================================================

    if (
        "prerequisite" in normalized_question
        or "prerequisites" in normalized_question
        or "what should i learn before" in normalized_question
        or "what do i need before" in normalized_question
        or "what skills do i need before" in normalized_question
    ):

        if detected_skill:

            skill_node = f"skill:{detected_skill}"

            prerequisites = []

            for source, target, edge_data in graph.in_edges(
                skill_node,
                data=True
            ):

                if edge_data.get(
                    "relation"
                ) != "PREREQUISITE_OF":

                    continue

                source_data = graph.nodes[source]

                if source_data.get(
                    "label"
                ) != "Skill":

                    continue

                prerequisite_name = source_data.get(
                    "name"
                )

                if prerequisite_name:
                    prerequisites.append(
                        prerequisite_name
                    )

            prerequisites = sorted(
                set(prerequisites)
            )

            return {
                "question": question,
                "intent": "prerequisite_search",
                "skill": detected_skill,
                "answer": (
                    f"{detected_skill} has "
                    f"{len(prerequisites)} "
                    f"prerequisite skill(s)."
                ),
                "results": prerequisites
            }

    # ==================================================
    # INTENT 2
    # COURSES FOR A SKILL
    # ==================================================

    if (
        "course" in normalized_question
        or "courses" in normalized_question
        or "learn" in normalized_question
    ):

        if detected_skill:

            skill_node = f"skill:{detected_skill}"

            courses = []

            for course_node, target, edge_data in graph.in_edges(
                skill_node,
                data=True
            ):

                if edge_data.get(
                    "relation"
                ) != "DEVELOPS":

                    continue

                course_data = graph.nodes[
                    course_node
                ]

                if course_data.get(
                    "label"
                ) != "Course":

                    continue

                courses.append({

                    "title":
                        course_data.get(
                            "title"
                        ),

                    "platform":
                        course_data.get(
                            "platform"
                        ),

                    "level":
                        course_data.get(
                            "level"
                        ),

                    "duration_hours":
                        course_data.get(
                            "duration_hours"
                        ),

                    "url":
                        course_data.get(
                            "url"
                        )
                })

            return {
                "question": question,
                "intent": "course_search",
                "skill": detected_skill,
                "answer": (
                    f"I found {len(courses)} "
                    f"course(s) that develop "
                    f"{detected_skill}."
                ),
                "results": courses
            }

    # ==================================================
    # INTENT 3
    # INTERNSHIPS FOR A SKILL
    # ==================================================

    if (
        "internship" in normalized_question
        or "internships" in normalized_question
        or "job" in normalized_question
        or "jobs" in normalized_question
    ):

        if detected_skill:

            skill_node = f"skill:{detected_skill}"

            internships = []

            for internship_node, target, edge_data in graph.in_edges(
                skill_node,
                data=True
            ):

                if edge_data.get(
                    "relation"
                ) != "REQUIRES":

                    continue

                internship_data = graph.nodes[
                    internship_node
                ]

                if internship_data.get(
                    "label"
                ) != "Internship":

                    continue

                internships.append({

                    "title":
                        internship_data.get(
                            "title"
                        ),

                    "company":
                        internship_data.get(
                            "company"
                        ),

                    "domain":
                        internship_data.get(
                            "domain"
                        ),

                    "level":
                        internship_data.get(
                            "level"
                        ),

                    "mode":
                        internship_data.get(
                            "mode"
                        ),

                    "duration_months":
                        internship_data.get(
                            "duration_months"
                        ),

                    "url":
                        internship_data.get(
                            "url"
                        )
                })

            return {
                "question": question,
                "intent": "internship_search",
                "skill": detected_skill,
                "answer": (
                    f"I found {len(internships)} "
                    f"internship(s) requiring "
                    f"{detected_skill}."
                ),
                "results": internships
            }

    # ==================================================
    # INTENT 4
    # PROJECTS FOR A SKILL
    # ==================================================

    if (
        "project" in normalized_question
        or "projects" in normalized_question
    ):

        if detected_skill:

            skill_node = f"skill:{detected_skill}"

            projects = []

            for project_node, target, edge_data in graph.in_edges(
                skill_node,
                data=True
            ):

                if edge_data.get(
                    "relation"
                ) != "REQUIRES":

                    continue

                project_data = graph.nodes[
                    project_node
                ]

                if project_data.get(
                    "label"
                ) != "Project":

                    continue

                projects.append({

                    "title":
                        project_data.get(
                            "title"
                        ),

                    "domain":
                        project_data.get(
                            "domain"
                        ),

                    "difficulty":
                        project_data.get(
                            "difficulty"
                        ),

                    "type":
                        project_data.get(
                            "type"
                        ),

                    "description":
                        project_data.get(
                            "description"
                        )
                })

            return {
                "question": question,
                "intent": "project_search",
                "skill": detected_skill,
                "answer": (
                    f"I found {len(projects)} "
                    f"project(s) that require "
                    f"{detected_skill}."
                ),
                "results": projects
            }

    # ==================================================
    # INTENT 5
    # STUDENT SKILLS
    # ==================================================

    if (
        student_id
        and (
            "my skills" in normalized_question
            or "my skill" in normalized_question
            or "what skills do i have"
            in normalized_question
        )
    ):

        student_node = f"student:{student_id}"

        if student_node in graph:

            skills = []

            for _, target, edge_data in graph.out_edges(
                student_node,
                data=True
            ):

                if edge_data.get(
                    "relation"
                ) != "HAS_SKILL":

                    continue

                skill_name = graph.nodes[
                    target
                ].get("name")

                if skill_name:
                    skills.append(
                        skill_name
                    )

            skills = sorted(
                set(skills)
            )

            return {
                "question": question,
                "intent": "student_skills",
                "answer": (
                    f"You currently have "
                    f"{len(skills)} skill(s) "
                    f"in your profile."
                ),
                "results": skills
            }

    # ==================================================
    # INTENT 6
    # PERSONALIZED INTERNSHIPS
    # ==================================================

    if (
        student_id
        and (
            "internships for me"
            in normalized_question

            or "internships can i get"
            in normalized_question

            or "internships suitable for me"
            in normalized_question
        )
    ):

        from src.recommender.internship_recommendation import (
            get_internship_recommendations
        )

        result = get_internship_recommendations(
            student_id,
            top_n=5
        )

        internships = []

        for internship in result.get(
            "internships",
            []
        ):

            internships.append({

                "title":
                    internship["title"],

                "company":
                    internship["company"],

                "domain":
                    internship["domain"],

                "score":
                    internship["score"],

                "matched_skills":
                    internship[
                        "matched_skills"
                    ],

                "missing_skills":
                    internship[
                        "missing_skills"
                    ]
            })

        return {
            "question": question,
            "intent":
                "personalized_internship_search",
            "answer":
                "Here are the internships "
                "recommended for your current "
                "skill profile.",
            "results": internships
        }

    # ==================================================
    # INTENT 7
    # PERSONALIZED COURSES
    # ==================================================

    if (
        student_id
        and (
            "courses for me"
            in normalized_question

            or "courses should i take"
            in normalized_question

            or "what should i learn"
            in normalized_question
        )
    ):

        return {
            "question": question,
            "intent":
                "personalized_course_search",
            "answer":
                "Use the Learning Roadmap "
                "and Course Recommendation "
                "Engine to find courses based "
                "on your skill gaps.",
            "results": []
        }

    # ==================================================
    # UNKNOWN QUESTION
    # ==================================================

    return {
        "question": question,
        "intent": "unknown",
        "answer": (
            "I could not understand the question. "
            "Try asking about courses, internships, "
            "projects, prerequisites, or your skills."
        ),
        "results": []
    }


# --------------------------------------------------
# DISPLAY RESULTS
# --------------------------------------------------

def print_query_result(result):

    print("=" * 60)
    print(
        "NATURAL LANGUAGE KNOWLEDGE GRAPH QUERY"
    )
    print("=" * 60)

    print(
        f"\nQuestion: "
        f"{result['question']}"
    )

    print(
        f"Intent: "
        f"{result.get('intent', 'unknown')}"
    )

    print(
        f"\nAnswer: "
        f"{result['answer']}"
    )

    results = result.get(
        "results",
        []
    )

    if not results:

        print(
            "\nNo additional results."
        )

    else:

        print("\nResults:")

        for index, item in enumerate(
            results,
            start=1
        ):

            if isinstance(
                item,
                dict
            ):

                print(
                    f"\n{index}. "
                    f"{item.get('title', 'Result')}"
                )

                for key, value in item.items():

                    if key == "title":
                        continue

                    print(
                        f"   {key}: {value}"
                    )

            else:

                print(
                    f"  {index}. {item}"
                )

    print(
        "\n" + "=" * 60
    )


# --------------------------------------------------
# TEST
# --------------------------------------------------

if __name__ == "__main__":

    test_questions = [

        "What courses can help me learn Python?",

        "Which internships require Java?",

        "What projects require JavaScript?",

        "What are the prerequisites for Deep Learning?",

        "What are my skills?"
    ]

    for question in test_questions:

        result = query_knowledge_graph(
            question,
            student_id="S01"
        )

        print_query_result(result)