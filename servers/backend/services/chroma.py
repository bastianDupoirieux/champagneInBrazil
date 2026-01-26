from chromadb import Collection


class RetrieverAugmentor:
    def __init__(self, collection: Collection):
        self.collection = collection

    def query_collection(self, query:str, top_k=3):
        results = self.collection.query(query_texts=[query], n_results=top_k)
        return results
