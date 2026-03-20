from __future__ import annotations

from typing import Iterable

from gdc_adk.memory.contracts import ContextBlock, ContextExportResult, ContextStoreResult


_CONTEXT_BLOCKS: dict[str, ContextBlock] = {}


def put_context_block(context_block: ContextBlock) -> ContextStoreResult:
    if not isinstance(context_block, ContextBlock):
        raise ValueError("context_block must be a ContextBlock.")
    if not context_block.source_artifact_ids:
        raise ValueError("context_block.source_artifact_ids must contain at least one artifact identifier.")
    if context_block.context_block_id in _CONTEXT_BLOCKS:
        raise ValueError(f"context_block_id already exists: {context_block.context_block_id}")
    _CONTEXT_BLOCKS[context_block.context_block_id] = context_block
    return ContextStoreResult(status="stored", context_block=context_block, message="Context block stored.")


def get_context_block(context_block_id: str) -> ContextStoreResult | None:
    if not isinstance(context_block_id, str) or not context_block_id.strip():
        raise ValueError("context_block_id must be a non-empty string.")
    block = _CONTEXT_BLOCKS.get(context_block_id)
    if block is None:
        return None
    return ContextStoreResult(status="found", context_block=block, message="Context block found.")


def list_context_blocks_by_artifact(artifact_id: str) -> list[ContextBlock]:
    if not isinstance(artifact_id, str) or not artifact_id.strip():
        raise ValueError("artifact_id must be a non-empty string.")
    return [block for block in _CONTEXT_BLOCKS.values() if artifact_id in block.source_artifact_ids]


def mark_context_block_superseded(context_block_id: str, superseded_by_id: str) -> ContextStoreResult:
    if not isinstance(superseded_by_id, str) or not superseded_by_id.strip():
        raise ValueError("superseded_by_id must be a non-empty string.")
    result = get_context_block(context_block_id)
    if result is None or result.context_block is None:
        raise ValueError(f"Unknown context_block_id: {context_block_id}")
    updated_block = ContextBlock(
        context_block_id=result.context_block.context_block_id,
        block_type=result.context_block.block_type,
        content=result.context_block.content,
        source_artifact_ids=result.context_block.source_artifact_ids,
        created_at=result.context_block.created_at,
        tags=result.context_block.tags,
        validity_window=result.context_block.validity_window,
        superseded_by=superseded_by_id,
    )
    _CONTEXT_BLOCKS[context_block_id] = updated_block
    return ContextStoreResult(status="superseded", context_block=updated_block, message="Context block superseded.")


def export_context_blocks(filter_spec: dict[str, object] | None = None) -> ContextExportResult:
    filter_spec = dict(filter_spec or {})
    artifact_id = filter_spec.get("artifact_id")
    records: list[ContextBlock] = []
    for block in _CONTEXT_BLOCKS.values():
        if artifact_id is not None and artifact_id not in block.source_artifact_ids:
            continue
        records.append(block)
    return ContextExportResult(context_blocks=tuple(records))


def reset_context_store() -> None:
    _CONTEXT_BLOCKS.clear()


def load_context_blocks(records: Iterable[ContextBlock]) -> None:
    if not isinstance(records, Iterable):
        raise ValueError("records must be an iterable of ContextBlock.")
    reset_context_store()
    for record in records:
        if not isinstance(record, ContextBlock):
            raise ValueError("all records must be ContextBlock instances.")
        if record.context_block_id in _CONTEXT_BLOCKS:
            raise ValueError(f"Duplicate context_block_id during load: {record.context_block_id}")
        if not record.source_artifact_ids:
            raise ValueError("context block source_artifact_ids must be non-empty.")
        _CONTEXT_BLOCKS[record.context_block_id] = record
