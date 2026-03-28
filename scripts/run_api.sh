#!/bin/bash
echo "Running API Tests..."
pytest TestsAPI/ --alluredir=Reports/allure-api-results
echo "API Tests Completed ✅"