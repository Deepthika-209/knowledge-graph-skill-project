from knowledge_graph import build_knowledge_graph


# Build the Knowledge Graph
kg = build_knowledge_graph()


# --------------------------------------------------
# QUERY 1: Get skills of a student
# --------------------------------------------------

def get_student_skills(student_id):

    student_node = f"student:{student_id}"

    skills = []

    for _, target, data in kg.out_edges(
        student_node,
        data=True
    ):

        if data["relation"] == "HAS_SKILL":

            skill_name = kg.nodes[target]["name"]

            proficiency = data["proficiency"]

            skills.append(
                (skill_name, proficiency)
            )

    return skills
# --------------------------------------------------
# QUERY 2: Get interests of a student
# --------------------------------------------------

def get_student_interests(student_id):

    student_node = f"student:{student_id}"

    interests = []

    for _, target, data in kg.out_edges(
        student_node,
        data=True
    ):

        if data["relation"] == "INTERESTED_IN":

            domain_name = kg.nodes[target]["name"]

            interests.append(domain_name)

    return interests
# --------------------------------------------------
# QUERY 3: Find skills related to student's skills
# --------------------------------------------------

def get_related_skills(student_id):

    student_node = f"student:{student_id}"

    related_skills = []

    # Find the student's existing skills
    for _, skill_node, student_edge in kg.out_edges(
        student_node,
        data=True
    ):

        if student_edge["relation"] != "HAS_SKILL":
            continue

        # Find skills related to the student's skill
        for _, related_node, relation_data in kg.out_edges(
            skill_node,
            data=True
        ):

            if relation_data["relation"] == "RELATED_TO":

                skill_name = kg.nodes[related_node]["name"]

                related_skills.append(
                    (
                        skill_name,
                        relation_data["strength"]
                    )
                )

    return related_skills

# --------------------------------------------------
# TEST THE QUERY
# --------------------------------------------------

if __name__ == "__main__":

    student_id = "S01"

    skills = get_student_skills(student_id)

    print("=" * 60)
    print("STUDENT SKILL QUERY")
    print("=" * 60)

    print(f"\nSkills of {student_id}:")

    for skill, proficiency in skills:

        print(
            f"- {skill} | Proficiency: {proficiency}"
        )
        interests = get_student_interests(student_id)

    print("\nInterests:")

    for interest in interests:

        print(f"- {interest}")
        related_skills = get_related_skills(student_id)

    print("\nRelated skills:")

    for skill, strength in related_skills:

        print(
            f"- {skill} | Strength: {strength}"
        )