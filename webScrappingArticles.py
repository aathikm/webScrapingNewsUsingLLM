from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Function to extract news articles from a page
def scrape_news_from_page(url, label):
    # Send a request to the website
    headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
        }  
    
    response = requests.get(url, headers=headers)
        
    # Check if request was successful
    if response.status_code != 200:
        print(f"Failed to retrieve page: {url}")
        return []

    # Parse the page content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all the articles or news elements (modify selectors based on website structure)
    news_items = soup.find_all('article')  # or use specific class or tag based on website

    # List to store scraped news data
    news_data = []

    # Loop through the found news items and extract relevant data
    for item in news_items:
        try:
            # Extract title, link, and summary (modify selectors as needed)
            title = item.find('h2').get_text().strip() if item.find('h2') else "No title"
            link = item.find('a')['href'] if item.find('a') else "No link"
            summary = item.find('p').get_text().strip() if item.find('p') else "No summary"

            # Append the news item to the list
            news_data.append({
                'title': title,
                'link': link,
                'summary': summary,
                'label': label,
                'raw_url': url
            })
        except Exception as e:
            print(f"Error processing article: {e}")

    return pd.DataFrame(news_data)

def complete_link(row):
    if row['link'].startswith('/'):  # Check if it's a relative URL
        return urljoin(row['raw_url'], row['link'])  # Join base URL and relative link
    else:
        return row['link'] 

# Function to scrape meaningful content from the specified structure
def scrape_article(link):
    try:
        # Send a GET request to the URL
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
        } 
        response = requests.get(link, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses

        # Parse the page content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the article container
        article = soup.find('article', class_='article')
        if article:
            # Extract the header content (title, etc.)
            header = article.find('header', class_='article-header')
            title = header.get_text(strip=True) if header else 'No Title'

            # Extract the main body content
            body = article.find('div', class_='article-body')
            paragraphs = body.find_all('p') if body else []
            body_content = " ".join(paragraph.get_text(strip=True) for paragraph in paragraphs)

            return {
                'title': title,
                'content': body_content.strip()  # Return the text content
            }
        return None  # Return None if no content is found

    except Exception as e:
        print(f"Error scraping {link}: {e}")
        return None

def reading_scrapped_news():

    # scrape_news_from_page("https://www.espn.in/football/")
    urls_with_label = [
        {"url": "https://www.espn.in/football/", "label": "football"},
        {"url": "https://www.espn.in/cricket/", "label": "cricket"},
        {"url": "https://www.espn.in/badminton/", "label": "badminton"},
        {"url": "https://www.espn.in/", "label": "general"}
        ]

    all_news_df = pd.DataFrame()

    # Loop over each URL and scrape the data
    for item in urls_with_label:
        url = item["url"]
        label = item["label"]
        
        news_df = scrape_news_from_page(url, label=label)  # Scrape the current URL
        all_news_df = pd.concat([all_news_df, news_df], ignore_index=True)  

    filtered_news_df = all_news_df[all_news_df['summary'] != "No summary"].reset_index().drop("index", axis=1)
        
    filtered_news_df["full_link"] = filtered_news_df.apply(complete_link, axis = 1)
    filtered_news_df = filtered_news_df[filtered_news_df["link"] != "No link"]
    required_df = filtered_news_df.drop(["link", "raw_url"], axis=1)
    required_df["scrapped_news"] = required_df["full_link"].apply(scrape_article)
    
    final_required_df = required_df[required_df["scrapped_news"] != None]

    return final_required_df