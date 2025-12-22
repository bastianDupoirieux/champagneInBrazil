import yaml
from setup.embeddings import appellation_documents
from setup.utils.embeddings import generate_embeddings
from chromadb import EmbeddingFunction, Embeddings, Documents, Client
import os
from dotenv import load_dotenv
import time

load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")

print(os.path.dirname(os.path.abspath(__file__)))
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.yml'), 'r') as stream:
    config = yaml.safe_load(stream)

tokenizer_name = config['tokenizer']
model_name = config['model']
max_tokens = config["max_tokens"]
docs_folder = config["docs_folder"]
hf_timeout = config["hf_timeout"]

class MultilingualEmbeddingsForAppellations(EmbeddingFunction):
    def __call__(self, texts: Documents) -> Embeddings:
        return list(map(lambda doc: generate_embeddings(doc, tokenizer_name, model_name, max_tokens, HF_TOKEN), texts))


def main():
    chroma_client = Client()
    collection = chroma_client.get_or_create_collection(name=config["collection_name"],
                                                        embedding_function = MultilingualEmbeddingsForAppellations())

    docs_dict = appellation_documents.main(docs_folder, max_tokens)

    docs_sublists = [docs_dict["documents"][i:i+1000] for i in range(0, len(docs_dict["documents"]), 1000)]
    docs_ids_sublists = [docs_dict["documents_ids"][i:i+1000] for i in range(0, len(docs_dict["documents_ids"]), 1000)]

    for i in range(0, len(docs_sublists)): #Due to HF free tier, only 1000 requests can be made every 5 minutes.
        # Divide the list into sublists of length 1000 to not run into a timeout error
        docs = docs_sublists[i]
        docs_ids = docs_ids_sublists[i]
        collection.add(documents=docs, ids=docs_ids)
        time.sleep(hf_timeout) # 5 minute break between all documents due to limitation from huggingface free tier

