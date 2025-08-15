# ⚡ Quick Start - Tetracore Server (5 Minutes Setup)

Panduan super cepat untuk menjalankan **Tetracore Server Simulation** di komputer Anda dalam 5 menit!

## 🚀 One-Command Setup (Jika memungkinkan)

Jika Anda sudah punya Python, Node.js, dan MongoDB:

```bash
# Clone dan setup dalam satu langkah
git clone https://github.com/your-username/tetracore-server.git
cd tetracore-server && chmod +x quick-setup.sh && ./quick-setup.sh
```

## 📦 Manual Quick Setup

### Step 1: Download Requirements (2 menit)

**Jika belum ada, install cepat:**

```bash
# Windows (menggunakan Chocolatey)
choco install python nodejs mongodb

# macOS (menggunakan Homebrew)  
brew install python node mongodb-community yarn

# Ubuntu/Debian
sudo apt update && sudo apt install -y python3 python3-pip nodejs npm mongodb
npm install -g yarn
```

### Step 2: Project Setup (2 menit)

```bash
# 1. Download project
mkdir tetracore-server && cd tetracore-server

# 2. Setup backend
mkdir backend && cd backend
cat > requirements.txt << EOF
fastapi==0.110.1
uvicorn==0.25.0
pymongo==4.5.0
motor==3.3.1
python-dotenv>=1.0.1
pydantic>=2.6.4
python-multipart>=0.0.9
requests>=2.31.0
numpy>=1.26.0
EOF

cat > .env << EOF
MONGO_URL="mongodb://localhost:27017"
DB_NAME="tetracore_db"
CORS_ORIGINS="*"
EOF

pip install -r requirements.txt

# 3. Setup frontend
cd ../
mkdir frontend && cd frontend
cat > .env << EOF
REACT_APP_BACKEND_URL=http://localhost:8001
WDS_SOCKET_PORT=3000
EOF

yarn create react-app . --template typescript
yarn add axios lucide-react tailwindcss @tailwindcss/forms
```

### Step 3: Start Services (1 menit)

```bash
# Terminal 1 - Start MongoDB
mongod

# Terminal 2 - Start Backend  
cd backend
python server.py

# Terminal 3 - Start Frontend
cd frontend  
yarn start
```

## 🎯 Ultra Quick Test

**Buka browser → http://localhost:3000**

1. ✅ Klik **"Create Pair"** - harus muncul tetrahedron biru & merah
2. ✅ Klik **"Start"** - simulasi harus berjalan  
3. ✅ Klik pada pair - detail analysis muncul

**🎉 Done! Aplikasi sudah berjalan!**

## 🚨 Quick Troubleshooting

### MongoDB tidak start?
```bash
# Windows: 
net start MongoDB

# macOS:
brew services start mongodb-community

# Linux:
sudo systemctl start mongodb
```

### Port conflict?
```bash
# Cek port yang digunakan
netstat -tulpn | grep :8001
netstat -tulpn | grep :3000

# Kill process jika perlu
sudo kill -9 $(lsof -ti:8001)
sudo kill -9 $(lsof -ti:3000)
```

### Dependencies error?
```bash
# Backend
pip install --upgrade pip
pip install -r requirements.txt

# Frontend  
yarn cache clean
rm -rf node_modules
yarn install
```

## 📋 Quick Commands Reference

```bash
# Start semua services
mongod &                          # MongoDB
cd backend && python server.py & # Backend  
cd frontend && yarn start &      # Frontend

# Stop semua services
pkill -f mongod
pkill -f "python server.py"  
pkill -f "yarn start"

# Health check
curl http://localhost:8001/api/status
curl http://localhost:3000
```

## 🔗 Quick Access URLs

- **App**: http://localhost:3000
- **API**: http://localhost:8001  
- **API Docs**: http://localhost:8001/docs
- **MongoDB**: mongodb://localhost:27017

---

**⚡ Total setup time: ~5 minutes | Ready to simulate tetrahedron physics!**