#!/bin/bash
echo "Running Locust Performance Test..."
locust -f Performance/Locust/locustfile.py --headless -u 10 -r 2 -t 30s
echo "Locust Test Completed ✅"