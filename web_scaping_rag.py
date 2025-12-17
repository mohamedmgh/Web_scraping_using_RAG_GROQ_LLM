from langchain_community.document_loaders import WebBaseLoader
from langchain_core.messages import AIMessage, HumanMessage
from dotenv import load_dotenv
from langchain_core.runnables import RunnablePassthrough


import streamlit as st
import os
import tempfile
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser



from dotenv import load_dotenv
# Load environment variables
load_dotenv()

os.environ['GROQ_API_KEY'] = os.getenv('GROQ_API_KEY')

# App configuration
st.set_page_config(page_title="RAG Chatbot Use Streamlit", page_icon="🤖")
st.title("RAG Chatbot")

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "db" not in st.session_state:
    st.session_state.db = None

# File uploader for website URL

st.header("Enter a Website URL")
website_url = st.text_input("Website URL")

# Initialize the vector database when a file is uploaded
if website_url and st.session_state.db is None:
    with st.sidebar:
        with st.spinner("Processing document..."):
            
            # Load the document
            loader = WebBaseLoader(website_url )
            data = loader.load()
            
            # Split text into chunks
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=512,
                chunk_overlap=0,
            )
            chunks = text_splitter.split_documents(data)
            
            # Create embeddings
            embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2"
            )
            
            # Initialize vector store sinon .vectorstore a la place de db
           
            st.session_state.db= FAISS.from_documents(chunks, embeddings)
            
            

# Function to get RAG response
def get_rag_response(query, chat_history):
    # Check if database is initialized
    if st.session_state.db is None:
        return "Please upload a document first."
    
    # Create retriever
    retriever = st.session_state.db.as_retriever(
        search_type="mmr",
        search_kwargs={'k': 4}
    )
    
    
    # Initialize Groq LLM
    llm = ChatGroq(
                        model="llama-3.3-70b-versatile",  
                        temperature=0.3,
                        max_tokens=512
                    )
    
    # Create RAG prompt template
    rag_template = """
    <s>[INST] You are an AI Assistant that follows instructions extremely well. Answer based on the context provided.
    
    Chat history: {chat_history}
    
    Context: {context}
    
    If the answer cannot be found in the context, please say "I don't have that information in the document." [/INST]
    
    User question: {query} </s>
    """
    
    # Format chat history for the prompt
    formatted_chat_history = "\n".join([
        f"Human: {msg.content}" if isinstance(msg, HumanMessage) else f"AI: {msg.content}"
        for msg in chat_history
    ])
    
    # Create prompt and chain
    prompt = ChatPromptTemplate.from_template(rag_template)
    output_parser = StrOutputParser()
    
    chain = (
        {
            "context": retriever, 
            "query": RunnablePassthrough(),
            "chat_history": lambda x: formatted_chat_history
        } 
        | prompt 
        | llm 
        | output_parser
    )
    
    return chain.invoke(query)

# Display chat history
for message in st.session_state.chat_history:
    if isinstance(message, HumanMessage):
        with st.chat_message("human"):
            st.markdown(message.content)
    else:
        with st.chat_message("ai"):
            st.markdown(message.content)

# Get user input
user_query = st.chat_input("Ask a question about your document...")

# Process user input
if user_query is not None and user_query != "":
    st.session_state.chat_history.append(HumanMessage(user_query))
    
    with st.chat_message("human"):
        st.markdown(user_query)
    
    with st.chat_message("ai"):
        with st.spinner("Thinking..."):
            ai_response = get_rag_response(user_query, st.session_state.chat_history)
            st.markdown(ai_response)
    
    st.session_state.chat_history.append(AIMessage(ai_response))                