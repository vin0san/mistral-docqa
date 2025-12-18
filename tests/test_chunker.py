import pytest
from app.services.chunker import TextChunker as Chunker

def test_empty_text():
    chunker  = Chunker()
    assert chunker.chunk("") == []

def test_single_chunk():
    text = "This is a test."
    chunker = Chunker(chunk_size=10, overlap_size=2)

    chunks = chunker.chunk(text)
    assert len(chunks) == 1
    assert chunks[0] == text

def test_overlap_behavior():
    text = " ".join([f"word{i}" for i in range(20)])

    chunker = Chunker(chunk_size=10, overlap_size=2)
    chunks = chunker.chunk(text)

    assert len(chunks) > 1

    first = chunks[0].split()
    second = chunks[1].split()

    # Check for overlap
    assert first[-2:] == second[:2]

def test_invalid_overlap():
    with pytest.raises(ValueError):
        Chunker(chunk_size=10, overlap_size=10)
