from utils.initialize_gemini import initialize_gemini
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain.load import dumps, loads



def reciprocal_rank_fusion(results, k=60):
    """ Reciprocal_rank_fusion that takes multiple lists of ranked documents 
        and an optional parameter k used in the RRF formula """
    
    # Initialize a dictionary to hold fused scores for each unique document
    fused_scores = {}

    # Iterate through each list of ranked documents
    for docs in results:
        # Iterate through each document in the list, with its rank (position in the list)
        for rank, doc in enumerate(docs):
            # Convert the document to a string format to use as a key (assumes documents can be serialized to JSON)
            doc_str = dumps(doc)
            # If the document is not yet in the fused_scores dictionary, add it with an initial score of 0
            if doc_str not in fused_scores:
                fused_scores[doc_str] = 0
            # Retrieve the current score of the document, if any
            previous_score = fused_scores[doc_str]
            # Update the score of the document using the RRF formula: 1 / (rank + k)
            fused_scores[doc_str] += 1 / (rank + k)

    # Sort the documents based on their fused scores in descending order to get the final reranked results
    reranked_results = [
        (loads(doc), score)
        for doc, score in sorted(fused_scores.items(), key=lambda x: x[1], reverse=True)
    ]

    # Return the reranked results as a list of tuples, each containing the document and its fused score
    return reranked_results


def prepare_retriever(retrieved_docs_per_query=5, is_multi_query=True, api_config_path="config/api1.yaml"):
    """
    Purpose:
    Creates a retriever object for retrieving relevant documents from a vector store based on user queries.
    
    Parameters:
    retrieved_docs_per_query: The number of query-related documents to retrieve for each query.
    is_multi_query: Indicates whether the retriever should handle multiple queries in a single prompt.
    api_config_path: (used only in case of multi-query) the api for the model used in multi-query retrieving.
    Returns:
    A Retriever object (either a single-query or multi-query retriever).
    """

    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vectordb = Chroma(persist_directory="databases", embedding_function=embeddings)
    retriever = vectordb.as_retriever(search_kwargs={"k": retrieved_docs_per_query})

    if is_multi_query:

        llm = initialize_gemini(api_config_path=api_config_path)

        # RAG-Fusion
        rag_fusion_prompt = PromptTemplate(
            template="""You are a helpful assistant that generates multiple search queries based on a single input query. \n
                You do this to help in retrieving mission.
                Generate multiple search queries related to: {question} \n
                Output (4 queries):
                return them as 
                1.
                2.
                3.
                4.
                """,
            input_variables=['question'])


        generate_queries_chain = (
            {"question":RunnablePassthrough()}
            | rag_fusion_prompt 
            | llm
            | StrOutputParser() 
            | (lambda x: x.split("\n"))
            | (lambda x: [element for element in x if any(element.startswith(prefix) for prefix in ["1", "2","3","4"])])
        )

        
        retriever = generate_queries_chain | retriever.map() | reciprocal_rank_fusion

    return retriever



question = "What is task decomposition for LLM agents?"
