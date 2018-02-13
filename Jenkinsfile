// This pipeline runs on commit to the develop branch.
// It will deploy to the QA server if all unit tests pass
// otherwise a notification is sent to Slack.
pipeline {
    agent {
        docker { 
            image 'google/cloud-sdk:latest'
            args """ --mount type=bind,source=/home/tomcat/.cache,destination=/.cache \
                     --mount type=bind,source=/home/tomcat/config,destination=/config
                     --mount type=bind,source=/home/tomcat/.config,destination=/.config'
                 """
        }
    }
    parameters {
        string(name: 'RepoUrl', defaultValue:'https://github.com/anjorinjnr/cryptograf-server')
        string(name: 'GaeSdkPath', defaultValue: '/usr/lib/google-cloud-sdk/platform/google_appengine')
    }

    stages {
        stage('Build') {
            steps {
                sh 'pip install -t lib -r requirements.txt'
            }
        }
        stage('Test') {
            steps {
               
                sh "python runner.py ${params.GaeSdkPath}"
            }
        }
        stage('Deploy to QA') {
            steps {
                 sh "gcloud auth activate-service-account --key-file /config/jenkins_qa_server.json"
                sh "gcloud app deploy --project=cryptograf-server-qa --verbosity=debug"
            }
        }
    }

    post {
        failure {
            sh """curl -X POST --data-urlencode \
                 'payload={\"channel\": \"#dev\", \
                          \"username\": \"buildbot\", \
                          \"text\": \"Breaking change - ${params.RepoUrl}/commit/${env.GIT_COMMIT}. Please fix! \", \
                          \"icon_emoji\": \":female-police-offcer:\"}' \
                  https://hooks.slack.com/services/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
                 """
        }
    }
}