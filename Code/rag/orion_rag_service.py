"""
A simple Flask API service that interacts with the ChromaDB client to
process queries and return results.

The service listens on the '/query' endpoint for POST requests containing a
JSON payload with a 'query' field. The service processes the query using the
ChromaDB client and returns the result as a JSON response.

Author: Rodrigo Prestes Machado
"""

import logging
from flask_cors import CORS
from flask import Flask, request, jsonify, abort
from orion_rag_chroma_client import OrionChromaDBClient

# The name of the collection to interact with in the ChromaDB
COLLECTION_NAME = "python_collection"


class OrionRAGService:
    """
    A simple Flask API service that interacts with the ChromaDB client to
    process queries and return results.
    """

    def __init__(self, host='0.0.0.0', port=3030):
        """
        Initializes the OrionRAGService with Flask app, ChromaDB client, and
        basic configurations for logging and CORS.

        Args:
            host (str): The host IP where the service will run. Defaults to
                    '0.0.0.0' to allow access from any network.
            port (int): The port on which the service will listen. Defaults
                    to 3030.
        """
        # Initialize the Flask app
        self.app = Flask(__name__)

        # Enable CORS (Cross-Origin Resource Sharing)
        CORS(self.app)

        # Initialize the ChromaDB client with the specified collection
        self.client = OrionChromaDBClient(COLLECTION_NAME)

        # Store the host and port
        self.host = host
        self.port = port

        # Setup logging to a file with INFO level
        logging.basicConfig(filename='chroma-service.log', level=logging.INFO)

        # Set up the API routes
        self.setup_routes()

    def setup_routes(self):
        """
        Defines the routes for the Flask app, specifically the '/query'
        endpoint which handles POST requests to interact with the ChromaDB
        client.
        """

        @self.app.route('/query', methods=['POST'])
        def query():
            """
            Handles POST requests to the '/query' endpoint. Expects a JSON
            payload with a 'query' field. Processes the query using the
            ChromaDB client and returns the result as JSON.

            Example Input:
              {
                "query": "your query string or object here"
              }

            Returns:
                Response: JSON response containing the query results or an
                        error message.
            """
            # Parse JSON request data
            data = request.json
            if not data or 'query' not in data:
                # Return a 400 error if 'query' parameter is missing
                abort(400, 'Bad Request: A query parameter is required.')

            # Log the received query
            logging.info('Received query: %s', data['query'])

            # Process the query using the ChromaDB client
            result = self.client.search(data['query'])

            # Apply a threshold filter to the results and return as JSON
            return jsonify(self.threshold_filter(result))

    def threshold_filter(self, result, threshold=1):
        """
        Filters the results from the ChromaDB client based on a distance
        threshold.

        Args:
            result (dict): The result dictionary returned by the ChromaDB
                    client, containing 'documents' and 'distances'.
            threshold (float): The distance threshold for filtering documents.
                    Only documents with a distance less than this value are
                    included in the result. Defaults to 1.

        Returns:
            list: A list of filtered documents that meet the distance
                  threshold criteria.
        """
        # Initialize an empty list for filtered documents
        filtered_documents = []

        # Extract documents and distances from the result
        ids = result.get('ids', [])[0]
        documents = result.get('documents', [])[0]
        distances = result.get('distances', [])[0]

        # Iterate over distances and filter based on the threshold
        for i, distance in enumerate(distances):
            if distance < threshold:
                filtered_documents.append(
                    {'id': ids[i], 'distance': distance, 'document': documents[i]})
        return filtered_documents

    def run(self):
        """
        Starts the Flask application, making the service available on the
        specified host and port. Also logs and prints a message indicating
        the URL where the service is running.
        """
        # Construct the service URL
        url = f"http://{self.host}:{self.port}"
        # Log the service start message
        logging.info("ChromaDB service is running at %s", url)
        # Print the service start message to the console
        print(f"ChromaDB service is running at {url}")
        # Start the Flask app
        self.app.run(host=self.host, port=self.port)


if __name__ == "__main__":
    # Create an instance of OrionRAGService and run it
    service = OrionRAGService("127.0.0.1")
    service.run()
