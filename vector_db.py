import pinecone
import yaml
import os
import sys
import nltk
#Only uncomment if punkt has not already been downloaded
#nltk.download('punkt')
from sent2vec.vectorizer import Vectorizer
from dotenv import load_dotenv
import os

from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim

def wait_on_index(serverName):
  ready = False

  while not ready:
    try:
      desc = pinecone.describe_index(serverName)
      if desc[7]['ready']:
        return True
      
    except pinecone.core.client.exceptions.NotFoundException:
      pass

#Take in a list of sentences -> Return a list of vectors w dim 768
def vectorize(sentences):

    model = SentenceTransformer('thenlper/gte-large')
    embeddings = model.encode(sentences)

    # vectorizer = Vectorizer()
    # vectorizer.run(sentences)
    # vectors = vectorizer.vectors
    return embeddings

def insert_memories(sentences, index):
    if len(sentences) > 0:
        vectorized_sentences = vectorize(sentences)
        formated_sentences = [(sentences[i], vectorized_sentences[i].tolist()) for i in range(len(vectorized_sentences))]
        index.upsert(formated_sentences)

def query_memories(questions, index, num_memories):
    vectorized_questions = vectorize(questions)
    answers = []
    score = 0
    for i in range(len(questions)):
        q = index.query(
            vector=vectorized_questions[i].tolist(),
            top_k=num_memories,
            include_values=True
        ).matches[0]
        answers.append(q.id)
        score += q.score
    score = score / len(questions)
    return (answers, score)

def read_yaml(file_path):
        with open(file_path, "r") as f:
            return yaml.safe_load(f)


def test_functions(serverName):
    load_dotenv()

    environment = os.getenv("ENVIRONMENT")
    api_key = os.getenv("KEY")


    # Create pinecone index and load
    pinecone.init(api_key=api_key, environment=environment)

    if len(pinecone.list_indexes()) == 0:
        os.system("python init_index.py " + serverName + " 768")

    if serverName not in pinecone.list_indexes():
        for i in pinecone.list_indexes():
            pinecone.delete_index(i)
        os.system("python init_index.py " + serverName + " 768")
    
    index = pinecone.Index(serverName)

    print('Enter Memory:')
    sentences = [i for i in input().split(".") if len(i) > 0]

    insert_memories(sentences, index)

    wait_on_index(serverName)

    questions = [i for i in input('What would you like to ask?').split("?") if len(i) > 0]

    print(query_memories(questions, index, 1)[0])

if __name__ == '__main__':
    if len(sys.argv > 1):
        serverName = sys.argv[1]

        test_functions(serverName)