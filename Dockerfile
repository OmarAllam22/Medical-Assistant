# getting the base image python:3.10 
#(our project deals with ChromaDB that doesn't support newest versions than python:3.10)
FROM python:3.10.0a1-windowsservercore
# copy files from directory into the container
COPY . .
# setup environment
RUN pip install -r requirements.txt
RUN python utils/create_vectordb.py
RUN python utils/get_books_info.py
# Intialize the application in --no-verbose mode
ENTRYPOINT ["python", "main.py", "--no-verbose"]