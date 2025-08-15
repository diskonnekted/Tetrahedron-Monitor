# 🏠 Tetracore Server - Localhost Installation Guide

Panduan lengkap untuk menginstall dan menjalankan **Tetracore Server Simulation** di localhost/komputer lokal Anda.

## 📋 Prerequisites Checker

Sebelum memulai, pastikan sistem Anda memenuhi requirements berikut:

### 1. Check Python Version
```bash
python --version
# Output yang diharapkan: Python 3.8.x atau lebih baru
```

### 2. Check Node.js Version
```bash
node --version
# Output yang diharapkan: v16.x.x atau lebih baru

npm --version
# Output yang diharapkan: 8.x.x atau lebih baru
```

### 3. Check Yarn Installation
```bash
yarn --version
# Jika belum ada, install dengan: npm install -g yarn
```

## 🔽 Step 1: Download & Setup Project

### Clone dari Repository (Jika tersedia)
```bash
git clone https://github.com/your-username/tetracore-server.git
cd tetracore-server
```

### Atau Buat Struktur Project Manual
```bash
mkdir tetracore-server
cd tetracore-server

# Buat struktur folder
mkdir backend frontend
mkdir backend/logs frontend/public/images
```

### Download File Project
Jika Anda memiliki file zip, extract ke folder `tetracore-server`:
```bash
# Extract file project
unzip tetracore-project.zip -d tetracore-server/
cd tetracore-server
```

## 🗄️ Step 2: MongoDB Installation & Setup

### Windows Installation

1. **Download MongoDB Community Server**
   ```bash
   # Kunjungi: https://www.mongodb.com/try/download/community
   # Pilih: Windows x64 MSI
   ```

2. **Install MongoDB**
   - Jalankan file `.msi` yang sudah didownload
   - Pilih "Complete" installation
   - Install sebagai Windows Service
   - Install MongoDB Compass (optional GUI tool)

3. **Verify Installation**
   ```bash
   # Buka Command Prompt sebagai Administrator
   mongod --version
   
   # Start MongoDB service (jika belum auto-start)
   net start MongoDB
   ```

### macOS Installation

```bash
# Install menggunakan Homebrew
brew tap mongodb/brew
brew install mongodb-community

# Start MongoDB service
brew services start mongodb/brew/mongodb-community

# Verify installation
mongod --version
```

### Linux (Ubuntu/Debian) Installation

```bash
# Update package database
sudo apt update

# Install MongoDB
sudo apt install -y mongodb

# Start MongoDB service
sudo systemctl start mongodb
sudo systemctl enable mongodb

# Verify installation
mongod --version
```

### Verify MongoDB Connection
```bash
# Test connection
mongo --eval "db.adminCommand('ismaster')"
# Output yang diharapkan: { "ismaster" : true, ... }
```

## 🐍 Step 3: Backend Setup

### Navigate ke Backend Directory
```bash
cd backend
```

### Create Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux  
python3 -m venv venv
source venv/bin/activate
```

### Install Python Dependencies
```bash
# Upgrade pip terlebih dahulu
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

Jika file `requirements.txt` tidak ada, install manual:
```bash
pip install fastapi==0.110.1
pip install uvicorn==0.25.0
pip install pymongo==4.5.0
pip install motor==3.3.1
pip install python-dotenv>=1.0.1
pip install pydantic>=2.6.4
pip install python-multipart>=0.0.9
pip install requests>=2.31.0
pip install numpy>=1.26.0
```

### Setup Environment Variables
```bash
# Buat file .env
touch .env  # Linux/macOS
# atau buat file .env manual di Windows

# Edit file .env dengan content:
echo 'MONGO_URL="mongodb://localhost:27017"' >> .env
echo 'DB_NAME="tetracore_db"' >> .env
echo 'CORS_ORIGINS="*"' >> .env
```

### Test Backend Installation
```bash
# Jalankan server test
python server.py

# Output yang diharapkan:
# INFO:     Started server process [xxxx]
# INFO:     Waiting for application startup.
# INFO:     Application startup complete.
# INFO:     Uvicorn running on http://0.0.0.0:8001
```

**Jangan tutup terminal ini!** Backend harus tetap berjalan.

## ⚛️ Step 4: Frontend Setup

### Buka Terminal Baru
```bash
# Navigate ke project directory
cd /path/to/tetracore-server
cd frontend
```

### Install Node.js Dependencies
```bash
# Install yarn jika belum ada
npm install -g yarn

# Install dependencies
yarn install
```

Jika terjadi error, coba:
```bash
# Clear cache dan install ulang
yarn cache clean
rm -rf node_modules package-lock.json
yarn install
```

### Setup Environment Variables
```bash
# Buat file .env
touch .env  # Linux/macOS
# atau buat file .env manual di Windows

# Edit file .env dengan content:
echo 'REACT_APP_BACKEND_URL=http://localhost:8001' >> .env
echo 'WDS_SOCKET_PORT=3000' >> .env
```

### Test Frontend Installation
```bash
# Start development server
yarn start

# Output yang diharapkan:
# webpack compiled successfully
# Local:            http://localhost:3000
# On Your Network:  http://192.168.x.x:3000
```

Browser akan otomatis terbuka ke `http://localhost:3000`

## 🧪 Step 5: Verification & Testing

### 1. Check Backend Health
Buka browser dan kunjungi:
```
http://localhost:8001/api/status
```
Response yang diharapkan:
```json
{
  "status": "Tetracore Server Running",
  "version": "1.0.0"
}
```

