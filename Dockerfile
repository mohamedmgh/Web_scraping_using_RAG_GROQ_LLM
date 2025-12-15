FROM python:3.11-slim

#Crée un dossier /app et va dedans
WORKDIR /app

#Copie la liste des bibliothèques à installer
COPY requirements.txt .

#Installe tous les librairies
RUN pip install -r requirements.txt

# Copie tout  code
COPY . .

# Ouvre la porte 8501 pour accéder à l'app
EXPOSE 8501

# Lance application
CMD ["streamlit", "run", "web_scaping_rag.py"]
