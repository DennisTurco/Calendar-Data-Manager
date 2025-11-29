from dataclasses import dataclass

from common.entities.TimeRange import TimeRange

@dataclass
class EventInfo:
    summary: str
    description: str
    range: TimeRange
    color: int
    time_zone: str
