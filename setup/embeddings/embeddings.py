import yaml
from setup.embeddings import appellation_documents
from setup.utils.embeddings import generate_embeddings
from chromadb import EmbeddingFunction, Embeddings, Documents, Client
import os

print(os.path.dirname(os.path.abspath(__file__)))
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.yml'), 'r') as stream:
    config = yaml.safe_load(stream)

tokenizer_name = config['tokenizer']
model_name = config['model']
max_tokens = config["max_tokens"]
docs_folder = config["docs_folder"]

class MultilingualEmbeddingsForAppellations(EmbeddingFunction):
    def __call__(self, texts: Documents) -> Embeddings:
        return list(map(lambda doc: generate_embeddings(doc, tokenizer_name, model_name, max_tokens), texts))


def main():
    chroma_client = Client()
    collection = chroma_client.get_or_create_collection(name=config["collection_name"],
                                                        embedding_function = MultilingualEmbeddingsForAppellations())

    docs_dict = appellation_documents.main(docs_folder, max_tokens)

    collection.add(documents = docs_dict["documents"], ids = docs_dict["documents_ids"])

