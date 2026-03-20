from __future__ import annotations

from collections import defaultdict
from functools import lru_cache
from typing import TypedDict

try:
    import geonamescache
except ImportError:  # pragma: no cover - exercised through fallback behavior tests
    geonamescache = None


class CityRecord(TypedDict):
    city_id: str
    canonical_name: str
    normalized_name: str
    country_code: str | None
    admin1_code: str | None
    timezone: str
    latitude: float
    longitude: float
    population: int
    aliases: list[str]


def normalize_city_name(city: str | None) -> str:
    return (city or "").strip().lower()


def _load_raw_cities() -> dict[str, dict[str, object]]:
    if geonamescache is not None:
        return geonamescache.GeonamesCache().get_cities()
    return {
        "paris_fr": {
            "name": "Paris",
            "countrycode": "FR",
            "admin1code": "11",
            "timezone": "Europe/Paris",
            "latitude": "48.85341",
            "longitude": "2.3488",
            "population": 2138551,
            "alternatenames": ["Paris, France"],
        },
        "london_gb": {
            "name": "London",
            "countrycode": "GB",
            "admin1code": "H9",
            "timezone": "Europe/London",
            "latitude": "51.50853",
            "longitude": "-0.12574",
            "population": 8961989,
            "alternatenames": ["London, UK"],
        },
        "new_york_us": {
            "name": "New York",
            "countrycode": "US",
            "admin1code": "NY",
            "timezone": "America/New_York",
            "latitude": "40.71427",
            "longitude": "-74.00597",
            "population": 8804190,
            "alternatenames": ["NYC", "New York City"],
        },
        "tokyo_jp": {
            "name": "Tokyo",
            "countrycode": "JP",
            "admin1code": "40",
            "timezone": "Asia/Tokyo",
            "latitude": "35.6895",
            "longitude": "139.69171",
            "population": 13929286,
            "alternatenames": ["Tokyo, Japan"],
        },
    }


@lru_cache(maxsize=1)
def get_city_registry(min_population: int = 100_000) -> dict[str, CityRecord]:
    registry: dict[str, CityRecord] = {}
    for city_id, info in _load_raw_cities().items():
        population = int(info.get("population", 0) or 0)
        if population < min_population:
            continue
        canonical_name = str(info["name"])
        normalized_name = normalize_city_name(canonical_name)
        aliases = sorted(
            {
                normalize_city_name(alias)
                for alias in (info.get("alternatenames", []) or [])
                if isinstance(alias, str) and normalize_city_name(alias) and normalize_city_name(alias) != normalized_name
            }
        )
        registry[city_id] = CityRecord(
            city_id=city_id,
            canonical_name=canonical_name,
            normalized_name=normalized_name,
            country_code=str(info.get("countrycode") or "") or None,
            admin1_code=str(info.get("admin1code") or "") or None,
            timezone=str(info.get("timezone") or ""),
            latitude=float(info.get("latitude")),
            longitude=float(info.get("longitude")),
            population=population,
            aliases=aliases,
        )
    return registry


@lru_cache(maxsize=1)
def get_city_alias_index() -> dict[str, list[str]]:
    alias_index: dict[str, list[str]] = defaultdict(list)
    registry = get_city_registry()
    sorted_cities = sorted(registry.items(), key=lambda item: item[1]["population"], reverse=True)
    for city_id, city_record in sorted_cities:
        alias_index[city_record["normalized_name"]].append(city_id)
        for alias in city_record["aliases"]:
            alias_index[alias].append(city_id)
    return dict(alias_index)


def lookup_city_candidates(name: str) -> list[CityRecord]:
    normalized_name = normalize_city_name(name)
    registry = get_city_registry()
    return [registry[city_id] for city_id in get_city_alias_index().get(normalized_name, [])]


def lookup_city(name: str) -> CityRecord | None:
    candidates = lookup_city_candidates(name)
    if not candidates:
        return None
    return candidates[0]
