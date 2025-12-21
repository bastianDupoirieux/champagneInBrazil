#Prepare the documents to be used in embeddings
import os
from setup.utils import pdf_reader

def create_id(doc_name:str, appellation:str, section:int, subsection:int)->str:
    doc_name = doc_name.replace(" ", "_")[:-4]
    return doc_name + '_' + appellation + '_' + str(section) + '_' + str(subsection)

def split_text(text, max_length) -> list:
    i = 0
    split_text_list = []
    while i*max_length < len(text):
        split_text_list.append(text[i*max_length:(i+1)*max_length])

    return split_text_list

def create_documents_for_embeddings(pdf_file: os.path, max_text_length:int)->dict:
    documents = []
    documents_ids = []

    book = pdf_reader.prepare_text_from_pdf_file(pdf_file)
    appellations_list = list(book.keys())

    for appellation in appellations_list:
        section_counter = 0
        prechunked_rulebook = book[appellation]
        for section in prechunked_rulebook:
            section_counter += 1
            subsection_counter = 0
            for subsection in section:
                text = appellation + ': ' + subsection
                if len(text) > max_text_length:
                    section.remove(subsection) #if the element is too long, remove ist
                    subtexts = split_text(text, max_text_length-len(appellation))
                    subtexts = appellation + subtexts
                    section.extend(subtexts)

                subsection_counter += 1
                doc_id = create_id(pdf_file, appellation, section_counter, subsection_counter)
                documents_ids.append(doc_id)
                documents.append(text)

    return {"documents": documents, "documents_ids": documents_ids}

def main(docs_folder: os.path, max_text_length:int):
    docs_list = []
    docs_id_list = []
    counter = 0
    for rulebook_file in os.listdir(docs_folder):
        if counter < 3:
            rulebook = create_documents_for_embeddings(os.path.join(docs_folder, rulebook_file), max_text_length)
            docs_list.extend(rulebook["documents"])
            docs_id_list.extend(rulebook["documents_ids"])
            counter += 1

    return {"documents": docs_list, "documents_ids": docs_id_list}
