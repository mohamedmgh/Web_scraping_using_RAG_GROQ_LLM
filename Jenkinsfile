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
        
       
        stage('🐳 Build Docker Image') {
            steps {
                bat 'docker build -t rag-chatbot:latest .'
            }
        }

        stage('🚀 Run Docker Container') {
            steps {
                bat '''
                docker stop rag-chatbot || exit 0
                docker rm rag-chatbot || exit 0
                docker run -d -p 8501:8501 --name rag-chatbot rag-chatbot:latest
                '''
            }
        }
    }

    post {
        success {
            echo '🎉 Build and deploy finished!'
            echo 'Open http://<YOUR_JENKINS_HOST>:8501 to view the app'
        }
        failure {
            echo '❌ The pipeline failed. Check logs for errors.'
        }
    }
}