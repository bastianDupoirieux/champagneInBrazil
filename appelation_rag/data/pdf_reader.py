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

    def separate_multiple_books_by_title(self, doc)-> list:
        """
        In the case of appellation rulebooks, there can be multiple books within one pdf document.
        Separates these rulebooks and returns each as a single element of a list
        :param doc: the text from a pdf document
        :return: a list containing each separate rulebook from a pdf document
        """
        result = []
        # Regex pattern to match each complete document section
        pattern = (r"(Cahier des charges de l[’']appellation d[’']origine contrôlée"  # header line
                    r"(?:.*?«.*?»)?"               # same-line appellation (optional)
                    r"(?:\s*«.*?»)?"               # next-line appellation (optional)
                    r"[\s\S]*?)"                   # capture body text
                    r"(?=(?:Cahier des charges de l[’']appellation d[’']origine contrôlée|$))"
                    )

        matches = re.findall(pattern, doc)

        for text in matches:
            result.append(text)

        return result


class MarkdownTextUtils:

    def __init__(self, md_text):
        self.md_text = md_text
        self.hierarchy = [ "Chapter", "Section", "Subsection"]
        self.regex_map = {"Chapter": r"CHAPITRE\s+[IVXLCDM]+(?:\s*\[[^\]]+\])?",
                          "Section": re.compile(r"^\*\*\s*([IVXLCDM]+)\s*-\s*(.*)$"),
                          "Subsection": re.compile(r"^_([0-9]+)°-\s*(.*)$")}


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

    def _get_chapters_from_doc(self):
        """
        Extracts the chapters from the documents
        :return:
        """
        pattern = self.regex_map["Chapter"]
        chapters = re.split(pattern, self.md_text)

        return chapters[1:] #the first element is what comes before the first chapter, aka nothing of value

