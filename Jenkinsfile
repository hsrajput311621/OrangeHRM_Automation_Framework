pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/hsrajput311621/OrangeHRM_Automation_Framework.git'


            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Run UI Tests') {
            steps {
                sh 'pytest Tests/ --alluredir=Reports/allure-results'
            }
        }

        stage('Run API Tests') {
            steps {
                sh 'pytest TestsAPI/ --alluredir=Reports/allure-api-results'
            }
        }

        stage('Run Performance Tests') {
            steps {
                sh 'locust -f Performance/Locust/locustfile.py --headless -u 10 -r 2 -t 30s'
            }
        }

        stage('Generate Allure Report') {
            steps {
                sh 'allure generate Reports/allure-results -o Reports/allure-report --clean'
            }
        }
    }
}
