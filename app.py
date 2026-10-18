
import html
from pathlib import Path

import networkx as nx
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from pyvis.network import Network
<<<<<<< HEAD
from src.integrations.internship_api import fetch_internships
=======
>>>>>>> bf716a946ab822024f0ae8183626d872d5362002

from database.database import get_connection, initialize_database
from src.admin.data_ingestion import (
    get_dataset_status,
    get_dataset_types,
    import_dataset,
)
from src.auth.authentication import login_user, register_user
from src.knowledge_graph import build_knowledge_graph
from src.recommender.recommendation_engine import get_recommendations


# ============================================================
# APP SETUP
# ============================================================

initialize_database()

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

APP_TITLE = "Knowledge Graph-Based Student Skill & Project Recommendation System"
APP_SUBTITLE = "Personalized recommendations using skills, domains, prerequisites and project relationships"

st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# DATA
# ============================================================

def load_master_data():
    skills_path = DATA_DIR / "skills.csv"
    domains_path = DATA_DIR / "domains.csv"

    skills_df = pd.read_csv(skills_path) if skills_path.exists() else pd.DataFrame()
    domains_df = pd.read_csv(domains_path) if domains_path.exists() else pd.DataFrame()

    available_skills = []
    available_domains = []

    if "name" in skills_df.columns:
        available_skills = sorted(
            skills_df["name"].dropna().astype(str).unique().tolist()
        )

    if "name" in domains_df.columns:
        available_domains = sorted(
            domains_df["name"].dropna().astype(str).unique().tolist()
        )

    return skills_df, domains_df, available_skills, available_domains


skills_df, domains_df, AVAILABLE_SKILLS, AVAILABLE_DOMAINS = load_master_data()


# ============================================================
# PROFESSIONAL CSS
# ============================================================

