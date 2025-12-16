FROM python:3.11-slim

# Crée un dossier /app et va dedans
WORKDIR /app

# Installe les dépendances requises directement, incluant maintenant les bibliothèques de scraping
RUN pip install \
    streamlit \
    langchain \
    langchain-groq \
    langchain-community \
    langchain-text-splitters \
    sentence-transformers \
    faiss-cpu \
    pypdf \
    python-dotenv \
    # Bibliothèques pour le Web Scraping :
    requests \
    beautifulsoup4 \
    lxml

# Copie tout le code
COPY . .

# Ouvre la porte 8501 pour accéder à l'app
EXPOSE 8501

# Lance l'application
CMD ["streamlit", "run", "web_scaping_rag.py"]