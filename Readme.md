RAG Chatbot avec Streamlit et Groq
Un chatbot intelligent qui répond à vos questions basées sur vos documents PDF.

🚀 Fonctionnalités

📄 Upload your web site 
🧠 Recherche sémantique avec embeddings
⚡ Réponses rapides avec Groq API
💬 Interface chat intuitive avec Streamlit

📦 Installation
1. Cloner le repository
bash git clone https://github.com/mohamedmgh/Web_scraping_using_RAG_GROQ_LLM.git

2. Créer un environnement virtuel
bash python -m venv venv

3. Activer l'environnement
Windows :
bash venv\Scripts\activate
Mac/Linux :
bash source venv/bin/activate

4. Installer les dépendances
bash pip install -r requirements.txt

5. Configurer l'API Groq

Créez un compte sur Groq Console
Générez une API Key
Créez un fichier .env :

bash GROQ_API_KEY=gsk_votre_token_ici


🎯 Utilisation
bash streamlit run app.py
Puis ouvrez votre navigateur sur : http://localhost:8501
📚 Technologies utilisées

Streamlit - Interface web
LangChain - Framework RAG
Groq - LLM (Llama 3)
FAISS - Base de données vectorielle
Sentence Transformers - Embeddings

🤝 Contribution
Les contributions sont les bienvenues !

👤 Auteur
mohamedmgh

