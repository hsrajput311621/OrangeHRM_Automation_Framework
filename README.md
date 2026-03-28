# OrangeHRM Automation Framework
✅ Selenium + Python + Pytest  
✅ POM + PageFactory  
✅ Allure Reports + HTML Reports  
✅ API Testing (Requests + Pytest)  
✅ Performance Testing (Locust + JMeter)  
✅ Jenkins CI Pipeline  
✅ GitHub Actions CI Pipeline  
✅ Fully Data-Driven (JSON, CSV, Excel, Pandas DataFrame)

---

## 🚀 Features

### ✅ UI Automation
- Selenium WebDriver (Python)
- Page Object Model (POM)
- PageFactory Locators
- Explicit Waits
- Automatic Highlighting of Web Elements
- Screenshot on Failure
- Detailed Logging (automation.log + error.log)
- Parallel Execution support

### ✅ API Testing
- Requests library
- GET / POST / DELETE operations
- API + UI combined workflow tests

### ✅ Performance Testing
- Locust: Login + Dashboard load test
- JMeter: Full workflow load test

### ✅ Data Driven
Supports:
- JSON  
- CSV  
- Excel  
- Pandas DataFrame  

### ✅ CI/CD
- Jenkinsfile included
- GitHub Actions workflow included

---

## 📂 Project Structure

### **UI Tests**
```bash
pytest Tests/ --alluredir=Reports/allure-results
pytest TestsAPI/
locust -f Performance/Locust/locustfile.py --headless -u 10 -r 2 -t 20s
pytest Tests/ --maxfail=1 -q
locust -f Performance/Locust/locustfile.py