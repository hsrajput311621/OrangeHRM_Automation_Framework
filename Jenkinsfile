pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main',
                    credentialsId: 'github-creds',
                    url: 'https://github.com/hsrajput311621/OrangeHRM_Automation_Framework.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                bat 'pip install -r requirements.txt'
            }
        }

        stage('Run UI Tests') {
            steps {
                bat 'pytest Tests/ --alluredir=Reports/allure-results'
            }
        }

        stage('Run API Tests') {
            steps {
                bat 'pytest TestsAPI/ --alluredir=Reports/allure-api-results'
            }
        }

        stage('Run Performance Tests') {
            steps {
                bat 'locust -f Performance/Locust/locustfile.py --headless -u 10 -r 2 -t 30s'
            }
        }

        stage('Generate Allure Report') {
            steps {
                bat 'allure generate Reports/allure-results -o Reports/allure-report --clean'
            }
        }
    }
}
