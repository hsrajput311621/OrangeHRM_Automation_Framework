// pipeline {
//     agent any

//     stages {

//         stage('Checkout') {
//             steps {
//                 git branch: 'main',
//                     credentialsId: 'github-creds',
//                     url: 'https://github.com/hsrajput311621/OrangeHRM_Automation_Framework.git'
//             }
//         }

//         stage('Install Dependencies') {
//             steps {
//                 bat 'pip install -r requirements.txt'
//             }
//         }

//         stage('Run UI Tests') {
//             steps {
//                 bat 'pytest Tests/ --alluredir=Reports/allure-results'
//             }
//         }

//         stage('Run API Tests') {
//             steps {
//                 bat 'pytest TestsAPI/ --alluredir=Reports/allure-api-results'
//             }
//         }

//         stage('Run Performance Tests') {
//             steps {
//                 bat 'locust -f Performance/Locust/locustfile.py --headless -u 10 -r 2 -t 30s'
//             }
//         }

//         stage('Generate Allure Report') {
//             steps {
//                 bat 'allure generate Reports/allure-results -o Reports/allure-report --clean'
//             }
//         }
//     }
// }


pipeline {
    agent any

    environment {
        VENV_DIR    = ".venv"
        REPORTS_DIR = "Reports"
        SCREEN_DIR  = "Screenshots"

        // IMPORTANT: Your actual Python path (correct)
      //  PYTHON_EXE = "C:\\Users\\hiteshr\\AppData\\Local\\Programs\\Python\\Python313\\python.exe"
        PYTHON_EXE = "C:\\Users\\hiteshr\\AppData\\Local\\Programs\\Python\\Python311\\python.exe"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm  // uses the repo configured in job
            }
        }

        stage('Set up Python venv') {
            steps {
                bat """
                    "${PYTHON_EXE}" -m venv ${VENV_DIR}
                    ${VENV_DIR}\\Scripts\\pip install --upgrade pip
                    ${VENV_DIR}\\Scripts\\pip install -r requirements.txt
                """
            }
        }

        stage('Prepare Folders') {
            steps {
                bat "if not exist ${REPORTS_DIR} mkdir ${REPORTS_DIR}"
                bat "if not exist ${SCREEN_DIR} mkdir ${SCREEN_DIR}"
            }
        }

        stage('Run UI Tests') {
            steps {
                bat """
                    ${VENV_DIR}\\Scripts\\pytest Tests/ --alluredir=${REPORTS_DIR}\\ui
                """
            }
        }

        stage('Run API Tests') {
            steps {
                bat """
                    ${VENV_DIR}\\Scripts\\pytest TestsAPI/ --alluredir=${REPORTS_DIR}\\api
                """
            }
        }

        stage('Run Performance Tests (Locust)') {
            steps {
                bat """
                    ${VENV_DIR}\\Scripts\\python -m locust -f Performance/Locust/locustfile.py --headless -u 5 -r 1 -t 15s
                """
            }
        }

        stage('Generate Allure Report') {
            steps {
                bat """
                    allure generate ${REPORTS_DIR}\\ui -o ${REPORTS_DIR}\\allure-ui --clean
                """
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: "${REPORTS_DIR}/**", allowEmptyArchive: true
            archiveArtifacts artifacts: "${SCREEN_DIR}/**", allowEmptyArchive: true
        }
    }
}
