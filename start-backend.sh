#!/bin/bash

# Privacy-Preserving Virtual Identity System - Backend Startup Script

echo "🔐 Starting Privacy-Preserving Virtual Identity System Backend..."

# Navigate to backend directory
cd "$(dirname "$0")/backend"

# Activate virtual environment
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run setup first."
    exit 1
fi

source venv/bin/activate

# Check if dependencies are installed
if ! python -c "import fastapi" 2>/dev/null; then
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
fi

# Generate secret keys if .env doesn't exist
if [ ! -f "../.env" ]; then
    echo "🔑 Generating secret keys..."
    JWT_SECRET=$(python -c "import secrets; print(secrets.token_urlsafe(32))")
    HMAC_SECRET=$(python -c "import secrets; print(secrets.token_urlsafe(32))")
    
    cat > ../.env << EOF
# Database URL (SQLite for development)
DATABASE_URL=sqlite+aiosqlite:///../vid_system.db

# JWT Secret Key
JWT_SECRET_KEY=$JWT_SECRET

# HMAC Secret Key for QR signing
HMAC_SECRET_KEY=$HMAC_SECRET

# VID Settings
VID_EXPIRY_MINUTES=60
VID_USAGE_LIMIT=1

# CORS Origins
CORS_ORIGINS=http://localhost:3000,http://localhost:8000,http://127.0.0.1:8000,http://127.0.0.1:3000
EOF
    echo "✅ Environment file created"
fi

# Start the server
echo "🚀 Starting FastAPI server on http://localhost:8000"
echo "📚 API documentation available at http://localhost:8000/docs"
echo ""
python main.py
