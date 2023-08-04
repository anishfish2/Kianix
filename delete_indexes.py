import pinecone
from vector_db import read_yaml
from dotenv import load_dotenv
import os

def delete_indexes():
    load_dotenv()

    environment = os.getenv("ENVIRONMENT")
    api_key = os.getenv("KEY")


    # Create pinecone index and load
    pinecone.init(api_key=api_key, environment=environment)

    for i in pinecone.list_indexes():
        pinecone.delete_index(i)

if __name__ == '__main__':
    delete_indexes()
    print("All indexes deleted sucessfully!")
