from fastapi import FastAPI
import pandas as pd
from pydantic import BaseModel
from web_scraping_news import ScrapData
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import uvicorn
from webScrappingArticles import reading_scrapped_news

app = FastAPI()
scheduler = AsyncIOScheduler()

class ScrapRequest(BaseModel):
    url: str
    keywords: list

@app.post("/scrap")
async def scrap_and_send_column(request: ScrapRequest):
    url = request.url
    keywords = request.keywords
    
    # Scrap data using ScrapData
    scrap_cls = ScrapData(url=url, keywords=keywords)
    df = scrap_cls.scrap()

    # Extract a specific column (e.g., "Country")
    column_data = df["scrapped_news"].tolist()  # Extract the 'Country' column as a list

    # Return the column data as a JSON response
    return {"news": column_data}

@app.get("/scrapArticle")
async def scrap_and_send_column():
        
    # Scrap data using ScrapData
    df = reading_scrapped_news()
    json_records = df.to_dict(orient='records')
    # print(df)
    # Extract a specific column (e.g., "Country")
    # column_data = df["scrapped_news"].tolist()  # Extract the 'Country' column as a list

    # Return the column data as a JSON response
    return json_records

if __name__ == "__main__":
    # uvicorn.run(app, host="127.0.0.1", port=8000)
    uvicorn.run(app, host="0.0.0.0", port=8000)
