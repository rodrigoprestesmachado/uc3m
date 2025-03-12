"""
This script demonstrates how to use the Orion tools to merge text files, chunk
them, store the chunks in a ChromaDB collection.

Modules:
    orion_text_merger: Used for merging multiple text files into a single file.
    orion_text_chunker: Handles splitting a text file into smaller chunks.

Global Variables:
    DOCUMENTATION (str): Directory containing text files to be merged.
    FILE_NAME (str): Name of the merged output text file.
    COLLECTION_NAME (str): Name of the ChromaDB collection.
    CHUNK_SIZE (int): Maximum size of each chunk.

Functions:
    merger_text_files(): Merges all text files in the DOCUMENTATION directory
    	into a single file.
    create_database(): Splits the merged file into chunks and stores them in
    	the ChromaDB collection.
"""

from orion_text_merger import TextMerger
from orion_text_chunker import TextChunker
from orion_rag_chroma_client import OrionChromaDBClient

DOCUMENTATION = '/Users/rodrigo/Downloads/documentation/'
FILE_NAME = 'merged.txt'
COLLECTION_NAME = "python_collection"
CHUNK_SIZE = 500

def merger_text_files():
    """Merges text files from the DOCUMENTATION directory into a single file."""
    TextMerger(DOCUMENTATION, FILE_NAME).merge_files()

def create_database():
    """
    Splits the merged text file into chunks and stores them in the ChromaDB
    collection.
    """
    chunker = TextChunker(FILE_NAME, CHUNK_SIZE)
    chunker.split_into_chunks()
    chunks = chunker.get_chunks()
    print(f'Number of chunks: {len(chunks)}')

    client = OrionChromaDBClient(COLLECTION_NAME)
    client.add_chunks_to_db(chunks)

if __name__ == "__main__":
    # Uncomment the following lines to merge files and create the database
    # merger_text_files()
    create_database()
