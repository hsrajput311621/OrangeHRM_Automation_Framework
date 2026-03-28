#!/bin/bash
echo "Running UI Tests..."
pytest Tests/ --alluredir=Reports/allure-results
echo "UI Tests Completed ✅"