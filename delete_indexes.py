import pinecone
import sys
import time
import yaml

if __name__ == '__main__':

    def read_yaml(file_path):
        with open(file_path, "r") as f:
            return yaml.safe_load(f)


    apiInfo = read_yaml("config.yaml")

    environment = apiInfo["API"]["ENVIRONMENT"]
    api_key = apiInfo["API"]["KEY"]


    # Create pinecone index and load
    pinecone.init(api_key=api_key, environment=environment)

    for i in pinecone.list_indexes():
        print("Deleting", i)
        pinecone.delete_index(i)

