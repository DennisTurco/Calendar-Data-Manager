from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional

@dataclass
class EventInfo():
    summary: str
    description: str
    start: Optional[datetime]
    end: Optional[datetime]
    color: int
    time_zone: str

    @property
    def duration(self) -> Optional[timedelta]:
        if self.start is None or self.end is None:
            return None
        return self.end - self.start
