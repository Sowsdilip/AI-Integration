import numpy as np
import pytest
from unittest.mock import patch

from Semantic_Cache.semantic_with_fastapi import (
    find_best_match,
    cache,
    CacheEntry,
    embed_model,
)


@pytest.fixture(autouse=True)
def clean_cache():
    cache.clear()      # runs before each test
    yield
    cache.clear()      # runs after each test, even if it failed


@pytest.fixture
def fake_encode():
    """Replace the real model with a fake that returns whatever vector we choose."""
    with patch.object(embed_model, "encode") as mock:
        yield mock


def test_returns_none_when_cache_empty():
    match, score = find_best_match("any question")
    assert match is None


def test_finds_exact_match(fake_encode):
    fake_encode.return_value = np.array([1.0, 0.0, 0.0])
    cache.append(CacheEntry(question="test", answer="test answer",
                            embedding=[1.0, 0.0, 0.0]))

    match, score = find_best_match("any question")

    assert match is not None            # assert first, then use match
    assert match.answer == "test answer"
    assert score == pytest.approx(1.0)  # tolerant float comparison
    fake_encode.assert_called_once()    # proves the mock was actually used


def test_dissimilar_question_scores_low(fake_encode):
    fake_encode.return_value = np.array([0.0, 1.0, 0.0])   # orthogonal to cached vector
    cache.append(CacheEntry(question="test", answer="test answer",
                            embedding=[1.0, 0.0, 0.0]))

    match, score = find_best_match("totally different")

    assert score == pytest.approx(0.0)   # adjust if your code returns None/threshold differently


def test_picks_best_of_several_entries(fake_encode):
    fake_encode.return_value = np.array([1.0, 0.1, 0.0])
    cache.append(CacheEntry(question="a", answer="far",  embedding=[0.0, 1.0, 0.0]))
    cache.append(CacheEntry(question="b", answer="near", embedding=[1.0, 0.0, 0.0]))

    match, score = find_best_match("query")

    assert match.answer == "near"