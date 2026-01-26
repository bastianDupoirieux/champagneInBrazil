import os
import pandas as pd
import tabula
import pymupdf4llm
import re


def prepare_text_from_pdf_file(file:os.path)->dict: #This function might not be at the right place here
    """
    Prepares a PDF file by combining all functions from the classes to be ready for tokenizing
    :param file:
    :return:
    """
    print(f"reading file {file}")
    pdf_reader = PdfReader(file)
    doc = pdf_reader.read_pdf("text")
    books = pdf_reader.separate_multiple_books_by_title(doc)

    if len(books) == 0: #Problem with the title, the books can't be separated. Consider it one giant rulebook
        books = [doc]

    result_dict = {}

    for book in books:
        rulebook_utils = RulebookUtils(book)
        try:
            title = rulebook_utils.get_appellation_title()

        except: #If the title can't be read
            print(f"Title from book {book[:200]} in file {file} could not be read, please input manually")
            title = input("Title from book: ").upper()

        print(f"Preparing data for appellation {title}")

        if title not in result_dict.keys():
            split_book = rulebook_utils.doc_split()
            result_dict[title] = split_book
            print(f"Added {title} to result")
        else:
            print("passed, appellation already in dictionary")
            pass
    print(f"Finished preparing document for appellation {file}")
    return result_dict


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



class MarkdownUtils:

    def __init__(self, md_text):
        self.md_text = md_text

    def _remove_deleted_text(self) -> str:
        """
        When given a string in Markdown format, remove the deleted entries (i.e. entries found between two ~~ ~~ markers).
        Goes through the string sequentially to find the elements that should be deleted.
        :return:
        """
        pattern = "~~.*?~~"
        text_without_deleted = re.sub(pattern, "", self.md_text)
        return text_without_deleted

    def clean_up_md_text(self) -> str:
        """
        Remove separators and markdown formatters.
        """
        text = self._remove_deleted_text()
        text = text.replace("\n", " ")
        text = text.replace("**", "")
        text = text.replace("_", "")  # replace italics

        return text


class RulebookUtils:

    def __init__(self, rulebook_text):
        self.rulebook_text = rulebook_text
        self.hierarchy = ["Section", "Subsection"]
        self.regex_map = {"Section": r"(?m)(?=^\s*\*\*\s*[IVXLCDM]+\s*.*?-.*?\*\*\s*(?:\r?\n\s*)*)",
                          "Subsection": re.compile(r"(?m)(?=^[ \t]*_?\d+(?:°|º)\s*-\s*)")}


    def get_appellation_title(self) -> str:
        """
        Get the name of the appellation the rulebook applies to.
        Every rulebook of the INAO has the mention: "Cahier des charges de l'appellation d'origine contrôlée « <name_of_the_appellation> »
        :return: the title of the appellation in the text
        """
        pattern = r"Cahier des charges de l[’']appellation d’origine contrôlée(?:\s*\*\*)?\s*(?:.*\s*)?«\s*(.*?)\s*»"
        match = re.search(pattern, self.rulebook_text, re.IGNORECASE)
        return match.group(1)



    def _split_text_by_hierarchy(self) -> list:
        """
        Splits a document into different sections and subsections.
        Returns a nested array containing the subsections of each section
        :return:
        """
        section_pattern = self.regex_map["Section"]
        subsection_pattern = self.regex_map["Subsection"]

        sections = re.split(section_pattern, self.rulebook_text)
        for i in range(0, len(sections)):
            section = sections[i]
            section_split_by_subsection = re.split(subsection_pattern, section)
            sections[i] = section_split_by_subsection

        return sections

    def doc_split(self):
        """

        :return:
        """
        cleaned_sections = []
        sections = self._split_text_by_hierarchy()

        for section in sections:
            # Clean each subsection and keep only if length > 1
            cleaned_subsections = []
            for subsection in section:
                md_utils = MarkdownUtils(subsection)
                cleaned_text = md_utils.clean_up_md_text()
                if len(cleaned_text) > 1:  # keep only if length > 1
                    cleaned_subsections.append(cleaned_text)

            # Keep the section only if it has any non-empty subsections
            if cleaned_subsections:
                cleaned_sections.append(cleaned_subsections)

        #sections = cleaned_sections

        return cleaned_sections