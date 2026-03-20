from __future__ import annotations

from gdc_adk.providers.router import execute_task
from gdc_adk.providers.base import LLMRequest
from gdc_adk.memory.cache import get_cached, set_cached
from gdc_adk.control_plane.optimizer import cache_key_for, reuse_allowed


def ask_local_first(task_type: str, prompt: str, system: str | None = None):
    key = cache_key_for(task_type, prompt)

    if reuse_allowed(task_type):
        cached = get_cached(key)
        if cached is not None:
            return cached

    response = execute_task(task_type, LLMRequest(prompt=prompt, system=system))

    if reuse_allowed(task_type):
        set_cached(key, response)

    return response
