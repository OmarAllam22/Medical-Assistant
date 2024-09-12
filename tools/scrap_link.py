import requests
from bs4 import BeautifulSoup

class ScrapLink:
    """
    scrap provided Link using DuckDuckGo search Engine.
    """
    headers = {'user-agent': 'my-app/0.0.1'}
    
    def __init__(self, max_chars = 5000,headers=headers, set_max_chars=False):
        self.headers = headers
        self.max_chars = max_chars
        self.set_max_chars = set_max_chars

    def scrap(self, link):
        soup = self._get_soup_from_link(link)

        if soup: hidden_link = self._get_hidden_link(soup)
        else: hidden_link = None

        if soup and hidden_link:             
            soup = self._get_soup_from_link(hidden_link)
        text = ""
        try:
            for par in soup.findAll('p'):
                text= text + " " + par.get_text()
            if self.set_max_chars:
                return text[: self.max_chars].strip()
            else:
                return text[:].strip()
        except Exception as e: 
            return f"Error Scrapping this Link with the following exception: {e}"
        
    def _get_soup_from_link(self, link):
        response = requests.get(link, headers=self.headers)
        if response.status_code == 200:
            # Parse the HTML content
            return BeautifulSoup(response.text, 'html.parser')
        else:
            return None
    
    def _get_hidden_link(self, soup):
        """
        Checks if the soup contains a redirect script and extracts the link.
        Args:
            soup: A BeautifulSoup object representing the HTML content.
        Returns:
            The extracted redirect URL (string) if found, otherwise None.
        """
        # Find the script tag with redirection logic
        script_tag = soup.find('script', language='JavaScript')
        # Check if script tag is found and contains the specific content
        if script_tag and script_tag.text.strip().startswith('window.parent.location.replace'):
            # Extract the redirect URL from the script content
            redirect_url = script_tag.text.strip().split('"')[1]  # Extract the URL within quotes
            return redirect_url
        else:
            # Soup doesn't match the expected format
            return None
