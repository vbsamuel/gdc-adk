from __future__ import annotations

from dataclasses import dataclass
from threading import Lock
from typing import Any, Callable, Protocol, TypeVar

from gdc_adk.config.settings import get_local_execution_config

T = TypeVar("T")


class ManagedLocalProvider(Protocol):
    name: str
    model: str
    backend_name: str
    is_local_backend: bool

    def warm_model(self, keep_alive: Any | None = None) -> None:
        ...

    def unload_model(self) -> None:
        ...


@dataclass(frozen=True)
class LocalExecutionConfig:
    max_concurrent_models: int = 1
    unload_after_request: bool = True
    ollama_keep_alive: Any = 0
    prefer_warm_model: bool = True
    allow_backend_switch: bool = True


def _load_local_execution_config() -> LocalExecutionConfig:
    local_cfg = get_local_execution_config()
    return LocalExecutionConfig(
        # Local execution is intentionally serialized for now. The config key is
        # accepted for forward compatibility, but behavior stays fixed at 1.
        max_concurrent_models=1,
        unload_after_request=bool(local_cfg.get("unload_after_request", True)),
        ollama_keep_alive=local_cfg.get("ollama_keep_alive", 0),
        prefer_warm_model=bool(local_cfg.get("prefer_warm_model", True)),
        allow_backend_switch=bool(local_cfg.get("allow_backend_switch", True)),
    )


class LocalModelManager:
    def __init__(self) -> None:
        self._config = _load_local_execution_config()
        self._execution_lock = Lock()
        self._active_provider: ManagedLocalProvider | None = None
        self._active_backend: str | None = None
        self._active_model: str | None = None

    def is_local_provider(self, provider: Any) -> bool:
        return bool(getattr(provider, "is_local_backend", False))

    def run(self, provider: ManagedLocalProvider, generate_fn: Callable[[], T]) -> T:
        if not self.is_local_provider(provider):
            return generate_fn()

        with self._execution_lock:
            self._prepare_provider(provider)
            try:
                return generate_fn()
            finally:
                if self._config.unload_after_request:
                    provider.unload_model()
                    self._clear_active(provider)

    def _prepare_provider(self, provider: ManagedLocalProvider) -> None:
        target_backend = provider.backend_name
        target_model = provider.model

        if self._active_backend == target_backend and self._active_model == target_model:
            self._active_provider = provider
            return

        if self._active_provider is not None:
            if self._active_backend != target_backend and not self._config.allow_backend_switch:
                raise RuntimeError(
                    f"Local backend switch denied: {self._active_backend} -> {target_backend}"
                )
            self._active_provider.unload_model()
            self._clear_active(self._active_provider)

        if self._config.prefer_warm_model and not self._config.unload_after_request:
            provider.warm_model(keep_alive=self._config.ollama_keep_alive)

        self._active_provider = provider
        self._active_backend = target_backend
        self._active_model = target_model

    def _clear_active(self, provider: ManagedLocalProvider) -> None:
        if (
            self._active_backend == provider.backend_name
            and self._active_model == provider.model
        ):
            self._active_provider = None
            self._active_backend = None
            self._active_model = None


local_model_manager = LocalModelManager()
