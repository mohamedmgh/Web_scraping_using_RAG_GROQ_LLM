pipeline {
    // ↑ "Je suis un pipeline Jenkins"
    
    agent any
    // ↑ "Lance-moi sur n'importe quel serveur disponible"
    
    environment {
        IMAGE_NAME = "rag-chatbot"
        // ↑ "Le nom de mon image Docker"
    }
    
    stages {
        // ↑ "Voici les étapes à suivre"
        
        stage('Checkout Code') {
            // ↑ "ÉTAPE 1 : Télécharge le code"
            steps {
                checkout scm
                // ↑ "Va chercher le code sur Git"
            }
        }
        
        stage('Build Docker Image') {
            // ↑ "ÉTAPE 2 : Crée la boîte Docker"
            steps {
                sh "docker build -t ${IMAGE_NAME} ."
                // ↑ "Exécute la commande Docker build"
            }
        }
        
        stage('Deploy Container') {
            // ↑ "ÉTAPE 3 : Lance l'application"
            steps {
                sh "docker run -d --name chatbot ${IMAGE_NAME}"
                // ↑ "Lance le container"
            }
        }
    }
    
    post {
        success {
            // ↑ "Si tout s'est bien passé"
            echo 'Succès !'
        }
        failure {
            // ↑ "Si quelque chose a planté"
            echo 'Échec !'
        }
    }
}
// ↑ "Fin du pipeline Jenkins"