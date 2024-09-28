import sys
if "../" not in sys.path:
    sys.path.append("../")

import PyPDF2
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from initialize_gemini import initialize_gemini 
import os

class GetBooksInfo:
    """
    get information about books we have to embed in the router agent that decides which to RAG or search_web ...etc
    """
    def __init__(self, books_dir_path="books", api_path="config/api4.yaml"):
        self.summaries = ""
        self.books_dir_path = books_dir_path
        files = os.listdir(self.books_dir_path)
        for file in files:
            if file.endswith('.pdf'):
                pdf_path = os.path.join(self.books_dir_path, file)
                title_and_summary_dict = self._get_title_and_summary(pdf_path,api_path=api_path)
                self.summaries = "\n" + str(title_and_summary_dict)
                
    @property   
    def get_books_summary(self):
        return self.summaries 
    
    def _get_title_and_summary(self, pdf_path, api_path):
        """Extracts the title and summary from the first 20 pages of a PDF.
        Args:
            pdf_path: The path to the PDF file.
        Returns:
            A tuple containing the title and summary, or None if they cannot be extracted.
        """

        try:
            with open(pdf_path, 'rb') as pdf_file:
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                    # Initialize an empty string for the summary
                text = ''

                # Extract text from the first 20 pages
                for page_num in range(min(20, len(pdf_reader.pages))):
                    page = pdf_reader.pages[page_num]
                    t = page.extract_text()
                    text += t
        except Exception as e:
            print(f"Error Opening the file with the following exception: {e}")
            return {}
        
        prompt = PromptTemplate(
            template="""
                You will be given the first pages content of a book and your rule is to return a json with
                the following keys ["Title"(which is the title of the book), "summary"(which is the 300-word summary about the book)]
                Be informative in your summary and coincise.
                here is the content given to you: {text}
                Remember to output a json.
                """,
            input_variables=['text'])

        model = initialize_gemini(api_path)
        title_and_summary_chain = prompt | model | JsonOutputParser()
        title_and_summary_dict = title_and_summary_chain.invoke(text)
        return title_and_summary_dict

if __name__ == '__main__':
    object = GetBooksInfo()
    summaries = object.get_books_summary
    with open('book_summaries_for_Agent.txt', 'w') as f:
        f.write(summaries.strip())
