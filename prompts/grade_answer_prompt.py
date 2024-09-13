from langchain_core.prompts import PromptTemplate

grade_answer_prompt = PromptTemplate(
            template="""You are a grader assessing whether an answer is useful to resolve a question.

            Here is the answer:
            \n ------- \n
            {answer} 
            \n ------- \n
            Here is the question: {query}

            Evaluate the answer based on these criteria:
            1. Completeness: Does the answer address all aspects of the question?
            2. Relevance: Is the information provided directly relevant to the query?
            3. Specificity: Does the answer provide specific details or examples?
            4. Clarity: Is the answer easy to understand and free from ambiguity?

            # Examples of good and bad answers:

            Good Answer Examples:
                1. Query: What are the symptoms of COVID-19?
                Answer: The primary symptoms of COVID-19 include fever, cough, and shortness of breath. Other common symptoms may include fatigue, muscle aches, headache, loss of taste or smell, sore throat, congestion or runny nose, nausea or vomiting, and diarrhea.   

                2. Query: Who was the first president of the United States?
                Answer: George Washington was the first president of the United States.

                3. Query: How do you calculate the area of a circle?
                Answer: The area of a circle is calculated using the formula: A = πr², where A is the area, π is a mathematical constant approximately equal to 3.14159, and r is the radius of the circle.

                4. Query: What is the capital of France?
                Answer: The capital of France is Paris.

                5. Query: Explain the concept of artificial intelligence.
                Answer: Artificial intelligence (AI) is a broad field of computer science that deals with creating intelligent agents, which are systems that can reason, learn, and act autonomously. AI applications include natural language processing, computer vision, and robotics.

            Bad Answer Examples
                1. Query: What are the symptoms of COVID-19?
                Answer: Wear a mask.

                2. Query: Who was the first president of the United States?
                Answer: Abraham Lincoln.

                3. Query: How do you calculate the area of a circle?
                Answer: The area of a circle is a mathematical equation.

                4. Query: What is the capital of France?
                Answer: Paris is a city in France.

                5. Query: Explain the concept of artificial intelligence.
                Answer: AI is a computer program.

                6. Query: How are you?
                Answer: I cannot answer.

            **Important Note:** Questions that primarily seek personal opinions, emotions, or subjective judgments (e.g., "How are you?", "How do you do?", "Which is older, you or Elon Musk?") are considered good answers regardless of their content.

            Give a binary score 'yes' or 'no' to indicate whether the answer is useful to resolve a question.
            Provide the binary score as a JSON with a single key 'is_good_answer' and no preamble or explanation.""",
            input_variables=["answer", "query"],
        )