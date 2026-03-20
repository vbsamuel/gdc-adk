from google.adk.agents import Agent

from gdc_adk.capabilities.time import get_current_time, get_local_system_time
from gdc_adk.capabilities.weather import get_weather
from gdc_adk.config.settings import get_adk_agent_settings
from gdc_adk.control_plane.model_registry import resolve_adk_model_name


def build_weather_time_agent() -> Agent:
    cfg = get_adk_agent_settings("weather_time_agent")
    model_name = resolve_adk_model_name(cfg["adk_model_alias"])

    return Agent(
        name=cfg["name"],
        model=model_name,
        description=cfg["description"],
        instruction=cfg["instruction"],
        tools=[get_current_time, get_local_system_time, get_weather],
    )