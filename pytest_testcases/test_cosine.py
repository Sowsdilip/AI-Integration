from Semantic_Cache.similarity import cosine_similarity
import numpy as np
import pytest

def test_cosine_simlatiry_identical_vectors():
    a=[1.0,0.0]
    b=[1.0,0.0]
   # assert cosine_similarity(a,b) == 1.0
    assert cosine_similarity(a,b) == pytest.approx(1.0)


def test_cosine_similarity_orthogonal_vectors():
    a = [1.0, 0.0]
    b = [0.0 , 1.0]
    assert cosine_similarity(a,b) == 0.0