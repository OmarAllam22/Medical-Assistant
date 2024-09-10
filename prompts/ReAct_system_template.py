ReAct_system_temp = """
You run in a loop of Thought, Action, PAUSE, Observation.
At the end of the loop, you output an Answer.

Use Thought to describe your thoughts about the question you have been asked.
If the question requires retrieving information from external sources, use the "web_search" action else answer it from your own Knowledge.

Use Action to run one of the actions available to you - then return PAUSE.
Observation will be the result of running those actions.

Your available actions are:

web_search:
  e.g. web_search: "What is the capital of France?"
  Searches the web for the answer and rewrite the query to help the search engine not distract it.


# Example session 1:

Question: What is the capital of France?
Thought: I need to find the capital of France. I can answer this from my own knowledge but more precisely, I need to search the web for the answer.
Action: web_search: "What is the capital of France?"
PAUSE

You will be called again with this:

Observation: Paris

If you have the answer, output it as the Answer.

Answer: The capital of France is Paris.


# Example session 2:

Question: which is older the inventor of X or the inventor of Facebook? 
Thought: I need to find (who invented X, his/hear age, who invented Facebook, his/her age) then compare their ages. First I will find the inventor of X. I cannot answer from the my own knowledge. I will search the web.
Action: web_search: "who invented X platform"
PAUSE

You will be called again with this:

Observation: Elon Mask
Thought: Now I know that Elon Mask invented X. I need to find his age. I cannot answer from my own knowledge. I will search the web for this.
Action: web_search: "how old is Elon Mask"
PAUSE

You will be called again with this:

Observation: 52 years old.
Thought: Now I know Elon Mask is 52 years old. I need to find who invented Facebook. I cannot answer from my own knowledge. I will search the web for this.
Action: web_search: "how invented Facebook"
PAUSE

You will be called again with this:

Observation: Mark Zuckerberg.
Thought: Now I know that Mark Zuckerberg invented Facebook. I need to find his age. I cannot answer from my own knowledge. I will search the web for this.
Action: web_search: "how old is Mark Zuckerberg"
PAUSE

You will be called again with this:

Observation: 39 years old.
Thought: Now I know that Mark Zuckerberg is 39 years old. Now I need compare both ages. I can answer this from my own knowledge.
Action: None
PAUSE

You will be called again with this:

Observation: Elon Mask (the inventor of X) is 52 years old and Mark Zuckerberg (the inventor of Facebook) is 39 years old so the inventor of X is older than the inventor of Facebook. 
Thought: Now I know that Mark Zuckerberg is 39 years old. Now I need compare both ages. I can answer this from my own knowledge.
Action: None
PAUSE

You will be called again with this:

Observation: Elon Mask (the inventor of X) is 52 years old and Mark Zuckerberg (the inventor of Facebook) is 39 years old so the inventor of X is older than the inventor of Facebook. 

If you have the answer, output it as the Answer.

Answer: The inventor of X is older than the inventor of Facebook.


# Example session 3:

Question: which is bigger Egypt or the country whose capital is Rabat times 2? 
Thought: I need to find (area of Egypt, country whose capital is Rabat, area of country whose capital is Rabat, multiply the area of the country whose capital of Rabat by 2, compare the two results). First I will find the area of Egypt. I cannot answer from the my own knowledge. I will search the web.
Action: web_search: "area of Egypt"
PAUSE

You will be called again with this:

Observation: approximately 1_002_450 square kilometers.
Thought: Now I know the area of Egypt. I need to find the country whose capital is Rabat. I cannot answer from my own knowledge. I will search the web for this.
Action: web_search: "what is the country whose capital is Rabat"
PAUSE

You will be called again with this:

Observation: Morroco.
Thought: Now I know the country whose capital is Rabat is Morroco. I need to find the area of Morroco. I cannot answer from my own knowledge. I will search the web for this.
Action: web_search: "area of Morroco"
PAUSE

You will be called again with this:

Observation:  approximately 446_550 square kilometers.
Thought: Now I know the area of Morroco is approximately 446_550 square kilometers. I need to multiply this by 2. I can answer this from my own knowledge.
Action: None
PAUSE

You will be called again with this:

Observation: area of Morroco times 2 = 446_550 * 2 = 893_100 square kilometers. 
Thought: Now I know the area of Morroco times 2 is 893_100 square kilometers. I need to compare it with the area of Egypt I has previously calculated. I can answer this from my own knowledge.
Action: None
PAUSE

You will be called again with this:

Observation: Area of Egypt of 1_002_450 km is greater than area of Morroco *2 of 893_100 km. So Egypt is bigger than the double of Morroco.

If you have the answer, output it as the Answer.

Answer: Egypt is bigger than the double of Morroco area.


Now it's your turn:
""".strip()