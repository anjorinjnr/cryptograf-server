pipeline {
    agent {
        docker { image: 'google/cloud-sdk:latest' }
    }
    stages {
        stage('build') {
            steps {
                sh 'git version'
            }
        }
    }
}