from typing import Optional
import datetime

from uptime_kuma_api import MaintenanceStrategy
from pydantic import BaseModel, Field


class Maintenance(BaseModel):
    """Title (str) – Title.

    strategy (MaintenanceStrategy) – Strategy

    active (bool, optional) – True if maintenances is active, defaults to True

    description (str, optional) – Description, defaults to ""

    dateRange (list, optional) – DateTime Range, defaults to ["<current date>"]

    intervalDay (int, optional) – Interval (Run once every day), defaults to 1

    weekdays (list, optional) – List that contains the days of the week on which the maintenances is enabled (Sun = 0, Mon = 1, …, Sat = 6). Required for strategy RECURRING_WEEKDAY., defaults to [].

    daysOfMonth (list, optional) – List that contains the days of the month on which the maintenances is enabled (Day 1 = 1, Day 2 = 2, …, Day 31 = 31) and the last day of the month (Last Day of Month = "lastDay1", 2nd Last Day of Month = "lastDay2", 3rd Last Day of Month = "lastDay3", 4th Last Day of Month = "lastDay4"). Required for strategy RECURRING_DAY_OF_MONTH., defaults to [].

    timeRange (list, optional) – Maintenance Time Window of a Day, defaults to [{"hours": 2, "minutes": 0}, {"hours": 3, "minutes": 0}].
    """

    title: str
    strategy: MaintenanceStrategy
    active: Optional[bool] = True
    description: Optional[str] = ""
    dateRange: Optional[list] = Field(
        default_factory=lambda: [datetime.date.today().strftime("%Y-%m-%d 00:00:00")]
    )
    intervalDay: Optional[int] = 1
    weekdays: Optional[list] = Field(default_factory=list)
    daysOfMonth: Optional[list] = Field(default_factory=list)
    timeRange: Optional[list] = Field(
        default_factory=lambda: [{"hours": 2, "minutes": 0}, {"hours": 3, "minutes": 0}]
    )
    cron: Optional[str] = "30 3 * * *"
    durationMinutes: Optional[int] = 60
    timezoneOption: Optional[str] = None

    class Config:
        use_enum_values = True


class MaintenanceUpdate(Maintenance):
    title: Optional[str] = None
    strategy: Optional[MaintenanceStrategy] = None


class MonitorMaintenance(BaseModel):
    id: int
    name: str


class StatusPageMaintenance(BaseModel):
    id: int
    title: str
