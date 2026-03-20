from __future__ import annotations

import datetime as dt
from typing import TypedDict
from zoneinfo import ZoneInfo

from gdc_adk.capabilities.geo import get_city_registry, lookup_city


class TimeLookupResult(TypedDict):
    status: str
    city: str
    timezone: str
    iso_datetime: str
    report: str
    error_code: str | None


class SupportedTimeCitiesResult(TypedDict):
    status: str
    count: int
    cities: list[str]
    report: str


def get_current_time(city: str) -> TimeLookupResult:
    city_record = lookup_city(city)
    if city_record is None:
        return TimeLookupResult(
            status="rejected",
            city=city,
            timezone="",
            iso_datetime="",
            report=f"Sorry, I don't have timezone information for '{city}'.",
            error_code="unknown_city",
        )

    now = dt.datetime.now(ZoneInfo(city_record["timezone"]))
    return TimeLookupResult(
        status="success",
        city=city_record["canonical_name"],
        timezone=city_record["timezone"],
        iso_datetime=now.isoformat(),
        report=f"The current time in {city_record['canonical_name']} is {now.strftime('%Y-%m-%d %I:%M:%S %p %Z')}.",
        error_code=None,
    )


def get_local_system_time() -> TimeLookupResult:
    now = dt.datetime.now().astimezone()
    return TimeLookupResult(
        status="success",
        city="local system",
        timezone=str(now.tzinfo),
        iso_datetime=now.isoformat(),
        report=f"The current local time on this system is {now.strftime('%Y-%m-%d %I:%M:%S %p %Z')}.",
        error_code=None,
    )


def list_supported_time_cities() -> SupportedTimeCitiesResult:
    cities = sorted(city["canonical_name"] for city in get_city_registry().values())
    return SupportedTimeCitiesResult(
        status="success",
        count=len(cities),
        cities=cities,
        report=f"I currently support time lookup for {len(cities)} cities.",
    )
