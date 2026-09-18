import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path

from src.recommender.recommendation_engine import get_recommendations
from src.visualization import create_knowledge_graph_visualization


# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="Skill & Project Recommendation System",
    page_icon="🎓",
    layout="wide"
)


# ---------------------------------------------------------
# CUSTOM STYLING
# ---------------------------------------------------------

st.markdown(
    """
    <style>

    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }

    .subtitle {
        color: #666666;
        font-size: 1.05rem;
        margin-bottom: 1.5rem;
    }

    .section-title {
        font-size: 1.45rem;
        font-weight: 650;
        margin-top: 1.2rem;
        margin-bottom: 0.8rem;
    }

    .info-card {
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #dddddd;
        background-color: #fafafa;
        margin-bottom: 0.8rem;
    }

    .small-label {
        color: #666666;
        font-size: 0.85rem;
        margin-bottom: 0.2rem;
    }

    .profile-value {
        font-size: 1rem;
        font-weight: 600;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# TITLE
# ---------------------------------------------------------

st.markdown(
    '<div class="main-title">'
    'Knowledge Graph-Based Personalized Skill & Project '
    'Recommendation System'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'A Knowledge Graph-based system that recommends '
    'skills and projects based on a student profile.'
    '</div>',
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# STUDENT DATA
# ---------------------------------------------------------

students_df = pd.read_csv(
    "data/sample_students.csv"
)

students = dict(
    zip(
        students_df["student_id"],
        students_df["name"]
    )
)


# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

st.sidebar.header("Student Selection")

selected_student = st.sidebar.selectbox(
    "Select Student",
    list(students.keys()),
    format_func=lambda student_id:
        f"{student_id} - {students[student_id]}"
)

student_id = selected_student

student_profile = students_df[
    students_df["student_id"] == student_id
].iloc[0]


st.sidebar.markdown("---")

st.sidebar.subheader("Selected Profile")

st.sidebar.write(
    f"**Name:** {student_profile['name']}"
)

st.sidebar.write(
    f"**Level:** {student_profile['level']}"
)

st.sidebar.write(
    f"**Interest:** {student_profile['interests']}"
)


# ---------------------------------------------------------
# CURRENT SKILLS
# ---------------------------------------------------------

current_skills = [
    skill.strip()
    for skill in str(
        student_profile["skills"]
    ).split(";")
    if skill.strip()
]


# ---------------------------------------------------------
# GENERATE RECOMMENDATIONS
# ---------------------------------------------------------

result = get_recommendations(
    student_id,
    top_n=5
)

recommended_skill_count = len(
    result["skills"]
)

recommended_project_count = len(
    result["projects"]
)


# ---------------------------------------------------------
# STUDENT PROFILE SECTION
# ---------------------------------------------------------

st.markdown(
    '<div class="section-title">Student Profile</div>',
    unsafe_allow_html=True
)

profile_col1, profile_col2, profile_col3 = st.columns(3)

with profile_col1:
    st.markdown(
        '<div class="info-card">'
        '<div class="small-label">Student</div>'
        f'<div class="profile-value">'
        f'{student_profile["name"]} ({student_id})'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )

with profile_col2:
    st.markdown(
        '<div class="info-card">'
        '<div class="small-label">Level</div>'
        f'<div class="profile-value">'
        f'{student_profile["level"]}'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )

with profile_col3:
    st.markdown(
        '<div class="info-card">'
        '<div class="small-label">Interest Domain</div>'
        f'<div class="profile-value">'
        f'{student_profile["interests"]}'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )


# ---------------------------------------------------------
# CURRENT SKILLS
# ---------------------------------------------------------

st.markdown(
    '<div class="section-title">Current Skills</div>',
    unsafe_allow_html=True
)

if current_skills:
    st.write(
        " • ".join(current_skills)
    )
else:
    st.info("No current skills available.")


# ---------------------------------------------------------
# SUMMARY METRICS
# ---------------------------------------------------------

st.markdown(
    '<div class="section-title">Recommendation Summary</div>',
    unsafe_allow_html=True
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Student",
        student_profile["name"]
    )

with col2:
    st.metric(
        "Current Skills",
        len(current_skills)
    )

with col3:
    st.metric(
        "Skill Recommendations",
        recommended_skill_count
    )

with col4:
    st.metric(
        "Project Recommendations",
        recommended_project_count
    )


# ---------------------------------------------------------
# RECOMMENDED SKILLS
# ---------------------------------------------------------

st.markdown(
    '<div class="section-title">Recommended Skills</div>',
    unsafe_allow_html=True
)

if len(result["skills"]) == 0:

    st.info(
        "No new skill recommendations are available "
        "for this student profile."
    )

else:

    for index, skill in enumerate(
        result["skills"],
        start=1
    ):

        with st.container(border=True):

            st.subheader(
                f"{index}. {skill['skill']}"
            )

            match_percentage = (
                skill["score"] * 100
            )

            st.progress(
                skill["score"],
                text=(
                    f"Match Score: "
                    f"{match_percentage:.1f}%"
                )
            )

            if skill["missing_prerequisites"]:

                st.write(
                    "**Missing Prerequisites:** "
                    + ", ".join(
                        skill["missing_prerequisites"]
                    )
                )

            else:

                st.write(
                    "**Prerequisites:** "
                    "All prerequisites satisfied"
                )

            st.write(
                "**Why this skill is recommended:**"
            )

            st.write(
                skill["explanation"]
            )


# ---------------------------------------------------------
# RECOMMENDED PROJECTS
# ---------------------------------------------------------

st.markdown(
    '<div class="section-title">Recommended Projects</div>',
    unsafe_allow_html=True
)

if len(result["projects"]) == 0:

    st.info(
        "No suitable project recommendations "
        "are available for this student profile."
    )

else:

    for index, project in enumerate(
        result["projects"],
        start=1
    ):

        with st.container(border=True):

            st.subheader(
                f"{index}. {project['project']}"
            )

            match_percentage = (
                project["score"] * 100
            )

            st.progress(
                project["score"],
                text=(
                    f"Match Score: "
                    f"{match_percentage:.1f}%"
                )
            )

            st.write(
                f"**Domain:** {project['domain']}"
            )

            if project["known_skills"]:

                st.write(
                    "**Skills you already know:** "
                    + ", ".join(
                        project["known_skills"]
                    )
                )

            if project["missing_skills"]:

                st.write(
                    "**Skills to learn:** "
                    + ", ".join(
                        project["missing_skills"]
                    )
                )

            else:

                st.write(
                    "**Skills to learn:** "
                    "None — you already have all "
                    "required skills"
                )

            st.write(
                "**Why this project is recommended:**"
            )

            st.write(
                project["explanation"]
            )


# ---------------------------------------------------------
# KNOWLEDGE GRAPH VISUALIZATION
# ---------------------------------------------------------

st.markdown(
    '<div class="section-title">'
    'Knowledge Graph Visualization'
    '</div>',
    unsafe_allow_html=True
)

st.write(
    "The graph shows the selected student, their skills, "
    "related skills, prerequisites, recommended projects, "
    "and project-required skills."
)

if st.button(
    "Show Knowledge Graph",
    use_container_width=True
):

    output_file = create_knowledge_graph_visualization(
        student_id
    )

    html_path = Path(output_file)

    html_content = html_path.read_text(
        encoding="utf-8"
    )

    components.html(
        html_content,
        height=650,
        scrolling=True
    )