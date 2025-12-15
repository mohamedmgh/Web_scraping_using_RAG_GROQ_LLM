pipeline {
    agent any
    
    // Variables d'environnement
    environment {
        IMAGE_NAME = "rag-chatbot"
        CONTAINER_NAME = "rag-chatbot-app"
        PORT = "8501"
    }
    
    stages {
        // ÉTAPE 1 : Récupérer le code depuis Git
        stage('📥 Checkout Code') {
            steps {
                echo '🔍 Récupération du code depuis GitHub...'
                checkout scm
            }
        }
        
        // ÉTAPE 2 : Construire l'image Docker
        stage('🐳 Build Docker Image') {
            steps {
                echo '🔨 Construction de l\'image Docker...'
                script {
                    // Construire l'image
                    sh "docker build -t ${IMAGE_NAME}:latest ."
                }
            }
        }
        
        // ÉTAPE 3 : Arrêter l'ancien container s'il existe
        stage('🛑 Stop Old Container') {
            steps {
                echo '🛑 Arrêt de l\'ancien container...'
                script {
                    sh """
                        docker stop ${CONTAINER_NAME} || true
                        docker rm ${CONTAINER_NAME} || true
                    """
                }
            }
        }
        
        // ÉTAPE 4 : Lancer le nouveau container
        stage('🚀 Deploy Container') {
            steps {
                echo '🚀 Démarrage du nouveau container...'
                script {
                    sh """
                        docker run -d \
                          --name ${CONTAINER_NAME} \
                          -p ${PORT}:${PORT} \
                          -e GROQ_API_KEY=\${GROQ_API_KEY} \
                          ${IMAGE_NAME}:latest
                    """
                }
            }
        }
        
        // ÉTAPE 5 : Vérifier que ça marche
        stage('✅ Health Check') {
            steps {
                echo '✅ Vérification de l\'application...'
                script {
                    // Attendre 10 secondes que l'app démarre
                    sh "sleep 10"
                    // Tester si l'app répond
                    sh "curl -f http://localhost:${PORT}/_stcore/health || exit 1"
                }
            }
        }
    }
    
    // Que faire après (succès ou échec)
    post {
        success {
            echo '✅ SUCCÈS ! L\'application est déployée sur http://localhost:8501'
        }
        failure {
            echo '❌ ÉCHEC ! Quelque chose s\'est mal passé.'
            // Nettoyer en cas d'échec
            sh "docker stop ${CONTAINER_NAME} || true"
            sh "docker rm ${CONTAINER_NAME} || true"
        }
        always {
            echo '🧹 Nettoyage des images non utilisées...'
            sh "docker system prune -f"
        }
    }
}