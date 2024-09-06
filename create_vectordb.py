import os, yaml
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
import argparse

def main(source_dir, dest_dir):
    # define the GOOGLE_API_KEY for the embeddings model.
    with open("config/api4.yaml", 'r') as f:
        data = yaml.safe_load(f)
        os.environ["GOOGLE_API_KEY"] = data.get("GOOGLE_API_KEY",None)

    # create the vector database
    loader = PyPDFDirectoryLoader(source_dir)
    pages = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(pages)
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    Chroma.from_documents(documents=splits, embedding=embeddings, persist_directory=dest_dir)
    print("Vector Database Created Successfully.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process source and destination directories")
    parser.add_argument('-s', '--source', nargs='?', default='books', help='source directory which we read books from.')
    parser.add_argument('-d', '--dist', nargs='?', default='databases', help='destination directory which we write vectoradb in.')
    args = parser.parse_args()
    
    main(args.source, args.dist)