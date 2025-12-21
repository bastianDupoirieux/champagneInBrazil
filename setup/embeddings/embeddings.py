from setup.data.pdf_reader import prepare_text_from_pdf_file
from transformers import AutoTokenizer, AutoModel
import os
import utils

#Entrypoint: a dictionary per appellation containing the different elements from the rulebook
# For every appellation, I want to tokenise and chunk the document before calculating vector embeddings
# Step 1. Tokenise text
# Step 2. Rechunk the text if necessary (aka more than the token limit set)
# Step 3. Calculate the embeddings

def embeddings_entrypoint(appellation_dict:dict, tokenizer:str, max_length:int): #This function might not be at the right place here
    """

    :param max_length:
    :param appellation_dict:
    :param tokenizer:
    :return:
    """
    embeddings_dict = {}
    for appellation in appellation_dict.keys():
        if appellation not in embeddings_dict.keys():
            prechunked_rulebook = appellation_dict[appellation]
            for section in prechunked_rulebook:
                for subsection in section:
                    text = appellation + subsection
                    if len(text) > max_length:
                        rechunked_text = embeddings_utils.rechunk_text()
                    embeddings_utils = EmbeddingsUtils(text, max_length)
                    tokenised_text = embeddings_utils.tokenise_text(tokenizer)
                    embeddings = embeddings_utils.compute_embeddings()
            embeddings_dict[appellation] = embeddings
        else:
            pass
    return embeddings_dict



class EmbeddingsUtils:

    def __init__(self, text: str, max_length: int):
        self.text = text
        self.max_length = max_length

    def tokenise_text(self, tokeniser):
        pass

    def rechunk_text(self) -> list:
        """
        Takes the text and returns a list of maximum length substrings
        :return: a list of maximum length substrings
        """
        list_substr = []
        while len(self.text) > 0:
            list_substr.append(self.text[:self.max_length])

        return list_substr

    def compute_embeddings(self):
        pass
