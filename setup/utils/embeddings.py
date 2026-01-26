from chromadb import EmbeddingFunction, Embeddings, Documents
from transformers import AutoTokenizer, AutoModel
import torch
import torch.nn.functional as F
import time


class MultilingualEmbeddingFunction(EmbeddingFunction):
    
    def __init__(self, tokenizer_name: str, model_name: str, max_tokens: int, hf_token: str, batch_size: int, timeout: int):
        """
        Creates a custom embedding function
        :param tokenizer_name: name of the tokenizer
        :param model_name: name of the model
        :param max_tokens: max tokens
        :param hf_token: HF token
        :param batch_size: Max amount of elements per batch
        :param timeout: HF timeout
        """
        self.tokenizer_name = tokenizer_name
        self.model_name = model_name
        self.max_length = max_tokens
        self.hf_token = hf_token
        self.batch_size = batch_size
        self.timeout = timeout
        self._tokenizer = None
        self._model = None
        self._last_request_time = 0
        self._request_counter = 0

    def _load_models(self):
        """
        Loads the tokenizer and model
        :return:
        """
        if self._tokenizer is None:
            self._tokenizer = AutoTokenizer.from_pretrained(self.tokenizer_name, token=self.hf_token)
        if self._model is None:
            self._model = AutoModel.from_pretrained(self.model_name, token=self.hf_token)
            self._model.eval()

    def _check__rate_limit(self):
        """
        Checks the rate limit and ensure HF timeout is not reached
        :return:
        """
        current_time = time.time()
        
        if self._last_request_time + self.timeout < current_time:
            self._last_request_time = current_time
            self._request_counter = 0

        if self._request_counter >= self.batch_size:
            wait_time = self.timeout - (current_time - self._last_request_time)
            print(f"Rate limit reached, waiting for {wait_time} seconds")
            time.sleep(wait_time)
            self._request_counter = 0
            self._last_request_time = time.time()

        self._request_counter += 1

    def __call__(self, texts: Documents) -> Embeddings:
        """
        Calls the tokenizer and model to compute embeddings
        :param texts:
        :return:
        """
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
