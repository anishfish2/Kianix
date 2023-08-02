import pinecone
import sys
import yaml
from create_index import init_index

def resetIndex(serverName):

    def read_yaml(file_path):
        with open(file_path, "r") as f:
            return yaml.safe_load(f)


    apiInfo = read_yaml("config.yaml")

    environment = apiInfo["API"]["ENVIRONMENT"]
    api_key = apiInfo["API"]["KEY"]


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