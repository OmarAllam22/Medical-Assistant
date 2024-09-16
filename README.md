# Medical-Assistant (Agentic-based project from scratch)
## 📘 Overview:
This project is simply a medical terminal-assistant implemented under-the-hood as following:

<img width="900" src="https://github.com/user-attachments/assets/8c3e9e77-afa1-4859-bea7-9b307bb19682" alt="Project details">

_______________________________
## 📘 Project Goal:

This project presents a medical terminal-assistant designed to provide informative and accurate responses to user queries. The assistant leverages a ReAct-based agent to route queries to appropriate tools, including a Retrieval Augmented Generation (RAG) tool, a web search tool, and an LLM knowledge tool.
________________
## 📘 Technical Implementation:

* ### ReAct-Based Agent
  The core component of the assistant is a **ReAct-based agent** responsible for routing user queries to the most suitable too (based on description given in the ReAct prompt). This agent employs a   decision-making process to determine which tool is best equipped to handle the query based on its content and complexity.
* ### RAG Tool
  When a query is routed to the RAG tool, the following steps are executed:<br></br>
  - **Multi-Query Retrieval**: Multiple queries are generated from the original query to retrieve a more diverse set of relevant documents. This approach enhances the richness and comprehensiveness of the retrieved information.
  - **Document Ranking and Cleaning**: The retrieved documents are ranked based on their relevance to the query, and duplicates are removed to ensure a clean and focused dataset.
  - **Relevance Evaluation**: The cleaned documents are passed along with the original query to a model that evaluates their relevance. This step helps identify the most pertinent documents for answering the query.
* ### Web Search Tool
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

### First, For *Linux users*:
   * 1️⃣ run `git clone https://github.com/OmarAllam22/Medical-Assistant.git`
   * 2️⃣ enter the directory of the project  `cd Medical-Assitant`
   * 3️⃣ run the setup script `chmod +x setup.sh && ./setup.sh`
   * make sure the 
   * 4️⃣ initialize the terminal assistant with specifing the mode (--verbose or --no-verbose) `./main_script.sh --verbose`
-------------
### Second, For *linux users* via a docker image:
   * 1️⃣ From your local machine's terminal, **run `xhost +`**.
      - This step makes your machine's X-server open to connections from any host (as we want to connect this server (located on your local machine) from inside the docker container).
      - This X-server is enabled for applications that needs to run GUI from inside docker container (as docker containers is mainly CLI-based).
   * 2️⃣ From terminal, **run `docker build -t app_image .`**  
   * 3️⃣ From terminal, **run `docker run -it -v /tmp/.X11-unix:/tmp/.X11-unix:ro -e DISPLAY=$DISPLAY -p 80:8501 --name app app_image`**
      - This `-v /tmp/.X11-unix:/tmp/.X11-unix:ro` This mounts the local **/tmp/.X11-unix** directory to the container's **/tmp/.X11-unix** directory in **read-only** mode. This is typically used for running graphical applications within the container (GoogleChrome in our case).
      - This `-p 80:8501` maps port 8501 inside the container (default port for streamlit) to port 80 on the local host machine (default port for localhost).
   * 4️⃣ From your local machine, open a any web browser tab and **search for `http://localhost`**.
________________
## 📘 Resources:

* Hands on LangChain tutorials. [Here](https://python.langchain.com/v0.2/docs/tutorials/)
* Docker By Ahmed Sami. [Here](https://www.youtube.com/watch?v=PrusdhS2lmo&t=4310s)
* Building GUI application with docker introducing `X-server` concept. [Here](https://www.youtube.com/watch?v=cMsIT2otEjA&t=368s)
* Guide to building streamlit chatbot. [Here](https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps)
* About `streamlit.session_state` concept. [Here](https://docs.streamlit.io/get-started/fundamentals/advanced-concepts) 
* Using chromedriver and selenium on linux. [Here](https://www.youtube.com/watch?v=67h3IT2lm40)
________________
