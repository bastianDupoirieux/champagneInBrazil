import os
import pandas as pd
import tabula
import pymupdf
import pymupdf4llm
import re

class PdfReader:

    def __init__(self, pdf_path:os.path):
        self.pdf_path = pdf_path

    def read_pdf(self, pdf_contents_type):
        if str.lower(pdf_contents_type) not in ["table", "text"]:
            raise ValueError("Pdf contents type must be 'table' or 'text', given {}".format(pdf_contents_type))

        if pdf_contents_type == "table":
            return self._read_pdf_table()

        if pdf_contents_type == "text":
            return self._read_pdf_document_to_md()
        return None

    def _read_pdf_table(self)->pd.DataFrame:
        """
        Read a PDF file with tables and return a table, combine all tables into a single pd.DataFrame
        :param file_path: the path to the PDF file
        :return: a pd.DataFrame with the table in the PDF file
        """
        table_doc = tabula.read_pdf(self.pdf_path, pages='all')
        table = pd.concat(table_doc)
        return table

    def _read_pdf_document_to_md(self):
        return pymupdf4llm.to_markdown(self.pdf_path)



class MarkdownTextUtils:

    def __init__(self, md_text):
        self.md_text = md_text

    def clean_up_md_text(self) -> str:
        """Remove separators and markdown formatters.
        Must also remove values that should be deleted, i.e. thing between two ~~ [...] ~~ separators"""
        pass

    def get_appellation_title(self) -> str:
        """
        Get the name of the appellation the rulebook applies to.
        Every rulebook of the INAO has the mention: "Cahier des charges de l'appellation d'origine contrôlée « <name_of_the_appellation> »
        :return: the title of the appellation in the text
        """
        pattern = r"Cahier des charges de l[’']appellation d’origine contrôlée.*\s.*«\s*(.*?)\s*»"
        match = re.search(pattern, self.md_text, re.IGNORECASE)
        return match.group(1)

    def extract_toc_from_md(self) -> str:
        """extract the TOC from a certain Markdown text"""
        pass

    def _remove_deleted_text(self) -> str:
        """
        When given a string in Markdown format, remove the deleted entries (i.e. entries found between two ~~ ~~ markers).
        Goes through the string sequentially to find the elements that should be deleted.
        :return:
        """
        pattern = "~~.*?~~"
        text_without_deleted = re.sub(pattern, "", self.md_text)
        return text_without_deleted

    def separate_text_by_titles(self)->list:
        """In case the document contains multiplte rulebooks, separate it into different strings to handle each rulebook separately
        Returns a list of Markdown strings equivalent to a single rulebook
        """
        result = []
        pattern = r"(CAHIER DES CHARGES DE L[’']APPELLATION[\s\S]*?)(?=(?:# CAHIER DES CHARGES DE L[’']APPELLATION|$))"

        matches = re.findall(pattern, text)

        for text in matches:
            result.append(text)

        return result



