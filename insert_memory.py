import pinecone
import sys
from vector_db import insert_memories, read_yaml

def insert_memory(serverName, memories):

    apiInfo = read_yaml("config.yaml")

    environment = apiInfo["API"]["ENVIRONMENT"]
    api_key = apiInfo["API"]["KEY"]

    pinecone.init(api_key=api_key, environment=environment)

    if serverName not in pinecone.list_indexes():
        print("Server name does not exist")

    else:

        index = pinecone.Index(serverName)

        insert_memories(memories, index)


if __name__ == '__main__':
    if len(sys.argv) > 1:

        serverName = sys.argv[1]

        if len(sys.argv) > 2:

            memories = [i for i in sys.argv[2].split(".") if len(i) > 0]

            insert_memory(serverName, memories)

            print("Memory successfully uploaded!")
            
        else:
            print("Please provide the memory content as the second argument!")
            
    else:
        print("Please provide the server name as the first argument!")
    

    