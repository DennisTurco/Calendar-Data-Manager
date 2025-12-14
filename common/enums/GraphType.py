from enum import Enum

class GraphType(Enum):
    HOURS_PER_YEAR = 'Hours per Year'
    HOURS_PER_MONTH = 'Hours per Month'
    HOURS_BY_SUMMARY_BAR = 'Hours by Summary Bar chart'
    HOURS_BY_SUMMARY_PIE = 'Hours by Summary Pie chart'
    HOURS_PER_YEAR_BY_SUMMARY = 'Hours per Year By Summary'
    HOURS_PER_MONTH_BY_SUMMARY = 'Hours per Month By Summary'
    HOURS_PER_MONTH_GROUPED_BY_YEAR = 'Hours per Month Grouped By Year'

    @staticmethod
    def to_list() -> list[str]:
        return [GraphType.HOURS_PER_YEAR.value, GraphType.HOURS_PER_MONTH.value, GraphType.HOURS_BY_SUMMARY_BAR.value, GraphType.HOURS_BY_SUMMARY_PIE.value, GraphType.HOURS_PER_YEAR_BY_SUMMARY.value, GraphType.HOURS_PER_MONTH_BY_SUMMARY.value, GraphType.HOURS_PER_MONTH_GROUPED_BY_YEAR.value]
