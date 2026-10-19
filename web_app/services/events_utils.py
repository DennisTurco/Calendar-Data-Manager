from datetime import datetime, timedelta

from common.ConfigKeys import ConfigKeys


class EventsUtils:

    @staticmethod
    def format_events_list(events: list) -> list:
        """Return individual event rows matching the desktop viewer format."""
        result = []
        for index, event in enumerate(events, start=1):
            start = event.get("start", {})
            end = event.get("end", {})
            start_val = start.get("dateTime") or start.get("date") or ""
            end_val = end.get("dateTime") or end.get("date") or ""

            delta = None
            if start_val and end_val:
                try:
                    s = datetime.fromisoformat(start_val.replace("Z", "+00:00"))
                    e = datetime.fromisoformat(end_val.replace("Z", "+00:00"))
                    delta = e - s
                except Exception:
                    pass

            result.append({
                "index": index,
                "id": event.get("id", ""),
                "summary": event.get("summary") or "(no summary)",
                "start": start_val,
                "end": end_val,
                "start_display": EventsUtils.format_display_datetime(start_val),
                "end_display": EventsUtils.format_display_datetime(end_val),
                "duration": EventsUtils.convert_duration_time_by_delta(delta) if delta is not None else "",
                "duration_human": EventsUtils.humanize_duration(delta) if delta is not None else "",
                "duration_seconds": int(delta.total_seconds()) if delta is not None else 0,
                "color": EventsUtils.event_color(event.get("colorId")),
            })
        return result

    @staticmethod
    def event_color(color_id) -> dict:
        """Name and hex of a Google event colorId; events without one use the calendar's default color."""
        colors = ConfigKeys.Keys.EVENT_COLOR.value
        names = list(colors.keys())
        try:
            name = names[int(color_id) - 1]
            return {"name": name, "hex": colors[name]}
        except (TypeError, ValueError, IndexError):
            return {"name": "Calendar default", "hex": None}

    @staticmethod
    def humanize_duration(delta: timedelta) -> str:
        """Compact, readable duration: '45m', '2h', '1h 30m', '312h 5m'."""
        total_minutes = int(round(delta.total_seconds() / 60))
        if total_minutes <= 0:
            return "0m"
        h, m = divmod(total_minutes, 60)
        if h and m:
            return f"{h}h {m}m"
        return f"{h}h" if h else f"{m}m"

    @staticmethod
    def format_display_datetime(value: str) -> str:
        """Render an API date/dateTime string as 'YYYY-MM-DD HH:MM' (or just the date for all-day events)."""
        if not value:
            return ""
        try:
            if "T" not in value:
                return value
            return datetime.fromisoformat(value.replace("Z", "+00:00")).strftime("%Y-%m-%d %H:%M")
        except ValueError:
            return value

    @staticmethod
    def calculate_duration_and_aggregate_by_summary(events: list) -> list:
        totals: dict[str, timedelta] = {}
        for event in events:
            start = event.get("start", {})
            end = event.get("end", {})
            start_val = start.get("dateTime") or start.get("date")
            end_val = end.get("dateTime") or end.get("date")

            duration = timedelta()
            try:
                s = datetime.fromisoformat(start_val.replace("Z", "+00:00"))
                e = datetime.fromisoformat(end_val.replace("Z", "+00:00"))
                duration = e - s
            except Exception:
                pass

            summary = event.get("summary") or "(no summary)"
            totals[summary] = totals.get(summary, timedelta()) + duration

        sorted_items = sorted(totals.items(), key=lambda x: x[1], reverse=True)
        return [
            {"index": i + 1, "summary": summary, "duration": duration}
            for i, (summary, duration) in enumerate(sorted_items)
        ]

    @staticmethod
    def calculate_total_duration(events: list) -> timedelta:
        total_sum = timedelta()
        for event in events:
            total_sum += event.get("duration", timedelta())
        return total_sum

    @staticmethod
    def convert_duration_time_to_string(events: list) -> list:
        result = []
        for event in events:

            duration_str, duration_human, seconds = "", "", 0
            try:
                delta = event.get("duration", {})
                duration_str = EventsUtils.convert_duration_time_by_delta(delta)
                duration_human = EventsUtils.humanize_duration(delta)
                seconds = int(delta.total_seconds())
            except Exception:
                pass

            result.append({
                "index": event.get("index", {}),
                "summary": event.get("summary", {}),
                "duration": duration_str,
                "duration_human": duration_human,
                "duration_seconds": seconds,
            })
        return result

    @staticmethod
    def convert_duration_time(date_end: datetime, date_start: datetime) -> str:
        delta = date_end - date_start
        return EventsUtils.convert_duration_time_by_delta(delta)

    @staticmethod
    def convert_duration_time_by_delta(delta: timedelta) -> str:
        total_seconds = int(delta.total_seconds())
        h, remainder = divmod(total_seconds, 3600)
        m, s_sec = divmod(remainder, 60)
        return f"{h}:{m:02d}:{s_sec:02d}"