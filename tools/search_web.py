import requests
from bs4 import BeautifulSoup
from .scrap_link import ScrapLink

class WebSearch(ScrapLink):
    def __init__(self, num_top_links = 2):
        self.search_result = {}
        self.result_text = ""
        self.top_links = num_top_links 
        super().__init__(set_max_chars=False)
    
    def search_query(self, query):
        response = requests.get(f"https://html.duckduckgo.com/html/?q={query}", headers=super().headers)
        soup = BeautifulSoup(response.text, "html.parser")

        for i in soup.findAll("div",class_='results_links')[:self.top_links]:
            link = i.find("a").get('href')
            title = i.find('h2').text.strip()
            if not link.startswith("https:"):
                link = "https:" + link
                self.search_result[title] = link

                self.result_text += f"from {title}: {super().scrap(link)}\n"

        return self.result_text
    