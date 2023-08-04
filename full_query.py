import pinecone
import sys
from vector_db import query_memories, read_yaml
from dotenv import load_dotenv
import os

def full_query(serverName, memories, top_k):

    load_dotenv()

    environment = os.getenv("ENVIRONMENT")
    api_key = os.getenv("KEY")


    # Create pinecone index and load
    pinecone.init(api_key=api_key, environment=environment)

    if serverName not in pinecone.list_indexes():
        print("Server name does not exist")

    else:
        index = pinecone.Index(serverName)

        return query_memories(memories, index, top_k)

if __name__ == '__main__':
    
    if len(sys.argv) > 1:
        serverName = sys.argv[1]

        if len(sys.argv) > 2:
            memories = [i for i in sys.argv[2].split("?") if len(i) > 0]

            if len(sys.argv) > 3:
                top_k = int(sys.argv[3])

                print(full_query(serverName, memories, top_k))

            else:
                print("Please provide the top_k value as the third argument!")

        else:
            print("Please provide the memory content as the second argument!")  

    else:
        print("Please provide the server name as the first argument!")

    

    