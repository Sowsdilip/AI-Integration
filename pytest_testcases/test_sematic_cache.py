from Semantic_Cache.semantic_with_fastapi import find_best_match, cache, CacheEntry ,embed_model
from unittest.mock import patch
import numpy as np

def test_find_best_match_returns_none_when_cache_empty():
    cache.clear()
    match, score = find_best_match("any question")
    assert match is None

def test_find_best_match_finds_exact_match():
    cache.clear()
    embedding = [1.0, 0.0, 0.0]
    cache.append(CacheEntry(question="test", answer="test answer", embedding=embedding))
    # we'd need to mock embed_model.encode() to return this same embedding
    # — this is where testing gets trickier, good stopping point for today's intro

def test_find_best_match_with_mocked_embedding():
    cache.clear()
    with patch.object(embed_model, "encode", return_value=np.array([1.0, 0.0, 0.0])):
        cache.append(CacheEntry(question="test", answer="test answer", embedding=[1.0, 0.0, 0.0]))
        match, score = find_best_match("any question")
        print(match.answer)
        assert match is not None
        assert score == 1.0