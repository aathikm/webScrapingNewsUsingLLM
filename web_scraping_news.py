import keyword
import requests
from bs4 import BeautifulSoup
import pandas as pd

from llm_newsScraping import create_scraped_news

def get_third_part(link):
    parts = link.split('/')  # Split the URL by "/"
    if len(parts) > 3:       # Ensure the URL has enough parts
        return parts[3]
    return None

url = "https://www.espn.in/football/"
keywords = ["football", "soccer"]

class WebScrappingDataGeneration:
    def __init__(self, url, keywords: list):
        self.url = url
        self.keywords = keywords
        
    def scrap_data(self): 
        ## URL Link       
        URL_link = self.url
        
        ## Headers to prevent the bad connection issue
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
        }
        
        ## setup the beautiful soup functionality
        response = requests.get(URL_link, headers=headers)
        bsoup = BeautifulSoup(response.content, 'html.parser')
        
        ## Grep the links in website content page
        raw_links = bsoup.find_all("a")
        links = []
        text = []
        for link in raw_links:
            links.append(link.get("href"))
            text.append(link.string)
            
        ## Converting lists to dataframe
        raw_df = pd.DataFrame({
            "link": links,
            "label": text
        })
        raw_df1 = raw_df.dropna().reset_index()
        
        rVal = raw_df1["link"].map(lambda x: x.startswith("https://"))
        master_Df = raw_df1[rVal].drop("index", axis=1).reset_index().drop("index", axis=1)
        master_Df["extracted"] = master_Df["link"].apply(get_third_part)
        
        master_Df = master_Df[(master_Df["extracted"] == self.keywords[0]) | (master_Df["extracted"] == self.keywords[1])]
        master_Df = pd.DataFrame(master_Df)
        return master_Df
    
class ScrapData:
    def __init__(self, url, keywords: list):
        self.url = url
        self.keywords = keywords
    
    def scrap(self):        
        data = WebScrappingDataGeneration(url, keywords=keywords).scrap_data()
        data["scrapped_news"] = data["link"].apply(create_scraped_news)
        
        return data