st.markdown(
    """
    <style>
    .stApp {
        background: #f6f7fb;
    }

    [data-testid="stSidebar"] {
        display: none !important;
    }

    [data-testid="stSidebar"] * {
        display: none !important;
    }

    .block-container {
        max-width: 1350px;
        padding-top: 1.2rem;
        padding-bottom: 1rem;
    }

    .brand {
        font-size: 1.25rem;
        font-weight: 800;
        letter-spacing: -0.3px;
    }

    .muted {
        color: #94a3b8;
        font-size: 0.78rem;
    }

    .hero {
        background: linear-gradient(135deg, #312e81, #4f46e5);
        color: white;
        padding: 1.4rem 1.6rem;
        border-radius: 16px;
        margin-bottom: 1rem;
    }

    .hero h1 {
        margin: 0;
        font-size: 2rem;
        line-height: 1.15;
        color: white;
    }

    .hero p {
        margin: 0.45rem 0 0 0;
        color: #e0e7ff;
        font-size: 0.9rem;
    }

    .section {
        font-size: 1rem;
        font-weight: 800;
        color: #20243a;
        margin: 0.9rem 0 0.55rem 0;
        padding-bottom: 0.35rem;
        border-bottom: 1px solid #dfe3ee;
    }

    .card {
        background: white;
        border: 1px solid #e1e5ef;
        border-radius: 14px;
        padding: 0.9rem 1rem;
        min-height: 100px;
        box-shadow: 0 2px 10px rgba(15, 23, 42, 0.04);
    }

    .card-label {
        color: #64748b;
        font-size: 0.68rem;
        font-weight: 800;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }

    .card-value {
        color: #312e81;
        font-size: 1.25rem;
        font-weight: 800;
        margin-top: 0.25rem;
    }

    .card-text {
        color: #475569;
        font-size: 0.82rem;
        margin-top: 0.3rem;
        line-height: 1.4;
    }

    .login-wrap {
        max-width: 850px;
        margin: 3rem auto 0 auto;
    }

    .login-title {
        text-align: center;
        color: #20243a;
        font-size: 2rem;
        font-weight: 850;
        margin-bottom: 0.2rem;
    }

    .login-subtitle {
        text-align: center;
        color: #64748b;
        font-size: 0.88rem;
        margin-bottom: 1.3rem;
    }

    .top-nav {
        background: #ffffff;
        border: 1px solid #e1e5ef;
        border-radius: 14px;
        padding: 0.55rem 0.75rem;
        margin-bottom: 0.9rem;
        box-shadow: 0 2px 10px rgba(15, 23, 42, 0.04);
    }

    .top-brand {
        font-size: 0.98rem;
        font-weight: 800;
        color: #20243a;
    }

    .footer {
        text-align: center;
        color: #a8b1c2;
        font-size: 0.66rem;
        margin-top: 0.8rem;
        padding-top: 0.45rem;
        border-top: 1px solid #e8ebf2;
    }

    div[data-testid="stMetric"] {
        background: white;
        border: 1px solid #e1e5ef;
        border-radius: 13px;
        padding: 0.75rem;
    }

    div[data-testid="stMetricValue"] {
        color: #312e81 !important;
        font-weight: 800;
    }

    .stButton > button {
        border-radius: 9px;
        font-weight: 700;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SESSION
# ============================================================

st.session_state.setdefault("authenticated", False)
st.session_state.setdefault("user", None)
st.session_state.setdefault("page", "Dashboard")
st.session_state.setdefault("graph_built", False)
st.session_state.setdefault("graph_html", "")
st.session_state.setdefault("graph_student_id", "")


# ============================================================
# AUTH
# ============================================================

def show_authentication_page():
    st.markdown('<div class="login-wrap">', unsafe_allow_html=True)
    st.markdown(
        f'<div class="login-title">🧠 {html.escape(APP_TITLE)}</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div class="login-subtitle">{html.escape(APP_SUBTITLE)}</div>',
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    login_tab, register_tab = st.tabs(["🔐 Login", "📝 Create Account"])

    with login_tab:
        st.subheader("Welcome Back")

        email = st.text_input("Email", key="login_email")
        password = st.text_input(
            "Password",
            type="password",
            key="login_password",
        )

        if st.button("🔐 Login", use_container_width=True, key="login_button"):
            if not email.strip() or not password:
                st.error("Please enter both email and password.")
            else:
                user = login_user(email, password)

                if user:
                    st.session_state.authenticated = True
                    st.session_state.user = user
                    st.session_state.page = "Dashboard"
                    st.rerun()
                else:
                    st.error("Invalid email or password.")

    with register_tab:
        st.subheader("Create Student Account")

        name = st.text_input("Full Name", key="register_name")
        email = st.text_input("Email", key="register_email")
        password = st.text_input(
            "Password",
            type="password",
            key="register_password",
        )
        confirm_password = st.text_input(
            "Confirm Password",
            type="password",
            key="register_confirm_password",
        )

        student_id = st.text_input("Student ID", key="register_student_id")
        college = st.text_input("College", key="register_college")
        branch = st.text_input(
            "Branch",
            value="CSE",
            key="register_branch",
        )
        graduation_year = st.number_input(
            "Graduation Year",
            min_value=2024,
            max_value=2040,
            value=2027,
            step=1,
            key="register_graduation_year",
        )

        target_domain = st.selectbox(
            "Target / Interested Domain",
            ["Select a domain"] + AVAILABLE_DOMAINS,
            key="register_target_domain",
        )

        selected_skills = st.multiselect(
            "Current Skills",
            AVAILABLE_SKILLS,
            key="register_skills",
        )

        proficiencies = {}
        if selected_skills:
            st.caption("Set a proficiency level from 1 (basic) to 5 (strong).")

        for skill_name in selected_skills:
            proficiencies[skill_name] = st.slider(
                skill_name,
                1,
                5,
                2,
                key=f"proficiency_{skill_name}",
            )

        additional_interests = st.multiselect(
            "Additional Interests",
            AVAILABLE_DOMAINS,
            key="register_interests",
        )

        if st.button(
            "📝 Create Account",
            use_container_width=True,
            key="register_button",
        ):
            if not name.strip():
                st.error("Please enter your name.")
            elif not email.strip():
                st.error("Please enter your email.")
            elif not password:
                st.error("Please enter a password.")
            elif password != confirm_password:
                st.error("Passwords do not match.")
            elif not student_id.strip():
                st.error("Please enter your student ID.")
            elif target_domain == "Select a domain":
                st.error("Please select your target domain.")
            else:
                success, message = register_user(email, password)

                if not success:
                    st.error(message)
                else:
                    user = login_user(email, password)

                    if user is None:
                        st.error("Account created, but login failed.")
                    else:
                        connection = get_connection()
                        cursor = connection.cursor()

                        try:
                            cursor.execute(
                                """
                                INSERT INTO student_profiles
                                (user_id, student_id, name, college,
                                 branch, graduation_year, target_domain)
                                VALUES (?, ?, ?, ?, ?, ?, ?)
                                """,
                                (
                                    user["id"],
                                    student_id.strip(),
                                    name.strip(),
                                    college.strip(),
                                    branch.strip(),
                                    graduation_year,
                                    target_domain,
                                ),
                            )

                            for skill_name, proficiency in proficiencies.items():
                                cursor.execute(
                                    """
                                    INSERT INTO student_skills
                                    (user_id, skill_name, proficiency)
                                    VALUES (?, ?, ?)
                                    """,
                                    (
                                        user["id"],
                                        skill_name,
                                        proficiency,
                                    ),
                                )

                            cursor.execute(
                                """
                                INSERT INTO student_interests
                                (user_id, domain_name)
                                VALUES (?, ?)
                                """,
                                (user["id"], target_domain),
                            )

                            for domain_name in additional_interests:
                                if domain_name == target_domain:
                                    continue

                                cursor.execute(
                                    """
                                    INSERT INTO student_interests
                                    (user_id, domain_name)
                                    VALUES (?, ?)
                                    """,
                                    (user["id"], domain_name),
                                )

                            connection.commit()
                            st.success(
                                "Account created successfully. Please use the Login tab."
                            )

                        except Exception as error:
                            connection.rollback()
                            st.error(f"Profile creation failed: {error}")

                        finally:
                            connection.close()


# ============================================================
# STUDENT DATA
# ============================================================

def load_student_data(user_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, user_id, student_id, name, college, branch,
               graduation_year, target_domain
        FROM student_profiles
        WHERE user_id = ?
        """,
        (user_id,),
    )
    profile = cursor.fetchone()

    cursor.execute(
        """
        SELECT skill_name, proficiency
        FROM student_skills
        WHERE user_id = ?
        ORDER BY skill_name
        """,
        (user_id,),
    )
    skills = cursor.fetchall()

    cursor.execute(
        """
        SELECT domain_name
        FROM student_interests
        WHERE user_id = ?
        ORDER BY domain_name
        """,
        (user_id,),
    )
    interests = cursor.fetchall()

    connection.close()
    return profile, skills, interests


