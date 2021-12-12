# /bin/bash

# Exit script on error
set -e

# Remove any prexisting builds
rm -rf dist

echo "Building 'functions' pip package wheel..."

# Build a poetry wheel only in a silent mode
poetry build -q -f wheel

echo "Installing 'functions' locally..."

# Install the wheel in a silent mode and without any warnings
pip install -qq dist/functions_cli*.whl
