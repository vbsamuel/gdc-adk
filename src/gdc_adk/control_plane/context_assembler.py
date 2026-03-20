from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class ContextAssemblyRequest:
    prompt: str
    system_prompt: str | None = None
    supporting_context: tuple[str, ...] = ()


@dataclass(frozen=True)
class ContextAssemblyResult:
    prompt: str
    system_prompt: str | None
    supporting_context: tuple[str, ...] = field(default_factory=tuple)


def assemble_provider_context(request: ContextAssemblyRequest) -> ContextAssemblyResult:
    if not request.prompt.strip():
        raise ValueError("prompt must be non-empty")
    normalized_context = tuple(item.strip() for item in request.supporting_context if item.strip())
    return ContextAssemblyResult(
        prompt=request.prompt.strip(),
        system_prompt=request.system_prompt.strip() if request.system_prompt else None,
        supporting_context=normalized_context,
    )
