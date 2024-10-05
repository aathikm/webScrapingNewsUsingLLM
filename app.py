import groq
import validators, streamlit as st 
import os
from dotenv import load_dotenv
load_dotenv()

from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import UnstructuredURLLoader

st.title("Text summarization from websites")

# with st.sidebar:
#     groq_api = st.text_input("Enter the groq Api key...", value="", type="password")

groq_api = os.getenv("GROQ_API")
    
url_link = st.text_input("URL", label_visibility='collapsed')

## Gemma Model USsing Groq API
llm = ChatGroq(model="Gemma-7b-It", groq_api_key=groq_api)

prompt_template = """
Providing the summarise content with 300 words:
Content: {text}
"""

prompt = PromptTemplate(template = prompt_template, input_variables=["text"])

if st.button("Summarise the content:"):
    
    ## Check the groq_api key value
    if not groq_api.strip() or not url_link.strip():
        st.error("Please provide the necessary details to start the summarization")
        
    ##Validating the groq_api and url link
    elif not validators.url(url_link):
        st.error("Please enter the valid URL")
        
    ## Read and summarise the content from URL
    else:
        try:
            with st.spinner("Waiting..."):           
                ## Read the url data
                loader = UnstructuredURLLoader(urls=[url_link], ssl_verify = False,
                                                 headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"})
                docs = loader.load()
                st.spinner(f"30% completed...")
                ## Chain for summarization
                chain = load_summarize_chain(llm, chain_type="stuff", prompt=prompt)
                st.spinner(f"70% completed...")
                output_chain = chain.run(docs)
                st.success(output_chain)
                
        except Exception as e:
            st.exception(f"Error {e}")