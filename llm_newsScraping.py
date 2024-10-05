import os
from dotenv import load_dotenv
load_dotenv()

from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import UnstructuredURLLoader

def create_scraped_news(url_link):
    groq_api = os.getenv("GROQ_API")

    ## Gemma Model USsing Groq API
    llm = ChatGroq(model="Gemma-7b-It", groq_api_key=groq_api)

    prompt_template = """
    Providing the title and subtitle and descrition with 100 words:
    Content: {text}
    """

    prompt = PromptTemplate(template = prompt_template, input_variables=["text"])
    loader = UnstructuredURLLoader(
        urls=[url_link],
        ssl_verify = False,
        headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"})
    docs = loader.load()

    ## Chain for summarization
    chain = load_summarize_chain(llm, chain_type="stuff", prompt=prompt)
    output_chain = chain.run(docs)
    
    return output_chain