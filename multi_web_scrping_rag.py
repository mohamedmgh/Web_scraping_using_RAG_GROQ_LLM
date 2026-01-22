from langchain_community.document_loaders import WebBaseLoader
from langchain_core.messages import AIMessage, HumanMessage
from dotenv import load_dotenv
from langchain_core.runnables import RunnablePassthrough
import streamlit as st
import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Load environment variables
load_dotenv()
os.environ['GROQ_API_KEY'] = os.getenv('GROQ_API_KEY')

# App configuration
st.set_page_config(page_title="RAG Chatbot Multi-Sites", page_icon="🤖")
st.title("RAG Chatbot - Multi-Sites")

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "db" not in st.session_state:
    st.session_state.db = None
if "processed_urls" not in st.session_state:
    st.session_state.processed_urls = []

# Sidebar for URL management
with st.sidebar:
    st.header("📚 Gestion des Sites Web")
    
    # Display processed URLs
    if st.session_state.processed_urls:
        st.subheader("Sites chargés:")
        for i, url in enumerate(st.session_state.processed_urls, 1):
            st.text(f"{i}. {url[:50]}...")
    
    st.divider()
    
    # Input for new URL
    new_url = st.text_input("Ajouter un nouveau site:", key="new_url_input")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("➕ Ajouter", use_container_width=True):
            if new_url and new_url not in st.session_state.processed_urls:
                with st.spinner(f"Traitement de {new_url}..."):
                    try:
                        # Load the document
                        loader = WebBaseLoader(new_url)
                        data = loader.load()
                        
                        # Split text into chunks
                        text_splitter = RecursiveCharacterTextSplitter(
                            chunk_size=512,
                            chunk_overlap=50,
                        )
                        chunks = text_splitter.split_documents(data)
                        
                        # Add source URL to metadata
                        for chunk in chunks:
                            chunk.metadata['source_url'] = new_url
                        
                        # Create embeddings
                        embeddings = HuggingFaceEmbeddings(
                            model_name="sentence-transformers/all-MiniLM-L6-v2"
                        )
                        
                        # Initialize or update vector store
                        if st.session_state.db is None:
                            st.session_state.db = FAISS.from_documents(chunks, embeddings)
                        else:
                            # Add new documents to existing database
                            new_db = FAISS.from_documents(chunks, embeddings)
                            st.session_state.db.merge_from(new_db)
                        
                        st.session_state.processed_urls.append(new_url)
                        st.success(f"✅ Site ajouté avec succès!")
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"❌ Erreur lors du chargement: {str(e)}")
            elif new_url in st.session_state.processed_urls:
                st.warning("⚠️ Ce site a déjà été ajouté!")
            else:
                st.warning("⚠️ Veuillez entrer une URL valide!")
    
    with col2:
        if st.button("🗑️ Tout effacer", use_container_width=True):
            st.session_state.db = None
            st.session_state.processed_urls = []
            st.session_state.chat_history = []
            st.success("✅ Toutes les données ont été effacées!")
            st.rerun()

# Main area
st.header("💬 Chat")

# Function to get RAG response
def get_rag_response(query, chat_history):
    # Check if database is initialized
    if st.session_state.db is None:
        return "Veuillez d'abord ajouter au moins un site web dans la barre latérale."
    
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
    rag_template = """[INST] Vous êtes un assistant IA qui suit les instructions de manière excellente.
Répondez en vous basant sur le contexte fourni provenant de plusieurs sites web.

Historique de conversation:
{chat_history}

Contexte (provenant de plusieurs sites):
{context}

Si la réponse ne peut pas être trouvée dans le contexte, dites "Je n'ai pas cette information dans les documents chargés."
Lorsque vous citez une information, mentionnez la source si elle est disponible .
Lorsque vous citez une information, ne dit pas " Je n'ai pas cette information dans les documents chargés".
[/INST]

Question de l'utilisateur: {query}"""
    
    # Format chat history for the prompt
    formatted_chat_history = "\n".join([
        f"Humain: {msg.content}" if isinstance(msg, HumanMessage) 
        else f"IA: {msg.content}"
        for msg in chat_history[-6:]  # Keep only last 6 messages for context
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

# Display information if no sites are loaded
if not st.session_state.processed_urls:
    st.info("👈 Commencez par ajouter des sites web dans la barre latérale pour pouvoir poser des questions!")

# Display chat history
for message in st.session_state.chat_history:
    if isinstance(message, HumanMessage):
        with st.chat_message("human"):
            st.markdown(message.content)
    else:
        with st.chat_message("ai"):
            st.markdown(message.content)

# Get user input
user_query = st.chat_input("Posez une question sur les documents chargés...")

# Process user input
if user_query is not None and user_query != "":
    st.session_state.chat_history.append(HumanMessage(user_query))
    
    with st.chat_message("human"):
        st.markdown(user_query)
    
    with st.chat_message("ai"):
        with st.spinner("Réflexion..."):
            ai_response = get_rag_response(user_query, st.session_state.chat_history)
            st.markdown(ai_response)
    
    st.session_state.chat_history.append(AIMessage(ai_response))