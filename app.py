import streamlit as st 
import requests
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
import re

# Base Class for WebScraper
class WebScraper(ABC):
   
    @abstractmethod
    def url_button(self, url):
        pass 
    
# Class for Url
class Url:
    def scrape_visible_text_from_url(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            for tag in soup(["script", "style", "meta", "link", "noscript", "header", "footer", "aside", "nav", "img"]):
                tag.extract()
            
            header_content = soup.find("header")
            header_text = header_content.get_text() if header_content else ""
            
            paragraph_content = soup.find_all("p")
            paragraph_text = " ".join([p.get_text() for p in paragraph_content])
            
            visible_text = f"{header_text}\n\n{paragraph_text}"
            visible_text = re.sub(r'\s+', ' ', visible_text)
            return visible_text.strip()
        
        except Exception as e:
            st.error(f"Error occurred while scraping the data: {e}")
            return None 

# URL Input
class UrlInput:
    def url_input(self):
        url_input = st.text_input("URL:", "")
        return url_input
        
## URL_Button
class UrlButton(WebScraper):
     def url_button(self, url):
        if st.button("Loading Data:"):
            if url:
                url_instance = Url()
                data = url_instance.scrape_visible_text_from_url(url)
                if data:
                    st.success("Data text successfully scraped!")
                    st.subheader("Scraped Text :")
                    st.write(data)
                else:
                    st.warning("Failed to load data from the URL.")
            else:
                st.warning("Please enter a valid URL")
                
        
# Streamlit app
def main():
    st.title("Web Data Scraper")
    url_input_instance = UrlInput()
    url = url_input_instance.url_input()
    url_button_instance = UrlButton()
    url_button_instance.url_button(url)
    
if __name__ == "__main__":
    main()
                     
                    