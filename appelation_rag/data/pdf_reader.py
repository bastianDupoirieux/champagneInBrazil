import os
import pandas as pd
import tabula
import pymupdf
import pymupdf4llm

def read_pdf_table(file_path:os.path)->pd.DataFrame:
    """
    Read a PDF file with tables and return a table, combine all tables into a single pd.DataFrame
    :param file_path: the path to the PDF file
    :return: a pd.DataFrame with the table in the PDF file
    """
    table_doc = tabula.read_pdf(file_path, pages='all')
    table = pd.concat(table_doc)
    return table

def read_pdf_document(pdf_file):
    return pymupdf4llm.to_markdown(pdf_file)
