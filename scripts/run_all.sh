#!/bin/bash

echo "Running FULL Automation Suite..."

echo "Step 1: UI Tests"
pytest Tests/ --alluredir=Reports/allure-results

echo "Step 2: API Tests"
pytest TestsAPI/ --alluredir=Reports/allure-api-results

echo "Step 3: Performance Tests (Locust)"
locust -f Performance/Locust/locustfile.py --headless -u 10 -r 2 -t 20s

echo "Step 4: Generate Allure Report"
allure generate Reports/allure-results -o Reports/allure-report --clean

echo "✅ FULL SUITE COMPLETED!"