pipeline {
    agent any
    
    environment {
        IMAGE_NAME = "rag-chatbot"
        CONTAINER_NAME = "rag-chatbot-app"
        PORT = "8501"
    }
    
    stages {
        stage('📥 Checkout Code') {
            steps {
                echo '🔍 Récupération du code depuis GitHub...'
                checkout scm
            }
        }
        
        stage('🐳 Build Docker Image') {
            steps {
                echo '🔨 Construction de l\'image Docker...'
                script {
                    // Désactiver BuildKit pour éviter les erreurs EOF
                    bat """
                        set DOCKER_BUILDKIT=0
                        docker build -t ${IMAGE_NAME}:latest .
                    """
                }
            }
        }
        
        stage('🛑 Stop Old Container') {
            steps {
                echo '🛑 Arrêt de l\'ancien container...'
                script {
                    // Arrêter et supprimer l'ancien container (ignorer les erreurs)
                    bat """
                        docker stop ${CONTAINER_NAME} 2>nul || echo "Aucun container à arrêter"
                        docker rm ${CONTAINER_NAME} 2>nul || echo "Aucun container à supprimer"
                    """
                }
            }
        }
        
        stage('🚀 Deploy Container') {
            steps {
                echo '🚀 Démarrage du nouveau container...'
                script {
                    bat """
                        docker run -d ^
                          --name ${CONTAINER_NAME} ^
                          -p ${PORT}:${PORT} ^
                          -e GROQ_API_KEY=%GROQ_API_KEY% ^
                          ${IMAGE_NAME}:latest
                    """
                }
            }
        }
        
        stage('✅ Health Check') {
            steps {
                echo '✅ Vérification de l\'application...'
                script {
                    // Attendre que l'app démarre
                    bat "timeout /t 10 /nobreak"
                    
                    // Vérifier que le container tourne
                    bat "docker ps | findstr ${CONTAINER_NAME}"
                }
            }
        }
    }
    
    post {
        success {
            echo '✅ SUCCÈS ! L\'application est déployée sur http://localhost:8501'
        }
        failure {
            echo '❌ ÉCHEC ! Quelque chose s\'est mal passé.'
            script {
                // Nettoyer en cas d'échec
                bat """
                    docker stop ${CONTAINER_NAME} 2>nul || echo "Pas de container à arrêter"
                    docker rm ${CONTAINER_NAME} 2>nul || echo "Pas de container à supprimer"
                """
            }
        }
        always {
            echo '🧹 Nettoyage terminé'
        }
    }
}