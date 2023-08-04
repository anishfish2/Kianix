import pinecone
import sys
import yaml
from create_index import init_index
from dotenv import load_dotenv
import os

def resetIndex(serverName):
    load_dotenv()

    environment = os.getenv("ENVIRONMENT")
    api_key = os.getenv("KEY")


    # Create pinecone index and load
    pinecone.init(api_key=api_key, environment=environment)

    pinecone.delete_index(serverName)

    init_index(serverName, 768)

if __name__ == '__main__':
    if len(sys.argv) > 1:

        serverName = sys.argv[1]

        resetIndex(serverName)

    else:
        print("Please provide the server name as the first arguement!")