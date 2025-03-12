import sys
import os
from orion_pdf2text import OrionPdf2Text

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now you can import the class from orion_text_chunker
from orion_text_chunker import TextChunker
from orion_rag_chroma_client import OrionChromaDBClient


if __name__ == "__main__":
    # Convert the manuscript to txt using the OrionPdf2Text class
    PATH = "manuscript.pdf"
    converter = OrionPdf2Text(PATH)
    text = converter.convert_to_text()
    if text:
        # Save the wrapped text to a new .txt file
        converter.save_text_to_file("output.txt", text)

        # create chunks of text
        chunker = TextChunker("output.txt")
        chunker.split_into_chunks()
        chunks = chunker.get_chunks()

        client = OrionChromaDBClient("digital_culture")
        client.add_chunks_to_db(chunks)
