# Medical-Assistant (Agentic-based project from scratch)
## 📘 Overview:
This project is simply a medical terminal-assistant implemented under-the-hood as following:

<img width="900" src="https://github.com/user-attachments/assets/8c3e9e77-afa1-4859-bea7-9b307bb19682" alt="Project details">

<details>
<summary><h3> 🚩 click here to show the project images 🚩 </h3></summary>
  
* here is a snapshot of the (--verbose) mode:

<img height="200" src="https://github.com/user-attachments/assets/fe9f4a8e-504e-43ae-b879-783ff9d6051e" alt="--no-verbose mode">

* here is a snapshot of the (--no-verbose) mode:

<img height="400" src="https://github.com/user-attachments/assets/36ba2697-74fb-4b22-b6e5-79c15a69909f" alt="verbose mode1">
<img height="700" src="https://github.com/user-attachments/assets/5117836c-abd5-4edd-b7e9-94968b1cb0ec" alt="verbose mode2">
<img height="700" src="https://github.com/user-attachments/assets/ad979144-0aea-47a7-a6ad-d301b58d23f3" alt="verbose mode3">

</details>

_______________________________
## 📘 Project Goal:



This project presents a medical terminal-assistant designed to provide informative and accurate responses to user queries. The assistant leverages a ReAct-based agent to route queries to appropriate tools, including a Retrieval Augmented Generation (RAG) tool, a web search tool, and an LLM knowledge tool.
________________
## 📘 Technical Implementation:

* ### ReAct-Based Agent
  The core component of the assistant is a **ReAct-based agent** responsible for routing user queries to the most suitable too (based on description given in the ReAct prompt). This agent employs a   decision-making process to determine which tool is best equipped to handle the query based on its content and complexity.
  - ### RAG Tool
    When a query is routed to the RAG tool, the following steps are executed:<br></br>
    - **Multi-Query Retrieval**: Multiple queries are generated from the original query to retrieve a more diverse set of relevant documents. This approach enhances the richness and comprehensiveness of the retrieved information.
    - **Document Ranking and Cleaning**: The retrieved documents are ranked based on their relevance to the query, and duplicates are removed to ensure a clean and focused dataset.
    - **Relevance Evaluation**: The cleaned documents are passed along with the original query to a model that evaluates their relevance. This step helps identify the most pertinent documents for answering the query.
  - ### Web Search Tool
    when the query is routed to web search, I implemented from scratch a web search tool that:
    - **Searches the Internet**: The tool employs DuckDuckGo search engine to retrieve relevant web pages based on the query.
    - **Text Extraction**: The retrieved web pages are processed to extract relevant text content.
    - **Model Processing**: The extracted text is passed to a model that generates a response related to the original query.
* ### Answer Evaluation and Refinement
  Once the ReAct agent does its loop and found the final response, two checks are conducted:
  - **Hallucination Check**: A separate ReAct loop is generated to compare the original response with a new response. If the responses are significantly different, it indicates potential hallucination. In such cases, the assistant re-generates the answer.
  - **Answer Grading**: A model evaluates the quality of the response based on criteria like completeness, specificity, relevance, and clarity. This evaluation is guided by few-shot learning examples of good and bad answers. If the response is deemed inadequate, the assistant may refine it or seek additional information.
* ### Deployment:
    - The project is mainly run on linux-terminal. 
    - The final application was containerized by building a **windows-based docker-image** from the DockerFile.
________________
## 📘 How to use (You have 2 choices):
📌📌 **Desclaimer**: Before using it, make sure :
1. you have **four** `GOOGLE_API_KEY`
2. put the four instead of `xxxxx` in the four files in `config` directoy. (they are four to balance the request-load)
### First, For *Linux users*:
   * 1️⃣ run `git clone https://github.com/OmarAllam22/Medical-Assistant.git` to clone the repo.
   * 2️⃣ enter the directory of the project  `cd Medical-Assitant`
   * 3️⃣ run the setup script `chmod +x setup.sh && ./setup.sh`
   * make sure your python version is 3.10 or lower (ChromaDB used in the project currently doesn't support newer python versions)
     you can run `python --version`.
     if you have a version newer than 3.10 run `sudo apt-get install python 3.10` for ubuntu users
   * 4️⃣ initialize the terminal assistant with specifing the mode (--verbose or --no-verbose) `./main_script.sh --verbose`
-------------
### Second, For *Windows users* via a docker image:
   * 1️⃣ from cmd, run `git clone https://github.com/OmarAllam22/Medical-Assistant.git` to clone the repo.
   * 2️⃣ build the image from either docker or Docker-Desktop [see this as a guide](https://www.youtube.com/watch?v=_6yIwDp1vsY).
________________
## 📘 Resources:

* Hands on LangChain tutorials. [Here](https://python.langchain.com/v0.2/docs/tutorials/)
* Docker By Ahmed Sami. [Here](https://www.youtube.com/watch?v=PrusdhS2lmo&t=4310s)
* Advanced RAG technique (my advice is not be overheaded with their names, just focus on the logic). [Here](https://github.com/NisaarAgharia/Advanced_RAG/tree/main)
* Building simple ReAct agent from scratch. [Here](https://www.youtube.com/watch?v=hKVhRA9kfeM) and [this is my repo about it](https://github.com/OmarAllam22/my_ReAct_agent/tree/main)

________________
