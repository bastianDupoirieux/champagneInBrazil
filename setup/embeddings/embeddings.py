import yaml
from setup.embeddings import appellation_documents
from setup.utils.embeddings import MultilingualEmbeddingFunction
from chromadb import PersistentClient
import os
from dotenv import load_dotenv

load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")
CHROMA_DB_DIR = os.getenv("CHROMA_DB_DIRECTORY")

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../config.yml'), 'r') as stream:
    config = yaml.safe_load(stream)

tokenizer_name = config['tokenizer']
model_name = config['model']
max_tokens = config["max_tokens"]
docs_folder = config["docs_folder"]
hf_timeout = config["hf_timeout"]
batch_size = config["BATCH_SIZE"]



def main():
    chroma_client = PersistentClient(CHROMA_DB_DIR)
    collection = chroma_client.get_or_create_collection(name=config["collection_name"],
                                                        embedding_function = MultilingualEmbeddingFunction(tokenizer_name, model_name, max_tokens, HF_TOKEN, batch_size, hf_timeout))

    docs_dict = appellation_documents.main(docs_folder, max_tokens)


    total_docs = len(docs_dict["documents"])
    total_batches = total_docs // batch_size

    for batch_idx in range(total_batches):
        print(f"Adding batch {batch_idx+1}/{total_batches}")
        start_idx = batch_idx * batch_size
        end_idx = min(start_idx + batch_size, total_docs)
        docs = docs_dict["documents"][start_idx:end_idx]
        docs_ids = docs_dict["documents_ids"][start_idx:end_idx]
        metadata = docs_dict["metadata"][start_idx:end_idx]

        try:
            collection.add(documents=docs, ids=docs_ids, metadatas = metadata)
        except Exception as e:
            print(f"Error adding documents: {e}")


if __name__ == "__main__":
    main()
