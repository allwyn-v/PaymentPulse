#!/bin/bash

echo "🚀 Starting InsightX..."
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 16 or higher."
    exit 1
fi

# Create .env if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
fi

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt --quiet

# Install Node dependencies
echo "📦 Installing Node.js dependencies..."
npm install --silent

echo ""
echo "✅ Setup complete!"
echo ""
echo "🌐 Starting servers..."
echo "   - Backend: http://localhost:5000"
echo "   - Frontend: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop all servers"
echo ""

# Start backend in background
python3 app.py &
BACKEND_PID=$!

# Wait a bit for backend to start
sleep 3

# Start frontend
npm run dev &
FRONTEND_PID=$!

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID
