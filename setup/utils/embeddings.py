from chromadb import EmbeddingFunction, Embeddings, Documents
from transformers import AutoTokenizer, AutoModel
import torch
import torch.nn.functional as F
import time


class MultilingualEmbeddingFunction(EmbeddingFunction):
    
    def __init__(self, tokenizer_name: str, model_name: str, max_length: int, hf_token: str, batch_size: int):
        self.tokenizer_name = tokenizer_name
        self.model_name = model_name
        self.max_length = max_length
        self.hf_token = hf_token
        self.batch_size = batch_size
        self._tokenizer = None
        self._model = None
        self._last_request_time = 0
        self._request_counter = 0

    def _load_models(self):
        if self._tokenizer is None:
            self._tokenizer = AutoTokenizer.from_pretrained(self.tokenizer_name, token=self.hf_token)
        if self._model is None:
            self._model = AutoModel.from_pretrained(self.model_name, token=self.hf_token)
            self._model.eval()

    def _check__rate_limit(self):
        current_time = time.time()
        
        if self._last_request_time + 300 < current_time:
            self._last_request_time = current_time
            self._request_counter = 0

        if self._request_counter >= self.batch_size:
            wait_time = 300 - (current_time - self._last_request_time)
            print(f"Rate limit reached, waiting for {wait_time} seconds")
            time.sleep(wait_time)
            self._request_counter = 0
            self._last_request_time = time.time()

        self._request_counter += 1

    def __call__(self, texts: Documents) -> Embeddings:
        self._load_models()
        embeddings = []

        for text in texts:
            self._check__rate_limit()
            inputs = self._tokenizer(text, return_tensors="pt", max_length=self.max_length, truncation=False)
            with torch.no_grad():
                outputs = self._model(**inputs)
                embedding = outputs.last_hidden_state
                embedding = F.normalize(embedding, p=2, dim=1)
                embeddings.append(embedding.numpy().tolist()[0])
        return embeddings
