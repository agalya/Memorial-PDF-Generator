#!/bin/bash
# Start Memorial PDF Generator Web Server
# This script installs dependencies and launches the Flask app

echo ""
echo "==================================="
echo "Memorial PDF Generator - Web Server"
echo "==================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3 from https://www.python.org/"
    exit 1
fi

# Install dependencies
echo "Installing dependencies..."
pip3 install -r requirements.txt -q

if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi

echo ""
echo "✓ Dependencies installed"
echo ""
echo "Starting web server..."
echo ""
echo "Open your browser and go to: http://127.0.0.1:5000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Run the Flask app
python3 app.py
