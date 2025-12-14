from flask import Blueprint, render_template
import markdown
from common.InformationMessages import InformationMessages
from common.enums.GraphType import GraphType

bp = Blueprint("graph", __name__, url_prefix="/graph")

@bp.route("/")
def graph():
    graph_types = GraphType.to_list()
    print(graph_types)
    return render_template(
        "graph.html",
        active_page="graph",
        section_message = markdown.markdown(InformationMessages.graph_info_message, extensions=["extra", "nl2br"]),
        graph_types = GraphType.to_list()
        )
