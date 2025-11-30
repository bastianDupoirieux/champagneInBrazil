from appelation_rag.data.pdf_reader import prepare_text_from_pdf_file
from transformers import AutoTokenizer
import os

#Entrypoint: a dictionary per appellation containing the different elements from the rulebook
# For every appellation, I want to tokenise and chunk the document before calculating vector embeddings
# Step 1. Tokenise text
# Step 2. Rechunk the text if necessary (aka more than the token limit set)
# Step 3. Calculate the embeddings

def embeddings_entrypoint(appellation_dict:dict, tokenizer:str, max_tokens:int): #This function might not be at the right place here
    """

    :param appellation_dict:
    :param tokenizer:
    :return:
    """
    embeddings_dict = {}
    for appellation in appellation_dict.keys():
        if appellation not in appellation_dict.keys():
            prechunked_rulebook = appellation_dict[appellation]
            for section in prechunked_rulebook:
                for subsection in section:
                    text = appellation + subsection
                    embeddings_utils = EmbeddingsUtils(text)
                    tokenised_text = embeddings_utils.tokenise_text(tokenizer)
                    if len(tokenised_text) > max_tokens:
                        rechunked_text = embeddings_utils.rechunk_text()
                    else:
                        pass
                    embeddings = embeddings_utils.compute_embeddings()
            embeddings_dict[appellation] = embeddings
        else:
            pass
    return embeddings_dict



class EmbeddingsUtils:

    def __init__(self, text, max_tokens):
        self.text = text
        self.max_tokens = max_tokens

    def tokenise_text(self, tokeniser):
        pass

    def rechunk_text(self):
        pass

    def compute_embeddings(self):
        pass
