from unittest.mock import patch

def test_find_best_match_with_mocked_embedding():
    cache.clear()
    with patch.object(embed_model, "encode", return_value=np.array([1.0, 0.0, 0.0])):
        cache.append(CacheEntry(question="test", answer="test answer", embedding=[1.0, 0.0, 0.0]))
        match, score = find_best_match("any question")
        assert match is not None
        assert score == 1.0