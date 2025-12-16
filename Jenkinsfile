pipeline {
    agent any
    
    environment {
        IMAGE_NAME = "rag-chatbot"
        CONTAINER_NAME = "rag-chatbot-app"
        PORT = "8501"
        DOCKER_BUILDKIT = "0"
    }
    
    stages {
        stage('📥 Checkout') {
            steps {
                echo '📥 Récupération du code...'
                checkout scm
            }
        }
        
       
        stage('🐳 Build Image') {
            steps {
                echo '🐳 Construction de l\'image Docker (version légère)...'
                script {
                    // Tag l'ancienne image avant de construire
                    bat "docker tag ${IMAGE_NAME}:latest ${IMAGE_NAME}:old 2>nul || echo 'Première build'"
                    
                    // Build sans cache pour forcer la nouvelle version
                    bat """
                        set DOCKER_BUILDKIT=0
                        docker build --no-cache -t ${IMAGE_NAME}:latest .
                    """
                    
                    // Vérifier la taille de l'image
                    bat "docker images ${IMAGE_NAME}:latest"
                }
            }
        }
        
        stage('🚀 Deploy') {
            steps {
                echo '🚀 Déploiement du container...'
                script {
                    bat """
                        docker run -d ^
                          --name ${CONTAINER_NAME} ^
                          -p ${PORT}:${PORT} ^
                          --restart unless-stopped ^
                          -e GROQ_API_KEY=%GROQ_API_KEY% ^
                          ${IMAGE_NAME}:latest
                    """
                }
            }
        }
        
        stage('✅ Verify') {
            steps {
                echo '✅ Vérification du déploiement...'
                script {
                    bat "timeout /t 20 /nobreak"
                    
                    def status = bat(
                        script: "docker ps --filter name=${CONTAINER_NAME} --format \"{{.Status}}\"",
                        returnStdout: true
                    ).trim()
                    
                    if (status.contains("Up")) {
                        echo "✅ Application déployée avec succès!"
                        bat "docker logs ${CONTAINER_NAME}"
                    } else {
                        error "❌ Le container n'a pas démarré"
                    }
                }
            }
        }
    }
    
    post {
        success {
            echo """
            ====================================
            ✅ DÉPLOIEMENT RÉUSSI !
            ====================================
            🌐 URL: http://localhost:8501
            📦 Container: ${CONTAINER_NAME}
            🐳 Image: ${IMAGE_NAME}:latest
            ====================================
            """
        }
        failure {
            echo '❌ Échec du déploiement'
            script {
                bat "docker logs ${CONTAINER_NAME} 2>nul || echo 'Pas de logs'"
            }
        }
        always {
            echo '🧹 Nettoyage final...'
            bat "docker image prune -f"
        }
    }
}