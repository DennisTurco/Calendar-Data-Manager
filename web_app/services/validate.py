from datetime import datetime

class Validate:
    @staticmethod
    def is_date_provided_valid(date_from_str, date_to_str) -> bool:
        return date_from_str and date_to_str and len(date_from_str) > 0 and len(date_to_str) > 0

    @staticmethod
    def is_date_interval_valid(date_from: datetime, date_to: datetime) -> bool:
        return date_from < date_to