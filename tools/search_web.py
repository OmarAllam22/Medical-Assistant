import requests
from bs4 import BeautifulSoup
from .scrap_link import ScrapLink

class WebSearch(ScrapLink):
    """
    WebSearch class performs web searches using DuckDuckGo and retrieves summaries.

    This class leverages DuckDuckGo to search for relevant webpages based on a
    user query. It then extracts summaries from the top search results and
    returns a formatted string containing the summaries.

    Inherits from the `ScrapLink` class for getting text from any website link.
    """
    def __init__(self, num_top_links = 2):
        """
        Initializes the WebSearch object.

        Args:
            num_top_links (int, optional): The number of top search results to process. Defaults to 2.
        """
        self.search_result = {} # Dictionary to store title-link pairs
        self.result_text = "" # String to store the text scrapped from a website
        self.top_links = num_top_links  # Maximum number of top links to process
        # Inherit behavior from ScrapLink for getting text from a website (set_max_chars defaults to False)
        super().__init__(set_max_chars=False)
    
    def search_query(self, query):
        """
        Performs a web search using DuckDuckGo and retrieves texts.

        Args:
            query (str): The user's search query.

        Returns:
            str: A formatted string containing final texts from the top search results.
        """
        response = requests.get(f"https://html.duckduckgo.com/html/?q={query}", headers=super().headers)
        soup = BeautifulSoup(response.text, "html.parser")

        for i in soup.findAll("div",class_='results_links')[:self.top_links]:
            link = i.find("a").get('href')
            title = i.find('h2').text.strip()

            # Ensure links start with "https:" for proper access
            if not link.startswith("https:"):
                link = "https:" + link
                
                # Store title-link pair and scrape summary for each top link
                self.search_result[title] = link
                self.result_text += f"from {title}: {super().scrap(link)}\n"

        return self.result_text
    