import transformers
from transformers import AutoTokenizer, AutoModel

def get_token_num(inputs:transformers.tokenization_utils_base.BatchEncoding)->int:
    """

    :param inputs:
    :return:
    """
    return len(inputs.encodings[0].ids)

def tokenize_text(text:str, tokenizer_name):
    tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)
    inputs = tokenizer(text, return_tensors="pt")
    return inputs

def embeddings(tokenized_inputs:transformers.tokenization_utils_base.BatchEncoding, model_name):
    model = AutoModel.from_pretrained(model_name)
    outputs = model(**tokenized_inputs)
    return outputs

def split_text(text, max_length) -> list:
    i = 0
    split_text_list = []
    while i*max_length < len(text):
        split_text_list.append(text[i*max_length:(i+1)*max_length])

    return split_text_list

