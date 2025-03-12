"""
A class to split the content of a text file into chunks of a specified number
of words.

Author: Rodrigo Prestes Machado
"""
from orion_rag_chroma_client import OrionChromaDBClient

class TextChunker:
    """
    A class to split the content of a text file into chunks of a specified
    number of words.

    Attributes:
    -----------
    FILE_PATH : str
        The path to the text file that needs to be split.
    CHUNK_SIZE : int
        The number of words per chunk (default is 500).
    chunks : list
        A list to store the chunks of text.
    """

    def __init__(self, FILE_PATH, CHUNK_SIZE=500):
        """
        Initializes the TextChunker with the file path and chunk size.

        Parameters:
        -----------
        FILE_PATH : str
            The path to the text file.
        CHUNK_SIZE : int
            The number of words per chunk (default is 500).
        """
        self.FILE_PATH = FILE_PATH
        self.CHUNK_SIZE = CHUNK_SIZE
        self.chunks = []

    def split_into_chunks(self):
        """
        Splits the content of the file into chunks of the specified size.

        This method reads the entire content of the file, splits it into
        individual words, and then groups these words into chunks of the
        specified size. Each chunk is stored as a string in the `chunks`
        attribute.
        """
        with open(self.FILE_PATH, 'r', encoding='utf-8') as file:
            content = file.read()

        words = content.split()

        self.chunks = [
            words[i:i + self.CHUNK_SIZE]
            for i in range(0, len(words), self.CHUNK_SIZE)
        ]

        self.chunks = [' '.join(chunk) for chunk in self.chunks]

    def get_chunks(self):
        """
        Returns the list of text chunks.

        Returns:
        --------
        list
            A list of strings, each representing a chunk of the original text.
        """
        return self.chunks


if __name__ == "__main__":

    FILE_PATH = 'merged.txt'
    CHUNK_SIZE = 500

    chunker = TextChunker(FILE_PATH, CHUNK_SIZE)
    chunker.split_into_chunks()
    chunks = chunker.get_chunks()

    print(f"First chunk: {chunks[0]}")
