# Add the parent directory to sys.path
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from orion_rag_chroma_client import OrionChromaDBClient

if __name__ == "__main__":
    # Specify the ChromaDB collection name
    collection_name = "digital_culture"

    # Create an instance of the OrionChromaDBClient class
    client = OrionChromaDBClient(collection_name)

    # Search for a term in the collection
    search_results = client.search("competências digitais")
    #print(f"Search results: {search_results}")

    print(search_results["ids"][0][0])
    print(search_results["distances"][0][0])
    print(search_results["documents"][0][0])

    print("-------------------")

    print(search_results["ids"][0][1])
    print(search_results["distances"][0][1])
    print(search_results["documents"][0][1])

    print("-------------------")

    print(search_results["ids"][0][2])
    print(search_results["distances"][0][2])
    print(search_results["documents"][0][2])