#!/bin/bash

# Tetracore Server - Automated Setup Script
# Untuk Linux/macOS

set -e

echo "🌌 Tetracore Server Simulation - Automated Setup"
echo "=================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
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

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Step 1: Check Prerequisites
print_status "Checking prerequisites..."

# Check Python
if command_exists python3; then
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    print_success "Python $PYTHON_VERSION found"
    PYTHON_CMD="python3"
elif command_exists python; then
    PYTHON_VERSION=$(python --version 2>&1 | awk '{print $2}')
    print_success "Python $PYTHON_VERSION found"
    PYTHON_CMD="python"
else
    print_error "Python not found. Please install Python 3.8 or higher."
    exit 1
fi

# Check Node.js
if command_exists node; then
    NODE_VERSION=$(node --version)
    print_success "Node.js $NODE_VERSION found"
else
    print_error "Node.js not found. Please install Node.js 16 or higher."
    exit 1
fi

# Check Yarn
if command_exists yarn; then
    YARN_VERSION=$(yarn --version)
    print_success "Yarn $YARN_VERSION found"
else
    print_warning "Yarn not found. Installing Yarn..."
    npm install -g yarn
fi

# Check MongoDB
if command_exists mongod; then
    print_success "MongoDB found"
else
    print_warning "MongoDB not found. Please install MongoDB manually."
    print_status "Installation guides:"
    print_status "- macOS: brew install mongodb-community"
    print_status "- Ubuntu: sudo apt install mongodb"
    print_status "- Or visit: https://docs.mongodb.com/manual/installation/"
fi

# Step 2: Setup Backend
print_status "Setting up backend..."

cd backend

# Create virtual environment
if [ ! -d "venv" ]; then
    print_status "Creating Python virtual environment..."
    $PYTHON_CMD -m venv venv
fi

# Activate virtual environment
print_status "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
print_status "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
print_status "Installing Python dependencies..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
else
    print_error "requirements.txt not found in backend directory"
    exit 1
fi

# Setup environment variables
if [ ! -f ".env" ]; then
    print_status "Creating backend .env file..."
    cp .env.example .env
    print_success "Backend .env created from template"
else
    print_warning "Backend .env already exists, skipping..."
fi

print_success "Backend setup completed!"

# Step 3: Setup Frontend
print_status "Setting up frontend..."

cd ../frontend

# Install dependencies
print_status "Installing Node.js dependencies..."
if [ -f "package.json" ]; then
    yarn install
else
    print_error "package.json not found in frontend directory"
    exit 1
fi

# Setup environment variables
if [ ! -f ".env" ]; then
    print_status "Creating frontend .env file..."
    cp .env.example .env
    print_success "Frontend .env created from template"
else
    print_warning "Frontend .env already exists, skipping..."
fi

print_success "Frontend setup completed!"

# Step 4: Start Services
print_status "Starting services..."

# Start MongoDB (if not running)
if ! pgrep -x "mongod" > /dev/null; then
    print_status "Starting MongoDB..."
    if command_exists brew; then
        # macOS with Homebrew
        brew services start mongodb-community
    elif command_exists systemctl; then
        # Linux with systemctl
        sudo systemctl start mongodb
    else
        # Manual start
        mongod --fork --logpath /var/log/mongodb.log
    fi
else
    print_success "MongoDB already running"
fi

# Wait for MongoDB to start
sleep 2

# Test MongoDB connection
print_status "Testing MongoDB connection..."
if mongo --eval "db.adminCommand('ismaster')" >/dev/null 2>&1; then
    print_success "MongoDB connection successful"
else
    print_error "Failed to connect to MongoDB"
    exit 1
fi

cd ..

print_success "Setup completed successfully!"
print_status ""
print_status "🚀 To start the application:"
print_status ""
print_status "Terminal 1 - Backend:"
print_status "  cd backend"
print_status "  source venv/bin/activate"
print_status "  python server.py"
print_status ""
print_status "Terminal 2 - Frontend:"
print_status "  cd frontend"
print_status "  yarn start"
print_status ""
print_status "Then open http://localhost:3000 in your browser"
print_status ""
print_success "Happy simulating! 🌌"