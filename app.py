import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path

from src.recommender.recommendation_engine import get_recommendations
from src.visualization import create_knowledge_graph_visualization


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="KG Skill & Project Recommender",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# PROFESSIONAL UI THEME
# ============================================================

st.markdown(
    """
    <style>

    /* ======================================================
       MAIN PAGE
       ====================================================== */

    .stApp {
        background-color: #f6f7fb;
    }

    .main .block-container {
        padding-top: 1.5rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }


    /* ======================================================
       MAIN TITLE
       ====================================================== */

    .main h1 {
        text-align: center !important;
        color: #29254a !important;

        font-size: 2.15rem !important;
        line-height: 1.25 !important;

        font-weight: 800 !important;

        letter-spacing: -0.4px;

        margin-top: 0.5rem !important;
        margin-bottom: 0.55rem !important;

        width: 100%;
    }

    /* Center subtitle */

    .main .stCaption {
        text-align: center !important;
        color: #77758a !important;

        font-size: 0.95rem !important;

        margin-bottom: 1.4rem !important;
    }


    /* ======================================================
       SIDEBAR
       ====================================================== */

    section[data-testid="stSidebar"] {
        background: linear-gradient(
            180deg,
            #312e81 0%,
            #4338ca 50%,
            #6d28d9 100%
        );
    }

    section[data-testid="stSidebar"] * {
        color: white;
    }

    section[data-testid="stSidebar"] .stSelectbox label {
        color: #eef2ff !important;
        font-weight: 600;
    }

    section[data-testid="stSidebar"] .stSelectbox > div > div {
        background-color: rgba(255, 255, 255, 0.12);
        border: 1px solid rgba(255, 255, 255, 0.28);
        border-radius: 10px;
    }

    section[data-testid="stSidebar"] hr {
        border-color: rgba(255, 255, 255, 0.20);
    }


    /* ======================================================
       SECTION HEADINGS
       ====================================================== */

    .section-header {
        font-size: 1.3rem;
        font-weight: 750;

        color: #29254a;

        margin-top: 1.6rem;
        margin-bottom: 0.8rem;

        padding-bottom: 0.5rem;

        border-bottom: 2px solid #e0e7ff;

        text-align: left;
    }


    /* ======================================================
       ALL CARDS
       ====================================================== */

    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 15px !important;

        border: 1px solid #e1e4ef !important;

        background-color: white !important;

        box-shadow:
            0 4px 15px rgba(31, 41, 55, 0.05);
    }


    /* ======================================================
       STUDENT PROFILE CARDS
       ====================================================== */

    div[data-testid="stVerticalBlockBorderWrapper"] {
        min-height: 120px;
    }


    /* ======================================================
       PROFILE CARD TEXT
       ====================================================== */

    div[data-testid="stVerticalBlockBorderWrapper"] .stCaption {
        color: #858494 !important;

        font-size: 0.78rem !important;

        font-weight: 600;
    }


    /* ======================================================
       METRIC CARDS
       ====================================================== */

    div[data-testid="stMetric"] {
        background-color: white;

        border: 1px solid #e1e4ef;

        border-radius: 14px;

        padding: 1rem;

        box-shadow:
            0 4px 15px rgba(31, 41, 55, 0.05);

        text-align: left;
    }

    div[data-testid="stMetricLabel"] {
        color: #6b7280 !important;
    }

    div[data-testid="stMetricValue"] {
        color: #312e81 !important;

        font-weight: 750;
    }


    /* ======================================================
       CURRENT SKILLS
       ====================================================== */

    div[data-testid="stAlert"] {
        border-radius: 12px;
    }


    /* ======================================================
       MATCH SCORE PROGRESS BAR
       ====================================================== */

    div[data-testid="stProgress"] {
        margin-top: 0.2rem;

        margin-bottom: 0.15rem;
    }

    div[data-testid="stProgress"] > div {
        background-color: #e5e7eb !important;

        border-radius: 999px !important;
    }

    div[data-testid="stProgress"] > div > div {
        background: linear-gradient(
            90deg,
            #6366f1,
            #a78bfa
        ) !important;

        border-radius: 999px !important;
    }


    /* ======================================================
       MATCH SCORE TEXT
       ====================================================== */

    .match-score {
        font-size: 0.86rem;

        font-weight: 700;

        color: #4f46e5;

        margin-top: 0.15rem;

        margin-bottom: 0.55rem;

        text-align: left;
    }


    /* ======================================================
       BUTTON
       ====================================================== */

    .stButton > button {
        width: 100%;

        min-height: 45px;

        border-radius: 10px;

        background: linear-gradient(
            135deg,
            #4f46e5,
            #7c3aed
        );

        color: white;

        border: none;

        font-weight: 700;
    }

    .stButton > button:hover {
        background: linear-gradient(
            135deg,
            #4338ca,
            #6d28d9
        );

        color: white;
    }


    /* ======================================================
       FOOTER
       ====================================================== */

    .footer-text {
        text-align: center;

        color: #8a8899;

        font-size: 0.82rem;

        margin-top: 2rem;

        padding-top: 1rem;

        border-top: 1px solid #e5e7eb;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# APPLICATION TITLE
# ============================================================

st.title(
    "🧠 Knowledge Graph-Based Personalized "
    "Skill & Project Recommendation System"
)

st.caption(
    "Personalized skill and project recommendations "
    "using Knowledge Graph reasoning."
)


# ============================================================
# LOAD STUDENT DATA
# ============================================================

students_df = pd.read_csv(
    "data/sample_students.csv"
)

students = dict(
    zip(
        students_df["student_id"],
        students_df["name"]
    )
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🧠 KG Recommender")

st.sidebar.caption(
    "Personalized Skill & Project Analysis"
)

st.sidebar.markdown("---")

st.sidebar.subheader("👤 Select Student")

selected_student = st.sidebar.selectbox(
    "Student",
    list(students.keys()),
    format_func=lambda student_id:
        f"{student_id} — {students[student_id]}"
)

student_id = selected_student


# ============================================================
# SELECTED STUDENT PROFILE
# ============================================================

student_profile = students_df[
    students_df["student_id"] == student_id
].iloc[0]


# ============================================================
# SIDEBAR PROFILE
# ============================================================

st.sidebar.markdown("---")

st.sidebar.markdown(
    "**Selected Student**"
)

st.sidebar.write(
    f"👤 **{student_profile['name']}**"
)

st.sidebar.write(
    f"🎓 **Level:** {student_profile['level']}"
)

st.sidebar.write(
    f"🎯 **Interest:** {student_profile['interests']}"
)


# ============================================================
# CURRENT SKILLS
# ============================================================

current_skills = [
    skill.strip()
    for skill in str(
        student_profile["skills"]
    ).split(";")
    if skill.strip()
]


# ============================================================
# GET RECOMMENDATIONS
# ============================================================

result = get_recommendations(
    student_id,
    top_n=5
)

skill_count = len(
    result["skills"]
)

project_count = len(
    result["projects"]
)


# ============================================================
# STUDENT PROFILE
# ============================================================

st.markdown(
    '<div class="section-header">'
    '👤 Student Profile'
    '</div>',
    unsafe_allow_html=True
)

profile_col1, profile_col2, profile_col3 = st.columns(
    3,
    gap="medium"
)


# ------------------------------------------------------------
# STUDENT
# ------------------------------------------------------------

with profile_col1:

    with st.container(border=True):

        st.caption("STUDENT")

        st.subheader(
            student_profile["name"]
        )

        st.write(
            student_id
        )


# ------------------------------------------------------------
# ACADEMIC LEVEL
# ------------------------------------------------------------

with profile_col2:

    with st.container(border=True):

        st.caption("ACADEMIC LEVEL")

        st.subheader(
            student_profile["level"]
        )

        # Keeps visual height aligned
        st.write(" ")


# ------------------------------------------------------------
# INTEREST DOMAIN
# ------------------------------------------------------------

with profile_col3:

    with st.container(border=True):

        st.caption("INTEREST DOMAIN")

        st.subheader(
            student_profile["interests"]
        )

        # Keeps visual height aligned
        st.write(" ")


# ============================================================
# CURRENT SKILLS
# ============================================================

st.markdown(
    '<div class="section-header">'
    '🛠️ Current Skills'
    '</div>',
    unsafe_allow_html=True
)

if current_skills:

    st.info(
        "  •  ".join(
            current_skills
        )
    )

else:

    st.warning(
        "No current skills available."
    )


# ============================================================
# RECOMMENDATION SUMMARY
# ============================================================

st.markdown(
    '<div class="section-header">'
    '📊 Recommendation Summary'
    '</div>',
    unsafe_allow_html=True
)

summary_col1, summary_col2, summary_col3, summary_col4 = (
    st.columns(
        4,
        gap="medium"
    )
)


with summary_col1:

    st.metric(
        "Student",
        student_profile["name"]
    )


with summary_col2:

    st.metric(
        "Current Skills",
        len(current_skills)
    )


with summary_col3:

    st.metric(
        "Skill Recommendations",
        skill_count
    )


with summary_col4:

    st.metric(
        "Project Recommendations",
        project_count
    )


# ============================================================
# RECOMMENDED SKILLS
# ============================================================

st.markdown(
    '<div class="section-header">'
    '💡 Recommended Skills'
    '</div>',
    unsafe_allow_html=True
)


if not result["skills"]:

    st.info(
        "No new skill recommendations are available "
        "for this student."
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

            score = skill["score"]

            st.progress(
                score
            )

            st.markdown(
                f"""
                <div class="match-score">
                    Match Score: {score * 100:.1f}%
                </div>
                """,
                unsafe_allow_html=True
            )


            # ------------------------------------------------
            # PREREQUISITES
            # ------------------------------------------------

            if skill["missing_prerequisites"]:

                st.warning(
                    "⚠️ Missing prerequisites: "
                    + ", ".join(
                        skill[
                            "missing_prerequisites"
                        ]
                    )
                )

            else:

                st.success(
                    "✅ All prerequisites satisfied"
                )


            # ------------------------------------------------
            # EXPLANATION
            # ------------------------------------------------

            st.write(
                "**Why this skill is recommended:**"
            )

            st.info(
                skill["explanation"]
            )


# ============================================================
# RECOMMENDED PROJECTS
# ============================================================

st.markdown(
    '<div class="section-header">'
    '🚀 Recommended Projects'
    '</div>',
    unsafe_allow_html=True
)


if not result["projects"]:

    st.info(
        "No suitable project recommendations "
        "are available."
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

            score = project["score"]

            st.progress(
                score
            )

            st.markdown(
                f"""
                <div class="match-score">
                    Match Score: {score * 100:.1f}%
                </div>
                """,
                unsafe_allow_html=True
            )


            # ------------------------------------------------
            # DOMAIN
            # ------------------------------------------------

            st.write(
                f"**Domain:** {project['domain']}"
            )


            # ------------------------------------------------
            # KNOWN SKILLS
            # ------------------------------------------------

            if project["known_skills"]:

                st.write(
                    "**Skills you already know:** "
                    + ", ".join(
                        project["known_skills"]
                    )
                )


            # ------------------------------------------------
            # MISSING SKILLS
            # ------------------------------------------------

            if project["missing_skills"]:

                st.warning(
                    "📚 Skills to learn: "
                    + ", ".join(
                        project["missing_skills"]
                    )
                )

            else:

                st.success(
                    "✅ You already have all "
                    "required skills."
                )


            # ------------------------------------------------
            # EXPLANATION
            # ------------------------------------------------

            st.write(
                "**Why this project is recommended:**"
            )

            st.info(
                project["explanation"]
            )


# ============================================================
# KNOWLEDGE GRAPH
# ============================================================

st.markdown(
    '<div class="section-header">'
    '🕸️ Knowledge Graph Visualization'
    '</div>',
    unsafe_allow_html=True
)

st.write(
    "Explore the selected student's skills, related skills, "
    "prerequisites, recommended projects and project "
    "requirements."
)


# ============================================================
# SHOW KNOWLEDGE GRAPH
# ============================================================

if st.button(
    "🕸️ Show Knowledge Graph"
):

    output_file = (
        create_knowledge_graph_visualization(
            student_id
        )
    )

    html_path = Path(
        output_file
    )

    html_content = html_path.read_text(
        encoding="utf-8"
    )

    components.html(
        html_content,
        height=700,
        scrolling=True
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    '<div class="footer-text">'
    'Knowledge Graph-Based Personalized Skill & Project '
    'Recommendation System'
    '<br>'
    'Python • NetworkX • Streamlit • PyVis'
    '</div>',
    unsafe_allow_html=True
)