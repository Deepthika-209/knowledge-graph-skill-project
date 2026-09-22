from src.knowledge_graph import build_knowledge_graph
from src.recommender.recommendation_engine import get_recommendations

from pyvis.network import Network


# ============================================================
# KNOWLEDGE GRAPH VISUALIZATION
# ============================================================

def create_knowledge_graph_visualization(
    student_id=None
):

    kg = build_knowledge_graph()

    network = Network(
        height="700px",
        width="100%",
        directed=True,
        bgcolor="#f8fafc",
        font_color="#1f2937"
    )


    # ========================================================
    # COLOR PALETTE
    # ========================================================

    colors = {

        "Student": {
            "background": "#8b5cf6",
            "border": "#6d28d9",
            "highlight": "#a78bfa"
        },

        "Skill": {
            "background": "#60a5fa",
            "border": "#2563eb",
            "highlight": "#93c5fd"
        },

        "Project": {
            "background": "#34d399",
            "border": "#059669",
            "highlight": "#6ee7b7"
        },

        "Domain": {
            "background": "#f59e0b",
            "border": "#d97706",
            "highlight": "#fbbf24"
        }
    }


    # ========================================================
    # SELECT NODES
    # ========================================================

    if student_id is None:

        selected_nodes = set(
            kg.nodes()
        )

    else:

        student_node = (
            f"student:{student_id}"
        )

        selected_nodes = set()

        if student_node in kg:

            selected_nodes.add(
                student_node
            )


        # ----------------------------------------------------
        # Student direct relationships
        # ----------------------------------------------------

        for _, target, data in kg.out_edges(
            student_node,
            data=True
        ):

            selected_nodes.add(
                target
            )


        # ----------------------------------------------------
        # Related skills + prerequisites
        # ----------------------------------------------------

        direct_skill_nodes = [

            node
            for node in selected_nodes

            if kg.nodes[node].get("label")
            == "Skill"
        ]


        for skill_node in direct_skill_nodes:

            for _, target, data in kg.out_edges(
                skill_node,
                data=True
            ):

                relation = data.get(
                    "relation"
                )

                if relation in [
                    "RELATED_TO",
                    "PREREQUISITE_OF"
                ]:

                    selected_nodes.add(
                        target
                    )


        # ----------------------------------------------------
        # Recommended projects
        # ----------------------------------------------------

        recommendations = get_recommendations(
            student_id,
            top_n=5
        )


        recommended_projects = [

            project["project"]

            for project in
            recommendations["projects"]

        ]


        for project_name in recommended_projects:

            project_node = (
                f"project:{project_name}"
            )

            if project_node in kg:

                selected_nodes.add(
                    project_node
                )


                # Project required skills

                for _, skill_node, data in kg.out_edges(
                    project_node,
                    data=True
                ):

                    if data.get(
                        "relation"
                    ) == "REQUIRES":

                        selected_nodes.add(
                            skill_node
                        )


    # ========================================================
    # ADD NODES
    # ========================================================

    for node in selected_nodes:

        data = kg.nodes[node]

        node_type = data.get(
            "label",
            "Node"
        )


        # ----------------------------------------------------
        # Display name
        # ----------------------------------------------------

        if node_type == "Student":

            display_name = data.get(
                "name",
                data.get(
                    "student_id",
                    node
                )
            )

        elif node_type == "Project":

            display_name = data.get(
                "title",
                node
            )

        else:

            display_name = data.get(
                "name",
                node
            )


        # ----------------------------------------------------
        # Visual configuration
        # ----------------------------------------------------

        if node_type == "Student":

            shape = "star"
            size = 34

        elif node_type == "Skill":

            shape = "dot"
            size = 22

        elif node_type == "Project":

            shape = "box"
            size = 27

        elif node_type == "Domain":

            shape = "diamond"
            size = 30

        else:

            shape = "dot"
            size = 20


        color = colors.get(
            node_type,
            {
                "background": "#94a3b8",
                "border": "#64748b",
                "highlight": "#cbd5e1"
            }
        )


        # ----------------------------------------------------
        # Tooltip
        # ----------------------------------------------------

        tooltip = (
            f"<b>Type:</b> {node_type}<br>"
            f"<b>Name:</b> {display_name}"
        )


        if node_type == "Skill":

            difficulty = data.get(
                "difficulty"
            )

            skill_type = data.get(
                "type"
            )

            if difficulty is not None:

                tooltip += (
                    f"<br><b>Difficulty:</b> "
                    f"{difficulty}"
                )

            if skill_type:

                tooltip += (
                    f"<br><b>Skill Type:</b> "
                    f"{skill_type}"
                )


        elif node_type == "Project":

            domain = data.get(
                "domain"
            )

            difficulty = data.get(
                "difficulty"
            )

            project_type = data.get(
                "type"
            )

            if domain:

                tooltip += (
                    f"<br><b>Domain:</b> "
                    f"{domain}"
                )

            if difficulty is not None:

                tooltip += (
                    f"<br><b>Difficulty:</b> "
                    f"{difficulty}"
                )

            if project_type:

                tooltip += (
                    f"<br><b>Type:</b> "
                    f"{project_type}"
                )


        # ----------------------------------------------------
        # Add node
        # ----------------------------------------------------

        network.add_node(

            node,

            label=display_name,

            title=tooltip,

            shape=shape,

            size=size,

            color={

                "background":
                    color["background"],

                "border":
                    color["border"],

                "highlight": {

                    "background":
                        color["highlight"],

                    "border":
                        color["border"]
                },

                "hover": {

                    "background":
                        color["highlight"],

                    "border":
                        color["border"]
                }
            },

            borderWidth=2,

            shadow={
                "enabled": True,
                "color": "rgba(0,0,0,0.18)",
                "size": 8,
                "x": 2,
                "y": 3
            }
        )


    # ========================================================
    # RELATIONSHIP COLORS
    # ========================================================

    relation_colors = {

        "HAS_SKILL": "#8b5cf6",

        "INTERESTED_IN": "#f59e0b",

        "RELATED_TO": "#60a5fa",

        "PREREQUISITE_OF": "#ef4444",

        "REQUIRES": "#10b981",

        "BELONGS_TO": "#6366f1",

        "PART_OF": "#14b8a6",

        "SUBDOMAIN_OF": "#f97316"
    }


    # ========================================================
    # ADD EDGES
    # ========================================================

    for source, target, data in kg.edges(
        data=True
    ):

        if (
            source not in selected_nodes
            or target not in selected_nodes
        ):

            continue


        relation = data.get(
            "relation",
            "RELATED"
        )


        edge_color = relation_colors.get(
            relation,
            "#94a3b8"
        )


        network.add_edge(

            source,

            target,

            title=f"Relationship: {relation}",

            label=relation,

            color={
                "color": edge_color,
                "highlight": edge_color,
                "hover": edge_color
            },

            arrows="to",

            width=2,

            smooth={
                "enabled": True,
                "type": "dynamic"
            }
        )


    # ========================================================
    # PYVIS OPTIONS
    # ========================================================

    network.set_options(
        """
        {
            "nodes": {
                "font": {
                    "size": 14,
                    "face": "Arial",
                    "color": "#1f2937"
                },

                "borderWidth": 2,

                "shadow": {
                    "enabled": true,
                    "color": "rgba(0,0,0,0.15)",
                    "size": 8,
                    "x": 2,
                    "y": 3
                }
            },

            "edges": {

                "arrows": {
                    "to": {
                        "enabled": true,
                        "scaleFactor": 0.7
                    }
                },

                "font": {
                    "size": 9,
                    "face": "Arial",
                    "align": "middle",
                    "color": "#475569",
                    "strokeWidth": 3,
                    "strokeColor": "#ffffff"
                },

                "smooth": {
                    "enabled": true,
                    "type": "dynamic"
                }
            },

            "physics": {

                "enabled": true,

                "solver": "forceAtlas2Based",

                "forceAtlas2Based": {

                    "gravitationalConstant": -80,

                    "centralGravity": 0.015,

                    "springLength": 150,

                    "springConstant": 0.08,

                    "damping": 0.45
                },

                "minVelocity": 0.75
            },

            "interaction": {

                "hover": true,

                "navigationButtons": true,

                "keyboard": true,

                "zoomView": true,

                "dragView": true,

                "dragNodes": true
            }
        }
        """
    )


    # ========================================================
    # SAVE GRAPH
    # ========================================================

    output_file = "knowledge_graph.html"

    network.write_html(
        output_file
    )

    return output_file


# ============================================================
# DIRECT TEST
# ============================================================

if __name__ == "__main__":

    output_file = (
        create_knowledge_graph_visualization(
            "S01"
        )
    )

    print(
        "Student-specific Knowledge Graph created:"
    )

    print(
        output_file
    )