"""
Wrapper class for interacting with ChromaDB collections.

Author: Rodrigo Prestes Machado
"""

import chromadb
from chromadb.config import Settings

class OrionChromaDBClient:
    """
    A class to manage uploading text chunks to a ChromaDB collection and
    searching within that collection.

    Attributes:
    -----------
    collection_name : str
        The name of the ChromaDB collection where the chunks will be stored.
    client : chromadb.Client
        The ChromaDB client instance.
    collection : chromadb.Collection
        The ChromaDB collection instance where the chunks will be added.
    """

    def __init__(self, collection_name, database_path="./database"):
        """
        Initializes the OrionChromaDBClient with the collection name and
        enables persistence.

        Parameters:
        -----------
        collection_name : str
            The name of the ChromaDB collection where the chunks will be stored.
        persist_dir : str
            The directory where the database will be persisted (default: "chroma_db").
        """
        self.collection_name = collection_name
        self.client = chromadb.PersistentClient(path=database_path)
        self.collection = self._get_or_create_collection(collection_name)

    def _get_or_create_collection(self, collection_name):
        """
        Gets an existing collection or creates a new one if it doesn't exist.

        Parameters:
        -----------
        collection_name : str
            The name of the ChromaDB collection.

        Returns:
        --------
        chromadb.Collection
            The ChromaDB collection instance.
        """
        existing_collections = self.client.list_collections()
        collection_names = [col.name for col in existing_collections]
        if self.collection_name in collection_names:
            print(f"Opening existing collection: {self.collection_name}")
            return self.client.get_collection(self.collection_name)
        else:
            print(f"Creating new collection: {self.collection_name}")
            return self.client.create_collection(self.collection_name)

    def add_chunks_to_db(self, chunks):
        """
        Adds the list of text chunks to the ChromaDB collection.

        Parameters:
        -----------
        chunks : list
            A list of text chunks (strings) to be added to the collection.
        """
        for i, chunk in enumerate(chunks):
            print(f"Adding chunk {i}")
            self.collection.add(
                ids=[f"chunk_{i}"],
                documents=[chunk]
            )

    def search(self, query_text, n_results=5):
        """
        Searches the ChromaDB collection for documents matching the query.

        Parameters:
        -----------
        query_text : str
            The text to search for within the collection.
        n_results : int
            The number of top matching results to return (default is 5).

        Returns:
        --------
        list
            A list of dictionaries containing the search results.
        """
        results = self.collection.query(
            query_texts=[query_text],
            n_results=n_results,
        )
        return results

    def search_all(self):
        """
        Searches the ChromaDB collection for all documents matching the query.

        Returns:
        --------
        list
            A list of dictionaries containing all search results.
        """
        results = self.collection.get()
        return results

    def get_collection(self):
        """
        Returns the ChromaDB collection instance.

        Returns:
        --------
        chromadb.Collection
            The ChromaDB collection instance.
        """
        return self.collection


if __name__ == "__main__":
    # Example usage

    # List of text chunks (these would typically come from your TextChunker)
    chunks = [
        "apple",
        "banana",
        "cherry",
        "computer",
    ]

    # Specify the ChromaDB collection name
    collection_name = "my_text_collection"

    # Create an instance of the OrionChromaDBClient class
    client = OrionChromaDBClient(collection_name)

    # Add the chunks to the ChromaDB collection
    client.add_chunks_to_db(chunks)

    # Search for a term in the collection
    search_results = client.search("notebook")
    print(f"Search results: {search_results}")
