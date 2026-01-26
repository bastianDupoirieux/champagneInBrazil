#Prepare the documents to be used in embeddings
import os
from setup.utils import pdf_reader
import uuid

def create_metadata(doc_name:str, appellation:str, section:int, subsection:int)->str:
    """
    Creates metadata based on information
    :param doc_name: name of the document, as pathfile
    :param appellation: appellation name
    :param section: section in the document
    :param subsection: subsesction in the document
    :return: a concatenated string containing metadata
    """
    doc_name = doc_name.replace(" ", "_")[:-4]
    return doc_name + '_' + appellation + '_' + str(section) + '_' + str(subsection)

def split_text(text, max_length) -> list:
    """
    Splits the text into multiple subparts if the text is longer than the allowed max length
    :param text:
    :param max_length:
    :return: a list containing the split text
    """
    i = 0
    split_text_list = []
    while i*max_length < len(text):
        split_text_list.append(text[i*max_length:(i+1)*max_length]) #While the text is too long, add the text as subparts of the max allowed length
        i += 1
    return split_text_list

def create_documents_for_embeddings(pdf_file: os.path, max_text_length:int)->dict:
    """
    Splits the document to prepare it for embeddings.
    Splits the document by section and subsection, and indexes it and gets subsection.
    Returns a dictionary containing the relevant text from each subsection, the indices and the metadata
    :param pdf_file:
    :param max_text_length:
    :return:
    """
    documents = []
    documents_ids = []
    metadata_list = []

    book = pdf_reader.prepare_text_from_pdf_file(pdf_file) #Prepare the text from the pdf file
    appellations_list = list(book.keys()) #Gets all appellations from the prepared rulebook, relevant if multiple appellations within the same book

    for appellation in appellations_list:
        section_counter = 0
        prechunked_rulebook = book[appellation] #The book prechunked into sections and subsections
        for section in prechunked_rulebook: #Takes every element and subelement of the list and prepares it by extending it with ids and metadata
            section_counter += 1
            subsection_counter = 0
            for subsection in section:
                text = appellation + ': ' + subsection
                if len(text) > max_text_length: #In case the element is too long, split it up
                    section.remove(subsection) #if the element is too long, remove ist
                    subtexts = split_text(text, max_text_length-len(appellation))
                    subtexts = [appellation + s for s in subtexts] #Add the information on every appellation to every split up text part
                    section.extend(subtexts)
                    break #Move on to the next subsection

                subsection_counter += 1
                doc_id = uuid.uuid4()
                metadata = create_metadata(pdf_file, appellation, section_counter, subsection_counter)
                documents_ids.append(doc_id)
                documents.append(text)
                metadata_list.append(metadata)

    return {"documents": documents, "documents_ids": documents_ids, "metadata": metadata_list}

def main(docs_folder: os.path, max_text_length:int):
    """
    Prepares the documents for every document in a given folder
    :param docs_folder:
    :param max_text_length:
    :return:
    """
    docs_list = []
    docs_id_list = []
    metadata_list = []
    n_docs = len(os.listdir(docs_folder))
    counter = 1
    for rulebook_file in os.listdir(docs_folder):
        print(f"Adding document {counter}/{n_docs}")
        rulebook = create_documents_for_embeddings(os.path.join(docs_folder, rulebook_file), max_text_length)
        docs_list.extend(rulebook["documents"])
        docs_id_list.extend(rulebook["documents_ids"])
        metadata_list.extend(rulebook["metadata"])
        counter += 1
        
    return {"documents": docs_list, "documents_ids": docs_id_list, "metadata": metadata_list}
