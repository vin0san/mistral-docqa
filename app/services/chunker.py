from typing import List

class TextChunker:
    """
    Splits text into smaller chunks based on a specified maximum length.

    Design Goals:
    - determine optimal chunk size for processing.
    - testable.
    - framework agnostic.
    """

    def __init__(
            self,
            chunk_size: int = 500,
            overlap_size: int = 50,
    ):
        if overlap_size >= chunk_size:
            raise ValueError("overlap_size must be smaller than chunk_size")
        
        self.chunk_size = chunk_size
        self.overlap_size = overlap_size

    def chunk(self, text: str) -> List[str]:
        """
        Docstring for chunk
        
        :param self: Description
        :param text: Description
        :type text: str
        :return: Description
        :rtype: List[str]
        """
        if not text or not text.strip():
            return []
        
        words = text.split()
        chunks = []
        start = 0
        step = self.chunk_size - self.overlap_size

        while start < len(words):
            end = start +self.chunk_size
            chunk_words= words[start:end]
            chunk_text = " ".join(chunk_words)

            chunks.append(chunk_text)
            start += step

        return chunks