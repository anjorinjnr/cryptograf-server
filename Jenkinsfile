pipeline {
    agent {
        docker { image 'google/cloud-sdk:latest' }
    }
    stages {
        stage('build') {
            steps {
                sh 'pip install -t lib -r requirements.txt'
            }
        }
        stage('test') {
            steps {
                sh 'python runner.py /usr/lib/google-cloud-sdk/platform/google_appengine'
            }
        }

        stage('deploy to QA') {

            steps {
                echo currentBuild.result
            }
        }

    }
}