#!/bin/bash

# Privacy-Preserving Virtual Identity System - Frontend Startup Script

echo "🌐 Starting Privacy-Preserving Virtual Identity System Frontend..."

# Navigate to frontend directory
cd "$(dirname "$0")/frontend"

# Check if Python is available
if command -v python3 &> /dev/null; then
    echo "🚀 Starting frontend on http://localhost:3000"
    echo "📱 Open your browser and visit: http://localhost:3000"
    echo ""
    python3 -m http.server 3000
elif command -v python &> /dev/null; then
    echo "🚀 Starting frontend on http://localhost:3000"
    echo "📱 Open your browser and visit: http://localhost:3000"
    echo ""
    python -m http.server 3000
else
    echo "❌ Python not found. Please install Python to run the frontend server."
    exit 1
fi
