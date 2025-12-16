from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from common.settings import DATE_FORMATTER

@dataclass
class TimeRange:
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None

    @property
    def duration(self) -> float:
        if self.date_from and self.date_to:
            return (self.date_to - self.date_from).total_seconds()
        return 0.0

    @classmethod
    def build_from_string(cls, date_from: str, date_to: str):
        df = datetime.strptime(date_from, DATE_FORMATTER) if date_from else None
        dt = datetime.strptime(date_to, DATE_FORMATTER) if date_to else None
        return cls(df, dt)