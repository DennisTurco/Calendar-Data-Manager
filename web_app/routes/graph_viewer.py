from flask import Blueprint, flash, session, render_template
from common.Plotter import Plotter
from common.enums.GraphType import GraphType
from web_app.CacheManager import CacheManager
from web_app.services.events_utils import EventsUtils

bp = Blueprint("graph_viewer", __name__, url_prefix="/graphs")

@bp.route("/", methods=["GET"])
def view_graphs():
    cache_id = session.get("events_cache_id")
    selected_graphs = session.get("selected_graphs")

    events_json = CacheManager.get(cache_id)
    if not events_json or not selected_graphs:
        return "No graphs to display. Please fetch events first."

    flash("Events fetched successfully! View your graphs below.", "success")

    events = Plotter.load_data_from_list(events_json)
    events_list = EventsUtils.calculate_duration_and_aggregate_by_summary(events_json)
    total_duration = EventsUtils.calculate_total_duration(events_list)
    events_list = EventsUtils.convert_duration_time_to_string(events_list)
    graph_htmls = [_get_fig(events, g).to_html(full_html=False) for g in selected_graphs if _get_fig(events, g)]

    session.pop("events_cache_id", None)
    session.pop("selected_graphs", None)

    return render_template(
        "graphs.html",
        graph_htmls=graph_htmls,
        events_list=events_list,
        total_duration=total_duration
    )

def _get_fig(events, graph_type):
    mapping = {
        GraphType.HOURS_PER_YEAR.value: Plotter.chart_total_hours_per_year,
        GraphType.HOURS_PER_MONTH.value: Plotter.chart_total_hours_per_month,
        GraphType.HOURS_BY_SUMMARY_BAR.value: Plotter.chart_total_hours_by_summary,
        GraphType.HOURS_BY_SUMMARY_PIE.value: Plotter.chart_total_hours_by_summary_pie,
        GraphType.HOURS_PER_YEAR_BY_SUMMARY.value: Plotter.chart_total_hours_per_year_by_summary,
        GraphType.HOURS_PER_MONTH_BY_SUMMARY.value: Plotter.chart_total_hours_per_month_by_summary,
        GraphType.HOURS_PER_MONTH_GROUPED_BY_YEAR.value: Plotter.chart_total_hours_per_month_grouped_by_year
    }
    func = mapping.get(graph_type)
    if func:
        return func(events, get=True)
    return None
