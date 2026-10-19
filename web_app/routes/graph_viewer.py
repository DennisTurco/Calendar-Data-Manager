from flask import Blueprint, flash, session, render_template
from common.Plotter import Plotter
from common.enums.GraphType import GraphType
from web_app.CacheManager import CacheManager
from web_app.services.events_utils import EventsUtils

bp = Blueprint("graph_viewer", __name__, url_prefix="/graphs")

# Categorical palette shared by every chart so colors read as one system in both themes
_CHART_COLORWAY = ["#2fa88a", "#6366f1", "#f59e0b", "#ec4899", "#0ea5e9", "#84cc16", "#a855f7", "#f97316", "#64748b", "#ef4444"]


@bp.route("/", methods=["GET"])
def view_graphs():
    cache_id = session.get("events_cache_id")
    selected_graphs = session.get("selected_graphs")

    events_json = CacheManager.get(cache_id)
    if not events_json or not selected_graphs:
        return render_template("graphs.html", active_page="get events", graph_htmls=[], events_list=[])

    events = Plotter.load_data_from_list(events_json)
    aggregated = EventsUtils.calculate_duration_and_aggregate_by_summary(events_json)
    total_duration = EventsUtils.calculate_total_duration(aggregated)
    total_seconds = total_duration.total_seconds() or 1
    shares = [row["duration"].total_seconds() / total_seconds * 100 for row in aggregated]
    events_list = EventsUtils.convert_duration_time_to_string(aggregated)
    for row, share in zip(events_list, shares):
        row["share"] = share

    graph_htmls = []
    for graph_type in selected_graphs:
        fig = _get_fig(events, graph_type)
        if fig is None:
            continue
        _style_fig(fig)
        graph_htmls.append(fig.to_html(
            full_html=False,
            include_plotlyjs="cdn" if not graph_htmls else False,
            config={"displaylogo": False, "responsive": True},
        ))

    session.pop("events_cache_id", None)
    session.pop("selected_graphs", None)

    return render_template(
        "graphs.html",
        active_page="get events",
        graph_htmls=graph_htmls,
        events_list=events_list,
        total_duration=EventsUtils.humanize_duration(total_duration),
        total_duration_hours=total_duration.total_seconds() / 3600,
        total_events=len(events_json),
    )


def _style_fig(fig):
    """Transparent, theme-neutral layout; colors for text/grid are set client-side per theme."""
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, ui-sans-serif, system-ui, sans-serif", size=12),
        title=dict(font=dict(size=15), x=0, xanchor="left", pad=dict(l=4)),
        margin=dict(l=48, r=16, t=56, b=48),
        colorway=_CHART_COLORWAY,
        hoverlabel=dict(font=dict(family="Inter, ui-sans-serif, system-ui, sans-serif")),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
    )
    # plotly.express bakes its default colors into each trace, so re-assign them explicitly
    for i, trace in enumerate(fig.data):
        if trace.type == "bar" and isinstance(trace.marker.color, str):
            trace.marker.color = _CHART_COLORWAY[i % len(_CHART_COLORWAY)]
        elif trace.type == "pie":
            n = len(trace.labels) if trace.labels is not None else len(_CHART_COLORWAY)
            trace.marker.colors = [_CHART_COLORWAY[j % len(_CHART_COLORWAY)] for j in range(n)]
            trace.marker.line = dict(width=0)
    if fig.layout.coloraxis.colorscale is not None:
        fig.update_layout(coloraxis_colorscale=[[0, "#b9ead9"], [1, "#0f766e"]])
    # Value labels added by Plotter sit exactly on the bar top: lift them so they don't overlap the bar
    fig.update_annotations(yshift=10)
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(zeroline=False)


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
