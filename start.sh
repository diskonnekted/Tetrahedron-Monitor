#!/bin/bash

# Tetracore Server - Start Script
# Menjalankan semua services dalam satu command

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'  
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Cleanup function
cleanup() {
    print_status "Shutting down services..."
    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null || true
    fi
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null || true
    fi
    exit 0
}

# Set trap for cleanup
trap cleanup SIGINT SIGTERM

echo "🌌 Tetracore Server Simulation - Startup"
echo "========================================"

# Check if MongoDB is running
print_status "Checking MongoDB status..."
if ! pgrep -x "mongod" > /dev/null; then
    print_status "Starting MongoDB..."
    if command -v brew >/dev/null 2>&1; then
        # macOS with Homebrew
        brew services start mongodb-community
    elif command -v systemctl >/dev/null 2>&1; then
        # Linux with systemctl
        sudo systemctl start mongodb
    else
        # Manual start
        mongod --fork --logpath /var/log/mongodb.log
    fi
    sleep 3
else
    print_success "MongoDB already running"
fi

# Test MongoDB connection
if mongo --eval "db.adminCommand('ismaster')" >/dev/null 2>&1; then
    print_success "MongoDB connection OK"
else
    print_error "Failed to connect to MongoDB"
    exit 1
fi

# Start Backend
print_status "Starting backend server..."
cd backend
source venv/bin/activate
python server.py &
BACKEND_PID=$!
cd ..

# Wait for backend to start
sleep 3

# Test backend health
if curl -s http://localhost:8001/api/status >/dev/null; then
    print_success "Backend server running on http://localhost:8001"
else
    print_error "Backend server failed to start"
    cleanup
    exit 1
fi

# Start Frontend
print_status "Starting frontend server..."
cd frontend
yarn start &
FRONTEND_PID=$!
cd ..

# Wait for frontend to start
sleep 5

print_success "🚀 All services started successfully!"
print_status ""
print_status "Access your application:"
print_status "  Frontend: http://localhost:3000"
print_status "  Backend API: http://localhost:8001"
print_status "  API Docs: http://localhost:8001/docs"
print_status ""
print_status "Press Ctrl+C to stop all services"

# Keep script running
wait