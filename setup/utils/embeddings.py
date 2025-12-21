import transformers
from transformers import AutoTokenizer, AutoModel
import torch
import torch.nn.functional as F

def get_token_num(inputs:transformers.tokenization_utils_base.BatchEncoding)->int:
    """

    :param inputs:
    :return:
    """
    return len(inputs.encodings[0].ids)

def tokenize_text(text:str, tokenizer_name:str, max_length:int):
    tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)
    inputs = tokenizer(text, return_tensors="pt", max_length=max_length, truncation=False)
    return inputs

def compute_embeddings(tokenized_inputs:transformers.tokenization_utils_base.BatchEncoding, model_name):
    model = AutoModel.from_pretrained(model_name)
    with torch.no_grad():
        outputs = model(**tokenized_inputs) #For now no average poolings
    embeddings = outputs.last_hidden_state
    return embeddings


def generate_embeddings(text:str, tokenizer_name:str, model_name:str, max_length:int):
    inputs = tokenize_text(text, tokenizer_name, max_length)
    embeddings = compute_embeddings(inputs, model_name)

    #normalise embeddings
    embeddings = F.normalize(embeddings, p=2, dim=1)

    return embeddings.numpy().tolist()[0]
