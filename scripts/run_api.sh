#!/bin/bash
echo "Running API Tests..."
pytest TestAPI/ --alluredir=Reports/allure-api-results
echo "API Tests Completed ✅"