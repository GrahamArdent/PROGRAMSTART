"""Bounded exact document evidence for PROGRAMSTART semantic input.
Readers are supplied by an already authorized caller; hashes grant no access.
"""

from __future__ import annotations

import hashlib
import json
import re
from collections.abc import Callable

from pydantic import BaseModel, ConfigDict

_REFERENCE = re.compile(r"^[^\x00-\x20\x7f]+:sha256:([0-9a-f]{64})$")
MAX_DOCUMENTS = 4
MAX_DOCUMENT_BYTES = 8192
MAX_TOTAL_BYTES = 16384
MAX_REQUEST_BYTES = 24576
REQUIRED_CONTEXT_PROVENANCE_PATH = "context.required_context_refs"


class RequiredContextDocument(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    reference: str
    text: str


def validate_required_context_strings(value: object) -> None:
    """Refuse unencodable identifiers as well as document text before effects."""
    try:
        json.dumps(value, ensure_ascii=False).encode("utf-8", errors="strict")
    except UnicodeError as exc:
        raise ValueError("required context input must be strict UTF-8") from exc


def validate_required_refs(refs: list[str], durable_refs: list[str]) -> None:
    """Validate the role declaration without fetching or granting authority."""
    if len(refs) > MAX_DOCUMENTS or len(set(refs)) != len(refs):
        raise ValueError("required context references must be unique and bounded")
    for ref in refs:
        validate_required_context_strings(ref)
        if len(ref) > 512 or not _REFERENCE.fullmatch(ref) or ref not in durable_refs:
            raise ValueError("required context reference must be immutable and in durable references")


def validate_required_context(
    refs: list[str],
    documents: list[RequiredContextDocument],
    durable_refs: list[str],
) -> None:
    validate_required_refs(refs, durable_refs)
    if not refs or [doc.reference for doc in documents] != refs:
        raise ValueError("required context documents must match declared references exactly in order")
    total = 0
    for doc in documents:
        if not doc.text.strip():
            raise ValueError("required context document must contain meaningful text")
        try:
            content = doc.text.encode("utf-8", errors="strict")
        except UnicodeError as exc:
            raise ValueError("required context must be strict UTF-8") from exc
        total += len(content)
        if len(content) > MAX_DOCUMENT_BYTES or total > MAX_TOTAL_BYTES:
            raise ValueError("required context byte bound exceeded")
        if hashlib.sha256(content).hexdigest() != doc.reference.rsplit(":sha256:", 1)[1]:
            raise ValueError("required context content digest mismatch")


def capture_required_context(
    required_refs: list[str],
    reader: Callable[[str], bytes],
) -> list[RequiredContextDocument]:
    """Capture admitted exact bytes; propagate missing/permission errors unchanged."""
    validate_required_refs(required_refs, required_refs)
    if not required_refs:
        raise ValueError("required context declaration is empty")
    documents = []
    for ref in required_refs:
        raw = reader(ref)
        if not isinstance(raw, bytes):
            raise ValueError("required context reader must return exact bytes")
        if len(raw) > MAX_DOCUMENT_BYTES:
            raise ValueError("required context byte bound exceeded")
        try:
            text = raw.decode("utf-8", errors="strict")
        except UnicodeError as exc:
            raise ValueError("required context must be strict UTF-8") from exc
        documents.append(RequiredContextDocument(reference=ref, text=text))
    validate_required_context(required_refs, documents, required_refs)
    return documents
