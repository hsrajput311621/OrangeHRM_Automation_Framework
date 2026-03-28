#!/bin/bash
echo "Generating Allure Report..."
allure generate Reports/allure-results -o Reports/allure-report --clean
echo "Allure Report Generated at: Reports/allure-report ✅"