### 2. Check Frontend Loading
Kunjungi:
```
http://localhost:3000
```
Anda harus melihat interface Tetracore Server dengan:
- Header "Tetracore Server"
- Panel "Simulation Controls"
- Area "Tetrahedron Pairs Visualization"
- Panel "Pair Analysis"

### 3. Test Basic Functionality

#### Test 1: Create Tetrahedron Pair
1. Klik tombol **"Create Pair"**
2. Anda harus melihat pair baru muncul dengan matter (biru) dan antimatter (merah)
3. Counter "Active Pairs" harus bertambah

#### Test 2: Start Simulation
1. Klik tombol **"Start"**
2. Button berubah menjadi **"Stop"**
3. Amati perubahan pada "System Energy" dan metrics lainnya

#### Test 3: Pair Analysis
1. Klik pada salah satu tetrahedron pair
2. Panel "Pair Analysis" harus menampilkan detail:
   - Matter Tetrahedron (energy, frequency, phase)
   - Antimatter Tetrahedron (energy, frequency, phase)
   - Pairing Strength dan Entanglement status

## 🚨 Troubleshooting

### Problem 1: Backend tidak bisa start

**Error**: `ModuleNotFoundError: No module named 'fastapi'`
```bash
# Solution: Pastikan virtual environment aktif dan install dependencies
source venv/bin/activate  # Linux/macOS
# atau
venv\Scripts\activate     # Windows

pip install -r requirements.txt
```

**Error**: `pymongo.errors.ServerSelectionTimeoutError`
```bash
# Solution: MongoDB tidak berjalan
# Windows:
net start MongoDB

# macOS:
brew services start mongodb/brew/mongodb-community

# Linux:
sudo systemctl start mongodb
```

### Problem 2: Frontend tidak bisa start

**Error**: `command not found: yarn`
```bash
# Solution: Install yarn
npm install -g yarn
```

**Error**: `Module not found` atau dependency errors
```bash
# Solution: Clear cache dan reinstall
rm -rf node_modules package-lock.json yarn.lock
yarn install
```

### Problem 3: CORS Error

**Error**: `Access to fetch blocked by CORS policy`
```bash
# Solution 1: Check backend .env file
CORS_ORIGINS="*"

# Solution 2: Check frontend .env file  
REACT_APP_BACKEND_URL=http://localhost:8001

# Solution 3: Restart kedua server
```

### Problem 4: Port sudah digunakan

**Error**: `Error: listen EADDRINUSE: address already in use :::8001`
```bash
# Solution: Kill process yang menggunakan port
# Windows:
netstat -ano | findstr :8001
taskkill /PID [PID_NUMBER] /F

# Linux/macOS:
lsof -ti:8001 | xargs kill -9
```

### Problem 5: Database connection issues

**Error**: Database tidak bisa connect
```bash
# Check MongoDB status
# Windows:
net start MongoDB

# Linux:
sudo systemctl status mongodb

# macOS:
brew services list | grep mongo

# Test connection manual:
mongo --eval "db.adminCommand('ismaster')"
```

## 🔧 Development Tips

### Hot Reload
Kedua server mendukung hot reload:
- **Backend**: Perubahan pada `.py` files akan restart server otomatis
- **Frontend**: Perubahan pada React files akan refresh browser otomatis

### Debugging
```bash
# Backend logs
tail -f backend/logs/server.log

# MongoDB logs (jika ada issues)
# Windows: C:\Program Files\MongoDB\Server\4.4\log\mongod.log
# Linux: /var/log/mongodb/mongod.log
# macOS: /usr/local/var/log/mongodb/mongo.log
```

### Performance Monitoring
```bash
# Monitor resource usage
# Windows: Task Manager
# Linux: htop atau top
# macOS: Activity Monitor

# Monitor database
mongo
> show dbs
> use tetracore_db
> show collections
> db.tetrahedron_pairs.count()
```

## 🚀 Production Deployment (Optional)

### Build Frontend untuk Production
```bash
cd frontend
yarn build

# Serve dengan simple HTTP server
npx serve -s build -l 3000
```

### Run Backend dengan Gunicorn
```bash
cd backend
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker server:app --bind 0.0.0.0:8001
```

## 📱 Access URLs

Setelah semua berjalan dengan baik:

- **Frontend Application**: http://localhost:3000
- **Backend API**: http://localhost:8001
- **API Documentation**: http://localhost:8001/docs
- **MongoDB (jika ada Compass)**: mongodb://localhost:27017

## 🎉 Success Checklist

Pastikan semua item berikut ✅ sebelum mulai menggunakan aplikasi:

- ✅ MongoDB service berjalan
- ✅ Backend server running di port 8001
- ✅ Frontend dev server running di port 3000
- ✅ Dapat mengakses http://localhost:3000
- ✅ API health check berhasil (/api/status)
- ✅ Dapat membuat tetrahedron pairs
- ✅ Dapat menjalankan simulasi
- ✅ Dapat melihat pair analysis details

## 📞 Need Help?

Jika mengalami kesulitan:

1. **Check semua prerequisites** sudah terinstall dengan benar
2. **Verify port availability** (8001 dan 3000)  
3. **Check firewall/antivirus** tidak memblock aplikasi
4. **Restart services** MongoDB → Backend → Frontend
5. **Check logs** untuk error messages yang spesifik

---

**🎯 Selamat! Tetracore Server Simulation sudah siap digunakan di localhost Anda!**

Mulai eksplorasi simulasi Counter-Tetrahedron Pairing System berdasarkan teori Methane Metauniverse! 🌌