def logout():
    st.session_state.authenticated = False
    st.session_state.user = None
    st.session_state.page = "Dashboard"
    st.rerun()


# ============================================================
# SIDEBAR
# ============================================================

def show_top_navigation(profile):
    """Single clean navigation row shown directly below the hero."""
    page_options = [
        "Dashboard",
        "My Profile",
        "Skill Recommendations",
        "Project Recommendations",

        "Live Internships",

        "Knowledge Graph",
    ]

    nav_left, nav_right = st.columns([7.8, 1.2], gap="small")

    with nav_left:
        selected = st.segmented_control(
            "Application navigation",
            page_options,
            default=st.session_state.page,
            key="top_navigation",
            label_visibility="collapsed",
        )

    with nav_right:
        if st.button("Logout", use_container_width=True, key="top_logout"):
            logout()

    if selected and selected != st.session_state.page:
        st.session_state.page = selected
        st.rerun()


def show_admin_top_navigation():
    st.markdown(
        f"""
        <div class="top-nav">
            <div style="display:flex;align-items:center;justify-content:space-between;gap:1rem;flex-wrap:wrap;">
                <div>
                    <div class="top-brand">👑 Student Skill Graph · Admin</div>
                    <div class="muted">{html.escape(st.session_state.user['email'])}</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("Logout", use_container_width=False, key="admin_top_logout"):
        logout()


# ============================================================
# HEADERS / CARDS
# ============================================================

def page_header(title, subtitle, profile=None):
    # Every student page gets the same navigation row so the user can move
    # between Dashboard, Profile, Recommendations and Knowledge Graph
    # without restarting the application.
    if profile is None:
        profile = st.session_state.get("current_profile")

    st.markdown(
        f"""
        <div class="hero">
            <h1>{html.escape(title)}</h1>
            <p>{html.escape(subtitle)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if profile is not None:
        show_top_navigation(profile)


def card(title, value, text=""):
    safe_title = html.escape(str(title))
    safe_value = html.escape(str(value))
    safe_text = html.escape(str(text))

    st.markdown(
        f"""
        <div class="card">
            <div class="card-label">{safe_title}</div>
            <div class="card-value">{safe_value}</div>
            <div class="card-text">{safe_text}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# DASHBOARD
# ============================================================

def show_dashboard(profile, student_skills, student_interests, recommendations):
    page_header(
        APP_TITLE,
        APP_SUBTITLE,
        profile,
    )

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Current Skills", len(student_skills))
    with c2:
        st.metric("Interest Areas", len(student_interests))
    with c3:
        st.metric("Skill Recommendations", len(recommendations["skills"]))
    with c4:
        st.metric("Project Recommendations", len(recommendations["projects"]))

    st.markdown('<div class="section">🎯 Learning Profile</div>', unsafe_allow_html=True)

    p1, p2 = st.columns(2)
    with p1:
        card(
            "Target Domain",
            profile["target_domain"],
            "Recommendations are personalized around this domain.",
        )
    with p2:
        skills_text = (
            " • ".join(row["skill_name"] for row in student_skills)
            if student_skills
            else "No skills added"
        )
        card("Current Skills", len(student_skills), skills_text)

    st.markdown('<div class="section">💡 Explore</div>', unsafe_allow_html=True)

    e1, e2, e3 = st.columns(3)
    with e1:
        card("Skills", "Explore", "Discover skills connected to your existing knowledge.")
    with e2:
        card("Projects", "Explore", "Find projects matched to your skills and goals.")
    with e3:
        card("Knowledge Graph", "Explore", "See how your student, skills, domains and projects are connected.")

    st.markdown('<div class="section">⚡ Quick Actions</div>', unsafe_allow_html=True)

    q1, q2, q3 = st.columns(3)

    with q1:
        if st.button("💡 View Skill Recommendations", use_container_width=True):
            st.session_state.page = "Skill Recommendations"
            st.rerun()

    with q2:
        if st.button("🚀 View Project Recommendations", use_container_width=True):
            st.session_state.page = "Project Recommendations"
            st.rerun()

    with q3:
        if st.button("🕸️ Open Knowledge Graph", use_container_width=True):
            st.session_state.page = "Knowledge Graph"
            st.rerun()


# ============================================================
# PROFILE
# ============================================================

def show_profile_page(profile, student_skills, student_interests):
    page_header(
        "My Profile",
        "Your academic identity, skills and interests.",
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        card("Student", profile["name"], f"ID: {profile['student_id']}")

    with c2:
        card(
            "Academic",
            profile["branch"],
            f"{profile['college']} • Graduation {profile['graduation_year']}",
        )

    with c3:
        card(
            "Target Domain",
            profile["target_domain"],
            f"{len(student_interests)} interest area(s)",
        )

    st.markdown('<div class="section">🛠️ Skills & Proficiency</div>', unsafe_allow_html=True)

    if student_skills:
        rows = [
            {
                "Skill": row["skill_name"],
                "Proficiency": row["proficiency"],
            }
            for row in student_skills
        ]
        st.dataframe(
            pd.DataFrame(rows),
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("No skills have been added yet.")

    st.markdown('<div class="section">🎯 Interests</div>', unsafe_allow_html=True)

    if student_interests:
        st.info(
            " • ".join(row["domain_name"] for row in student_interests)
        )
    else:
        st.info("No interests have been added yet.")


# ============================================================
# RECOMMENDATIONS
# ============================================================

def show_skill_recommendations(recommendations):
    page_header(
        "Skill Recommendations",
        "Skills ranked using your current knowledge, interests and graph relationships.",
    )

    skills = recommendations["skills"]

    if not skills:
        st.info("No new skill recommendations are available.")
        return

    for index, skill in enumerate(skills, 1):
        score = min(max(float(skill["score"]), 0.0), 1.0)

        with st.container(border=True):
            st.markdown(f"### {index}. {skill['skill']}")
            st.caption(f"Match score: {score * 100:.1f}%")
            st.progress(score)

            if skill["missing_prerequisites"]:
                st.warning(
                    "Missing prerequisites: "
                    + ", ".join(skill["missing_prerequisites"])
                )
            else:
                st.success("All prerequisites satisfied.")

            st.write(skill["explanation"])


def show_project_recommendations(recommendations):
    page_header(
        "Project Recommendations",
        "Projects matched against your current skills and learning requirements.",
        st.session_state.get("current_profile"),
    )

    projects = recommendations["projects"]

    if not projects:
        st.info("No suitable project recommendations are available.")
        return

    for index, project in enumerate(projects, 1):
        score = min(max(float(project["score"]), 0.0), 1.0)

        with st.container(border=True):
            st.markdown(f"### {index}. {project['project']}")
            st.caption(
                f"Domain: {project['domain']} • Match score: {score * 100:.1f}%"
            )
            st.progress(score)

            if project["known_skills"]:
                st.write("✅ Known:", ", ".join(project["known_skills"]))

            if project["missing_skills"]:
                st.warning(
                    "📚 Skills to learn: "
                    + ", ".join(project["missing_skills"])
                )
            else:
                st.success("You already have all required skills.")

            st.write(project["explanation"])


# ============================================================
# KNOWLEDGE GRAPH
# ============================================================

def create_student_graph_html(student_id, recommendations):
    graph = build_knowledge_graph()
    student_node = f"student:{student_id}"

    if student_node not in graph.nodes:
        raise ValueError(
            f"Student node '{student_node}' not found in the graph."
        )

    selected_nodes = {student_node}
    direct_neighbors = set(graph.successors(student_node))
    selected_nodes.update(direct_neighbors)

    current_skill_nodes = {
        node
        for node in direct_neighbors
        if graph.nodes[node].get("label") == "Skill"
    }

    for skill_node in current_skill_nodes:
        for neighbor in graph.successors(skill_node):
            if graph.nodes[neighbor].get("label") == "Skill":
                selected_nodes.add(neighbor)

    recommended_skill_names = {
        item["skill"] for item in recommendations["skills"]
    }

    recommended_project_names = {
        item["project"] for item in recommendations["projects"]
    }

    project_nodes = set()

    for node, data in graph.nodes(data=True):
        label = data.get("label")
        name = data.get("name")

        if label == "Skill" and name in recommended_skill_names:
            selected_nodes.add(node)

        if label == "Project" and name in recommended_project_names:
            project_nodes.add(node)
            selected_nodes.add(node)

    for project_node in project_nodes:
        for neighbor in graph.successors(project_node):
            if graph.nodes[neighbor].get("label") == "Skill":
                selected_nodes.add(neighbor)

    display_graph = nx.MultiDiGraph()

    for node in selected_nodes:
        if node in graph.nodes:
            display_graph.add_node(node, **graph.nodes[node])

    for source, target, key, data in graph.edges(
        selected_nodes,
        keys=True,
        data=True,
    ):
        if source in selected_nodes and target in selected_nodes:
            display_graph.add_edge(
                source,
                target,
                key=key,
                **data,
            )

    if display_graph.number_of_nodes() > 80:
        keep_nodes = list(display_graph.nodes())[:80]
        display_graph = display_graph.subgraph(keep_nodes).copy()

    network = Network(
        height="560px",
        width="100%",
        directed=True,
        bgcolor="#ffffff",
        font_color="#20243a",
        cdn_resources="in_line",
    )

    network.set_options(
        """
        {
          "nodes": {
            "shape": "dot",
            "size": 20,
            "font": {
              "size": 14,
              "face": "Arial"
            },
            "borderWidth": 1
          },
          "edges": {
            "arrows": {
              "to": {
                "enabled": true,
                "scaleFactor": 0.55
              }
            },
            "font": {
              "size": 9,
              "align": "middle"
            },
            "smooth": {
              "enabled": true,
              "type": "dynamic"
            }
          },
          "physics": {
            "enabled": true,
            "stabilization": {
              "iterations": 180
            },
            "barnesHut": {
              "gravitationalConstant": -2600,
              "centralGravity": 0.18,
              "springLength": 145,
              "springConstant": 0.04,
              "damping": 0.16
            }
          },
          "interaction": {
            "hover": true,
            "navigationButtons": true,
            "keyboard": true
          }
        }
        """
    )

    node_colors = {
        "Student": "#7c3aed",
        "Skill": "#2563eb",
        "Project": "#16a34a",
        "Domain": "#ea580c",
        "Course": "#0891b2",
        "Internship": "#db2777",
        "Platform": "#64748b",
    }

    for node, data in display_graph.nodes(data=True):
        label = data.get("label", "Node")
        name = data.get("name", str(node))

        network.add_node(
            node,
            label=str(name),
            title=f"{label}: {name}",
            color=node_colors.get(label, "#94a3b8"),
            size=30 if label == "Student" else 21,
        )

    for source, target, key, data in display_graph.edges(
        keys=True,
        data=True,
    ):
        relation = data.get("relation", str(key))
        network.add_edge(
            source,
            target,
            label=relation,
            title=relation,
        )

    # Generate HTML in memory first, then write it explicitly as UTF-8.
    # PyVis' write_html() can use the Windows default charmap encoding,
    # which fails when graph labels contain Unicode characters.
    html_content = network.generate_html()

    html_path = DATA_DIR / "student_knowledge_graph.html"
    html_path.write_text(html_content, encoding="utf-8")

    return html_path


def show_knowledge_graph(student_id, recommendations):
    page_header(
        "Knowledge Graph",
        "Explore the relationships that support your skill and project recommendations.",
    )

    st.markdown(
        """
        <div class="card" style="min-height:0;margin-bottom:.8rem;">
            <div class="card-label">Graph view</div>
            <div style="font-size:.9rem;color:#475569;line-height:1.5;margin-top:.3rem;">
                Your student profile is connected to your skills and interest domains.
                Related skills, prerequisites and project requirements are shown around those nodes.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    refresh = st.button(
        "Refresh Knowledge Graph",
        type="primary",
        key="refresh_student_graph",
        use_container_width=True,
    )

    should_build = (
        refresh
        or not st.session_state.get("graph_built", False)
        or st.session_state.get("graph_student_id") != student_id
    )

    if should_build:
        try:
            with st.spinner("Preparing your knowledge graph..."):
                html_path = create_student_graph_html(
                    student_id,
                    recommendations,
                )
                html_content = html_path.read_text(encoding="utf-8")

            st.session_state["graph_html"] = html_content
            st.session_state["graph_built"] = True
            st.session_state["graph_student_id"] = student_id

        except Exception as error:
            st.session_state["graph_built"] = False
            st.session_state["graph_html"] = ""
            st.error(f"Knowledge Graph generation failed: {error}")

    if st.session_state.get("graph_built") and st.session_state.get("graph_html"):
        components.html(
            st.session_state["graph_html"],
            height=650,
            scrolling=False,
        )

        st.markdown(
            """
            <div style="display:flex;gap:.45rem;flex-wrap:wrap;margin-top:.45rem;">
                <span class="tag">Student</span>
                <span class="tag">Skill</span>
                <span class="tag">Domain</span>
                <span class="tag">Project</span>
                <span style="color:#94a3b8;font-size:.74rem;padding:.25rem .1rem;">
                    Drag nodes · zoom · hover for relationship labels
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ============================================================
# ADMIN
# ============================================================

def show_data_ingestion():
    st.markdown(
        '<div class="section">📥 Dataset Management</div>',
        unsafe_allow_html=True,
    )

    st.caption(
        "Import validated CSV/Excel files into the project's data layer."
    )

    selected_dataset = st.selectbox(
        "Dataset",
        get_dataset_types(),
        key="admin_dataset_type",
    )

    uploaded_file = st.file_uploader(
        "Upload CSV or Excel",
        type=["csv", "xlsx", "xls"],
        key="admin_dataset_upload",
    )

    if uploaded_file is not None:
        try:
            uploaded_file.seek(0)
            preview_df = (
                pd.read_csv(uploaded_file)
                if uploaded_file.name.lower().endswith(".csv")
                else pd.read_excel(uploaded_file)
            )

            st.dataframe(
                preview_df.head(8),
                use_container_width=True,
                hide_index=True,
            )

            if st.button(
                "✅ Validate & Import",
                type="primary",
                key="admin_import_dataset",
            ):
                uploaded_file.seek(0)
                result = import_dataset(
                    uploaded_file,
                    selected_dataset,
                )

                if result["success"]:
                    st.success(result["message"])
                    st.info(f"Imported rows: {result['rows']}")
                    if result.get("warnings"):
                        for warning in result["warnings"]:
                            st.warning(warning)
                else:
                    st.error(result["message"])
                    for warning in result.get("warnings", []):
                        st.warning(warning)

        except Exception as error:
            st.error(f"Could not read file: {error}")

    st.markdown("#### Current Dataset Status")

    status_rows = [
        {
            "Dataset": item["dataset"],
            "Rows": item["rows"],
            "Available": "Yes" if item["exists"] else "No",
        }
        for item in get_dataset_status()
    ]

    st.dataframe(
        pd.DataFrame(status_rows),
        use_container_width=True,
        hide_index=True,
    )


def show_admin_dashboard():
    show_admin_top_navigation()

    page_header(
        "Admin Dashboard",
        "Manage datasets and maintain the knowledge graph used by the application.",
    )

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) AS count FROM users")
    total_users = cursor.fetchone()["count"]

    cursor.execute("SELECT COUNT(*) AS count FROM student_profiles")
    total_students = cursor.fetchone()["count"]

    connection.close()

    def csv_count(filename):
        path = DATA_DIR / filename
        if not path.exists():
            return 0
        try:
            return len(pd.read_csv(path))
        except Exception:
            return 0

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Users", total_users)
    c2.metric("Students", total_students)
    c3.metric("Skills", csv_count("skills.csv"))
    c4.metric("Projects", csv_count("projects.csv"))

    show_data_ingestion()

    st.markdown('<div class="section">🕸️ Knowledge Graph Management</div>', unsafe_allow_html=True)

    if st.button(
        "🔄 Rebuild & Test Knowledge Graph",
        type="primary",
        key="admin_rebuild_graph",
    ):
        try:
            graph = build_knowledge_graph()

            st.success("Knowledge Graph rebuilt successfully.")

            c1, c2 = st.columns(2)
            c1.metric("Graph Nodes", graph.number_of_nodes())
            c2.metric("Graph Relationships", graph.number_of_edges())

        except Exception as error:
            st.error(f"Knowledge Graph rebuild failed: {error}")



def show_live_internships(student_skills, student_interests):
    page_header(
        "Live Internships",
        "Explore real internship listings from OpenIntern.",
        st.session_state.get("current_profile"),
    )

    st.caption(
        "Listings are fetched from an external service. "
        "Check each employer's application page for the latest details."
    )

    india_only = st.checkbox(
        "Show only listings whose location mentions India",
        value=False,
    )

    if st.button("🔄 Refresh Live Listings", type="primary"):
        st.cache_data.clear()

    with st.spinner("Fetching internship listings..."):
        result = fetch_internships(
            limit=27,
            india_only=india_only,
        )

    if not result["success"]:
        st.error(result["message"])
        st.info(
            "Please check your internet connection and try refreshing."
        )
        return

    internships = result["internships"]

    # Personalize internships using student skills and interests.

    student_skills_list = [
        str(row["skill_name"]).strip().lower()
        for row in student_skills
        if row["skill_name"]
    ]

    student_interests_list = [
        str(row["domain_name"]).strip().lower()
        for row in student_interests
        if row["domain_name"]
    ]

    target_domain = (
        st.session_state["current_profile"].get("target_domain") or ""
    ).strip().lower()

    # Connect related skills and domains to common internship titles.
    related_terms = {
    "web development": [
        "web developer",
        "frontend",
        "front-end",
        "backend",
        "back-end",
        "full stack",
        "software engineer",
        "software developer",
        "software development engineer",
    ],
    "javascript": [
        "frontend",
        "front-end",
        "web developer",
        "software developer",
    ],
    "html": [
        "frontend",
        "front-end",
        "web developer",
    ],
    "css": [
        "frontend",
        "front-end",
        "web developer",
    ],
    "java": [
        "software engineer",
        "software developer",
        "software development engineer",
    ],
    "python": [
        "data science",
        "machine learning",
        "ai developer",
        "data analyst",
    ],
    "artificial intelligence": [
        "ai developer",
        "machine learning",
        "data science",
    ],
    "ai": [
        "ai developer",
        "machine learning",
    ],
    "data science": [
        "data analyst",
        "data scientist",
        "machine learning",
    ],
    "cloud computing": [
        "cloud engineer",
        "devops",
    ],
    "cloud": [
        "cloud engineer",
        "devops",
        "software engineer",
    ],
    "devops": [
        "cloud engineer",
        "software engineer",
    ],
    "cybersecurity": [
        "security engineer",
        "security analyst",
    ],
    "software engineering": [
        "software engineer",
        "software developer",
        "software development engineer",
    ],
}

    def internship_score(internship):
        title = internship.get("title", "").lower()
        company = internship.get("company", "").lower()
        text = f"{title} {company}"

        score = 0
        matched_terms = []

        # Direct skill matches receive the highest weight.
        for skill in student_skills_list:
            if skill and skill in text:
                score += 3
                matched_terms.append(skill)

        # Interest and target-domain matches receive a lower weight.
        domains = student_interests_list + ([target_domain] if target_domain else [])

        for domain in domains:
            if domain and domain in text:
                score += 2
                matched_terms.append(domain)

        # Related terms provide additional relevance.
        for keyword in student_skills_list + domains:
            for related in related_terms.get(keyword, []):
                if related in title:
                    score += 1
                    matched_terms.append(related)

        return score, sorted(set(matched_terms))

    # Rank the best-matching internships first.
    ranked_internships = []

    for internship in internships:
        score, matched_terms = internship_score(internship)
        ranked_internships.append({
            **internship,
            "relevance_score": score,
            "matched_terms": matched_terms,
        })

    internships = sorted(
        ranked_internships,
        key=lambda item: item["relevance_score"],
        reverse=True,
    )

    if not internships:
        st.info(
            "No matching internships were returned. "
            "Try unchecking the India-only filter."
        )
        return

    st.success(f"Found {len(internships)} matching listings.")

    for internship in internships:
        with st.container(border=True):
            st.subheader(internship["title"])
            st.write(f"**Company:** {internship['company']}")
            st.write(f"**Location:** {internship['location']}")
            if internship["matched_terms"]:
                st.caption(
                    "Why recommended: "
                    + ", ".join(internship["matched_terms"])
                )
            else:
                st.caption("No direct skill or interest match identified.")
            posted_at = internship.get("posted_at")
            if posted_at:
                st.caption(f"Listed date: {posted_at}")

            apply_url = internship.get("url")
            if apply_url and apply_url.startswith("https://"):
                st.link_button(
                    "Apply on employer website ↗",
                    apply_url,
                )
            else:
                st.caption("No application link was provided.")


# ============================================================
# ROUTING
# ============================================================

if not st.session_state.authenticated:
    show_authentication_page()
    st.stop()

logged_in_user = st.session_state.user

if logged_in_user.get("role") == "admin":
    show_admin_dashboard()
    st.stop()

profile, student_skills, student_interests = load_student_data(
    logged_in_user["id"]
)

if profile is None:
    st.error("Student profile not found.")
    if st.button("Logout"):
        logout()
    st.stop()

student_id = profile["student_id"]
st.session_state["current_profile"] = dict(profile)

recommendations = get_recommendations(
    student_id,
    top_n=5,
)

current_page = st.session_state.page

if current_page == "Dashboard":
    show_dashboard(
        profile,
        student_skills,
        student_interests,
        recommendations,
    )
elif current_page == "My Profile":
    show_profile_page(
        profile,
        student_skills,
        student_interests,
    )
elif current_page == "Skill Recommendations":
    show_skill_recommendations(recommendations)
elif current_page == "Project Recommendations":
    show_project_recommendations(recommendations)

elif current_page == "Live Internships":
    show_live_internships(student_skills,
        student_interests,)

elif current_page == "Knowledge Graph":
    show_knowledge_graph(
        student_id,
        recommendations,
    )

st.markdown(
    f"""
    <div class="footer">
        {html.escape(APP_TITLE)}
    </div>
    """,
    unsafe_allow_html=True,
)
