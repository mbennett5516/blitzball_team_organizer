#!/bin/bash

echo "Running tests with coverage..."
# Run tests with coverage
python -m coverage run -m unittest discover
TEST_EXIT_CODE=$?

# Generate reports
python -m coverage report -m
python -m coverage html

echo "Coverage report generated at htmlcov/index.html"

# Exit with test result for CI/CD
exit $TEST_EXIT_CODE
