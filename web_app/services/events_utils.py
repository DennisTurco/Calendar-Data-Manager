from datetime import datetime, timedelta


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

            duration_str = ""
            if start_val and end_val:
                try:
                    s = datetime.fromisoformat(start_val.replace("Z", "+00:00"))
                    e = datetime.fromisoformat(end_val.replace("Z", "+00:00"))
                    duration_str = EventsUtils.convert_duration_time(e, s)
                except Exception:
                    pass

            result.append({
                "index": index,
                "id": event.get("id", ""),
                "summary": event.get("summary") or "(no summary)",
                "start": start_val,
                "end": end_val,
                "duration": duration_str,
            })
        return result

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

            duration_str = ""
            try:
                delta = event.get("duration", {})
                duration_str = EventsUtils.convert_duration_time_by_delta(delta)
            except Exception:
                pass

            result.append({
                "index": event.get("index", {}),
                "summary": event.get("summary", {}),
                "duration": duration_str,
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