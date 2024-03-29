import streamlit as st
from langchain_community.vectorstores.cassandra import Cassandra
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain_community.llms import OpenAI
from langchain_community.embeddings import OpenAIEmbeddings
from datasets import load_dataset
from dotenv import load_dotenv
import cassio
import os
from langchain.text_splitter import CharacterTextSplitter
load_dotenv()
from PyPDF2 import PdfReader
from typing_extensions import Concatenate
from PIL import Image
from cryptography.fernet import Fernet


st.set_page_config(page_title="Constitution Paddy", page_icon="images/COA.png", layout="wide")

ASTRA_DB_APPLICATION_TOKEN = st.secrets["ASTRA_DB_APPLICATION_TOKEN"]
ASTRA_DB_ID = st.secrets["ASTRA_DB_ID"]



OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

cassio.init(token=ASTRA_DB_APPLICATION_TOKEN, database_id=ASTRA_DB_ID)



llm = OpenAI(openai_api_key=OPENAI_API_KEY, model_name="gpt-3.5-turbo")
embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

astra_vector_store = Cassandra(
    embedding=embeddings,
    table_name="qa_mini",
    session=None,
    keyspace=None
)



astra_vector_index_cache = st.cache(allow_output_mutation=True)
def create_astra_vector_index(vectorstore):
    return VectorStoreIndexWrapper(vectorstore=vectorstore)

astra_vector_index = create_astra_vector_index(astra_vector_store)

st.title("Nigerian Constitution Buddy")
C1,C2,C3 = st.columns(3) 

with C2:
    st.image('images/nf.gif')  
st.sidebar.image('images/const.png') 
st.sidebar.write("This is your Nigeria constitution chat buddy, Answering all of your questions as regarding the Nigerian constitution. Just ask your question and click on answer and the chat buddy with give you the constitution gist")  
st.sidebar.write("\n\n\n")
st.sidebar.write("NB: This is a prototype, the chat buddy is still in development phase, so there might be some errors. Please report them to ezinwanneaka@gmail.com")
st.sidebar.markdown('![Visitor count](https://shields-io-visitor-counter.herokuapp.com/badge?page=https://share.streamlit.io/constitution-chat-buddy.streamlit.app/&label=VisitorsCount&labelColor=000000&logo=GitHub&logoColor=FFFFFF&color=1D70B8&style=for-the-badge)')
question = st.text_input("Ask me any question?")
question1 = f"Summarize in 200 characters or less, {question}"
import openai

if st.button('Answer'):
    try:
        answer = astra_vector_index.query(question1, llm=llm)
        st.write(f"Constitution Amebo:\n {answer}")
    except openai.error.RateLimitError as e:
        st.error("Oops! Looks like we've hit a rate limit error.")
        st.write("This might be because we've exceeded the rate limit of our chat buddy service.")
        st.write("Please wait for a moment and try again later. We're constantly working to improve our service.")
        st.write(f"Please try again after {e.retry_after_seconds} seconds.")




