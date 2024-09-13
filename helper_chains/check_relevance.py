from langchain_core.output_parsers import JsonOutputParser

class relevance_chain:
    def __call__(self, prompt, model, retriever, query):
        """
        helper function used to check the relevance of the retrieved documents to the query asked. 
        """
        retrieval_grader = prompt | model | JsonOutputParser()
        
        docs_txt = self._format_docs(retriever.invoke(query))        
        is_relevant = retrieval_grader.invoke({"question": query, "documents": docs_txt})['is_relevant']
        reason = retrieval_grader.invoke({"question": query, "documents": docs_txt})['reason']
        
        return is_relevant, reason, docs_txt

    def _format_docs(self, docs):
            """
            helper function used in the chain to get the text from the retrieved docs 
            """
            return "\n\n".join(doc[0].page_content if len(doc)==2 else doc.page_content for doc in docs)