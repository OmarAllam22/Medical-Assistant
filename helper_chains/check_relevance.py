import sys
if "../" not in sys.path:
    sys.path.append("../")

from utils.initialize_gemini import initialize_gemini
from utils.prepare_retriever import prepare_retriever

from langchain_core.output_parsers import JsonOutputParser

from prompts.check_docs_relevance_prompt import check_docs_relevance_prompt

class relevance_chain:
    def __call__(self, query):
        """
        helper function used to check the relevance of the retrieved documents to the query asked. 
        """
        rag_model = initialize_gemini(api_config_path="config/api3.yaml") 
        retriever = prepare_retriever()
        retrieval_grader = check_docs_relevance_prompt | rag_model | JsonOutputParser()
        
        docs_txt = self._format_docs(retriever.invoke(query))        
        is_relevant = retrieval_grader.invoke({"question": query, "documents": docs_txt})['is_relevant']
        reason = retrieval_grader.invoke({"question": query, "documents": docs_txt})['reason']
        
        return is_relevant, reason, docs_txt

    def _format_docs(self, docs):
            """
            helper function used in the chain to get the text from the retrieved docs 
            """
            return "\n\n".join(doc[0].page_content if len(doc)==2 else doc.page_content for doc in docs)