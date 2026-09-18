from src.knowledge_graph import build_knowledge_graph
from src.recommender.recommendation_engine import get_recommendations
from pyvis.network import Network


def create_knowledge_graph_visualization(student_id=None):

    kg = build_knowledge_graph()

    # --------------------------------------------------
    # CREATE NETWORK
    # --------------------------------------------------

    network = Network(
        height="650px",
        width="100%",
        directed=True,
        bgcolor="#ffffff",
        font_color="#222222"
    )

    # --------------------------------------------------
    # SELECT NODES
    # --------------------------------------------------

    if student_id is None:

        selected_nodes = set(kg.nodes())

    else:

        student_node = f"student:{student_id}"

        selected_nodes = set()

        # --------------------------------------------------
        # STUDENT NODE
        # --------------------------------------------------

        if student_node in kg:
            selected_nodes.add(student_node)

        # --------------------------------------------------
        # STUDENT'S DIRECT RELATIONSHIPS
        # --------------------------------------------------

        for _, target, data in kg.out_edges(
            student_node,
            data=True
        ):

            selected_nodes.add(target)

        # --------------------------------------------------
        # RELATED SKILLS AND PREREQUISITES
        # --------------------------------------------------

        direct_skill_nodes = [
            node
            for node in selected_nodes
            if kg.nodes[node].get("label") == "Skill"
        ]

        for skill_node in direct_skill_nodes:

            for _, target, data in kg.out_edges(
                skill_node,
                data=True
            ):

                if data["relation"] in [
                    "RELATED_TO",
                    "PREREQUISITE_OF"
                ]:

                    selected_nodes.add(target)

        # --------------------------------------------------
        # RECOMMENDED PROJECTS
        # --------------------------------------------------

        recommendations = get_recommendations(
            student_id,
            top_n=5
        )

        recommended_projects = [
            project["project"]
            for project in recommendations["projects"]
        ]

        for project_name in recommended_projects:

            project_node = f"project:{project_name}"

            if project_node in kg:

                selected_nodes.add(project_node)

                # Add skills required by the project
                for _, skill_node, data in kg.out_edges(
                    project_node,
                    data=True
                ):

                    if data["relation"] == "REQUIRES":

                        selected_nodes.add(skill_node)

    # --------------------------------------------------
    # ADD NODES
    # --------------------------------------------------

    for node in selected_nodes:

        data = kg.nodes[node]

        node_type = data.get(
            "label",
            "Node"
        )

        # --------------------------------------------------
        # DISPLAY NAME
        # --------------------------------------------------

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

        # --------------------------------------------------
        # NODE APPEARANCE
        # --------------------------------------------------

        if node_type == "Student":

            node_shape = "star"
            node_size = 30

        elif node_type == "Skill":

            node_shape = "dot"
            node_size = 20

        elif node_type == "Project":

            node_shape = "box"
            node_size = 25

        elif node_type == "Domain":

            node_shape = "diamond"
            node_size = 25

        else:

            node_shape = "dot"
            node_size = 18

        # --------------------------------------------------
        # TOOLTIP
        # --------------------------------------------------

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

        network.add_node(
            node,
            label=display_name,
            title=tooltip,
            shape=node_shape,
            size=node_size
        )

    # --------------------------------------------------
    # ADD EDGES
    # --------------------------------------------------

    for source, target, data in kg.edges(
        data=True
    ):

        if (
            source in selected_nodes
            and target in selected_nodes
        ):

            relation = data.get(
                "relation",
                "RELATED"
            )

            edge_title = (
                f"Relationship: {relation}"
            )

            network.add_edge(
                source,
                target,
                title=edge_title,
                label=relation
            )

    # --------------------------------------------------
    # VISUALIZATION OPTIONS
    # --------------------------------------------------

    network.set_options(
        """
        {
          "nodes": {
            "font": {
              "size": 14,
              "face": "Arial"
            },
            "borderWidth": 2
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
              "align": "middle"
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
              "gravitationalConstant": -50,
              "centralGravity": 0.01,
              "springLength": 120,
              "springConstant": 0.08,
              "damping": 0.4
            },
            "minVelocity": 0.75
          },

          "interaction": {
            "hover": true,
            "navigationButtons": true,
            "keyboard": true,
            "zoomView": true,
            "dragView": true
          }
        }
        """
    )

    # --------------------------------------------------
    # SAVE HTML
    # --------------------------------------------------

    output_file = "knowledge_graph.html"

    network.write_html(
        output_file
    )

    return output_file


# --------------------------------------------------
# TEST
# --------------------------------------------------

if __name__ == "__main__":

    output_file = create_knowledge_graph_visualization(
        "S01"
    )

    print(
        "Student-specific Knowledge Graph created:"
    )

    print(output_file)