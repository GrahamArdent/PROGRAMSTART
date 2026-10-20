"""Exercise vector adapter logic against an in-memory external-store transport."""

import json
import sys
from types import SimpleNamespace
from typing import Any

import pytest

from scripts import programstart_retrieval as retrieval
from tests.test_programstart_retrieval import _minimal_index


class Collection:
    def __init__(self):
        self.rows = {}
        self.batches = []
        self.result: dict[str, Any] = {"ids": []}

    def count(self):
        return len(self.rows)

    def delete(self, *, where):
        assert where == {"source_type": {"$ne": ""}}
        self.rows.clear()

    def add(self, *, ids, documents, metadatas):
        self.batches.append(len(ids))
        self.rows.update({key: (document, metadata) for key, document, metadata in zip(ids, documents, metadatas, strict=True)})

    def query(self, *, query_texts, n_results):
        assert query_texts == ["query"]
        assert n_results <= self.count()
        return self.result


def test_vector_store_batches_reuses_and_maps_optional_transport_fields(monkeypatch, tmp_path):
    collection = Collection()

    class Client:
        def __init__(self, **kwargs):
            self.options = kwargs

        def get_or_create_collection(self, *, name, metadata):
            assert name == "programstart_context" and metadata == {"hnsw:space": "cosine"}
            return collection

    monkeypatch.setitem(sys.modules, "chromadb", SimpleNamespace(Client=Client, PersistentClient=Client))
    chunks = [retrieval.Chunk(source_type="test", source_id=str(i), text=f"document {i}", metadata={}) for i in range(501)]
    store = retrieval.EmbeddingStore(chunks, persist_path=tmp_path / "store")
    assert collection.batches == [500, 1]
    retrieval.EmbeddingStore(chunks)
    assert collection.batches == [500, 1], "same-size store should be reused"
    assert store.query("query") == []
    collection.result = {"ids": [["test:0"]]}
    result = store.query("query", top_k=1000)
    assert [(r.score, r.text, r.metadata) for r in result] == [(0.0, "", {})]
    collection.result.update(
        distances=[[0.25]], documents=[["document 0"]], metadatas=[[{"source_type": "test", "source_id": "0"}]]
    )
    result = store.query("query")
    assert [(r.source_id, r.score, r.text) for r in result] == [("0", 0.75, "document 0")]
    lexical = retrieval.LexicalSearcher(chunks)
    hybrid = retrieval.HybridSearcher(lexical, store)
    assert hybrid.search("query", method="vector")[0].source_id == "0"


def test_chroma_override_and_relative_index_load(monkeypatch, tmp_path):
    monkeypatch.setenv("PROGRAMSTART_CHROMA_PATH", str(tmp_path / "vectors"))
    assert retrieval.default_chroma_path() == tmp_path / "vectors"
    (tmp_path / "index.json").write_text(json.dumps(_minimal_index()))
    monkeypatch.setattr(retrieval, "workspace_path", lambda relative: tmp_path / relative)
    assert retrieval._load_or_build_index("index.json") == _minimal_index()


def test_corpus_tolerates_optional_guidance_shapes():
    index: dict[str, Any] = json.loads(json.dumps(_minimal_index()))
    index["knowledge_base"]["retrieval_guidance"] = {
        "principles": "not-a-list",
        "embedding_guidance": [],
        "vector_index_guidance": {"opaque": {}},
    }
    for entry in index["knowledge_base"].get("third_party_apis", []):
        entry.pop("base_url", None)
    chunks = retrieval.build_corpus(index)
    assert chunks and all(chunk.text for chunk in chunks)


def test_hybrid_ask_builds_assistant_after_store_setup(monkeypatch, tmp_path, capsys):
    index = tmp_path / "index.json"
    index.write_text(json.dumps(_minimal_index()))
    collection = Collection()

    class Client:
        def __init__(self, **kwargs):
            pass

        def get_or_create_collection(self, **kwargs):
            return collection

    monkeypatch.setitem(sys.modules, "chromadb", SimpleNamespace(Client=Client, PersistentClient=Client))
    monkeypatch.setattr(retrieval.RAGAssistant, "_generate", lambda self, system, user: "Bounded transport answer")
    monkeypatch.setenv("PROGRAMSTART_CHROMA_PATH", str(tmp_path / "vectors"))
    assert retrieval.main(["ask", "query", "--method", "hybrid", "--index", str(index)]) == 0
    assert "Bounded transport answer" in capsys.readouterr().out


def test_unknown_retrieval_command_is_rejected_before_source_loading():
    with pytest.raises(SystemExit) as exc:
        retrieval.main(["not-a-command"])
    assert exc.value.code == 2
