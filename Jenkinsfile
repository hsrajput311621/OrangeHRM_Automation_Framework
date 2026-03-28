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
        // Selenium reads this → headless Chrome + stable flags in DriverManager.java
        CI = "true"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm  // uses the repo configured in job
            }
        }

        // Windows: use "py -3" launcher first; fall back to "python" if the launcher is missing.
        // Optional: define env var PYTHON_EXE as full path to python.exe in the Jenkins job.
        stage('Set up Python venv') {
            steps {
                // If the job defines PYTHON_EXE as an empty string, "if defined PYTHON_EXE" is still
                // true and cmd runs "" -m venv. Only use PYTHON_EXE when it is non-empty.
                bat """
                    if not "%PYTHON_EXE%"=="" (
                      "%PYTHON_EXE%" -m venv ${VENV_DIR}
                    ) else (
                      py -3 -m venv ${VENV_DIR}
                      if errorlevel 1 python -m venv ${VENV_DIR}
                    )
                    if not exist ${VENV_DIR}\\Scripts\\python.exe (
                      echo ERROR: Could not create venv. Install Python 3, add py/python to PATH, or set PYTHON_EXE to python.exe
                      exit /b 1
                    )
                    call ${VENV_DIR}\\Scripts\\python.exe -m pip install --upgrade pip
                    call ${VENV_DIR}\\Scripts\\python.exe -m pip install -r requirements.txt
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
                    ${VENV_DIR}\\Scripts\\pytest TestAPI/ --alluredir=${REPORTS_DIR}\\api
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
