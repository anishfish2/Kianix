import pinecone
from vector_db import read_yaml

def delete_indexes():
    apiInfo = read_yaml("config.yaml")

    environment = apiInfo["API"]["ENVIRONMENT"]
    api_key = apiInfo["API"]["KEY"]


    # Create pinecone index and load
    pinecone.init(api_key=api_key, environment=environment)

    for i in pinecone.list_indexes():
        pinecone.delete_index(i)

if __name__ == '__main__':
    delete_indexes()
    print("All indexes deleted sucessfully!")
