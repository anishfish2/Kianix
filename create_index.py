import pinecone
import sys
from vector_db import wait_on_index, read_yaml
from dotenv import load_dotenv
import os

def init_index(serverName, vector_dim):
    
    print('Creating Index', serverName)
    
    load_dotenv()

    environment = os.getenv("ENVIRONMENT")
    api_key = os.getenv("KEY")

    # Create pinecone index and load
    pinecone.init(api_key=api_key, environment=environment)

    pinecone.create_index(serverName, dimension=vector_dim, metric="cosine")

    print("Indexes after Creation:", pinecone.list_indexes())

    wait_on_index(serverName)

if __name__ == '__main__':

  if len(sys.argv) > 1:
    serverName = sys.argv[1]

    if len(sys.argv) > 2:
      vector_dim = int(sys.argv[2])
    else:
      #Default sent2vec dim
      vector_dim = 768

    init_index(serverName, vector_dim)

  else:
     print("Please provide the server name as the first argument!")

  
  

  