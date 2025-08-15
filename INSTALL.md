# Tetracore Server Simulation - Installation Guide

Panduan instalasi untuk aplikasi simulasi **Counter-Tetrahedron Pairing System** berdasarkan teori Methane Metauniverse (MMU).

## 📋 Prerequisites

### System Requirements
- **Operating System**: Linux, macOS, atau Windows 10/11
- **Python**: 3.8 atau lebih baru
- **Node.js**: 16 atau lebih baru
- **MongoDB**: 4.4 atau lebih baru
- **Memory**: Minimum 4GB RAM
- **Storage**: Minimum 2GB free space

### Dependencies
- Docker (opsional, untuk deployment)
- Git
- Yarn package manager

## 🚀 Installation Steps

### 1. Clone Repository

```bash
git clone https://github.com/your-username/tetracore-server.git
cd tetracore-server
```

### 2. Backend Setup

#### Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

#### Setup Environment Variables

Buat file `.env` di direktori `backend/`:

```bash
# backend/.env
MONGO_URL="mongodb://localhost:27017"
DB_NAME="tetracore_db"
CORS_ORIGINS="*"
```

#### Install MongoDB

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install mongodb
sudo systemctl start mongodb
sudo systemctl enable mongodb
```

**macOS (dengan Homebrew):**
```bash
brew tap mongodb/brew
brew install mongodb-community
brew services start mongodb/brew/mongodb-community
```

**Windows:**
1. Download MongoDB Community Server dari [mongodb.com](https://www.mongodb.com/try/download/community)
2. Jalankan installer dan ikuti petunjuk
3. Start MongoDB service

### 3. Frontend Setup

#### Install Node.js Dependencies

```bash
cd ../frontend
yarn install
```

#### Setup Environment Variables

Buat file `.env` di direktori `frontend/`:

```bash
# frontend/.env
REACT_APP_BACKEND_URL=http://localhost:8001
WDS_SOCKET_PORT=443
```

### 4. Verify Installation

#### Test Backend

```bash
cd backend
python server.py
```

Backend akan berjalan di `http://localhost:8001`

#### Test Frontend

```bash
cd frontend
yarn start
```

Frontend akan berjalan di `http://localhost:3000`

## ⚙️ Configuration

### Database Configuration

1. **MongoDB Connection**: Pastikan MongoDB berjalan di port default (27017)
2. **Database Name**: Aplikasi akan membuat database `tetracore_db` secara otomatis
3. **Collections**: Collection `tetrahedron_pairs` akan dibuat saat pair pertama disimpan

### Network Configuration

1. **Backend Port**: Default 8001 (dapat diubah di server.py)
2. **Frontend Port**: Default 3000 (dapat diubah di package.json)
3. **CORS**: Dikonfigurasi untuk mengizinkan semua origin (development mode)

## 🏃‍♂️ Running the Application

### Development Mode

#### Terminal 1 - Backend
```bash
cd backend
python server.py
```

#### Terminal 2 - Frontend
```bash
cd frontend
yarn start
```

### Production Mode

#### Build Frontend
```bash
cd frontend
yarn build
```

#### Run with Production Server
```bash
cd backend
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker server:app --bind 0.0.0.0:8001
```

## 🐳 Docker Deployment (Optional)

### Create Dockerfile for Backend

```dockerfile
# backend/Dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8001

CMD ["python", "server.py"]
```

### Create Dockerfile for Frontend

```dockerfile
# frontend/Dockerfile
FROM node:16-alpine

WORKDIR /app
COPY package.json yarn.lock ./
RUN yarn install

COPY . .
RUN yarn build

FROM nginx:alpine
COPY --from=0 /app/build /usr/share/nginx/html
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

### Docker Compose

```yaml
# docker-compose.yml
version: '3.8'

services:
  mongodb:
    image: mongo:4.4
    ports:
      - "27017:27017"
    volumes:
      - mongodb_data:/data/db

  backend:
    build: ./backend
    ports:
      - "8001:8001"
    environment:
      - MONGO_URL=mongodb://mongodb:27017
      - DB_NAME=tetracore_db
    depends_on:
      - mongodb

  frontend:
    build: ./frontend
    ports:
      - "3000:80"
    depends_on:
      - backend

volumes:
  mongodb_data:
```

### Run with Docker Compose

```bash
docker-compose up -d
```

## 📱 Usage Instructions

### 1. Membuat Tetrahedron Pairs

1. Buka aplikasi di browser
2. Klik tombol "Create Pair" untuk membuat pasangan matter-antimatter
3. Pair akan muncul dalam visualisasi dengan indikator stabilitas

### 2. Menjalankan Simulasi

1. Klik tombol "Start" untuk memulai simulasi
2. Amati perubahan energy state dan oscillation dalam real-time
3. Klik "Stop" untuk menghentikan simulasi

### 3. Analisis Detail

1. Klik pada pair tetrahedron untuk melihat detail
2. Panel analysis akan menampilkan:
   - Energy state matter dan antimatter
   - Frequency dan phase oscillation
   - Pairing strength dan entanglement status

### 4. Management System

- **Reset**: Hapus semua pairs dan reset simulasi
- **Delete**: Hapus pair individual dengan tombol delete (X)
- **Monitor**: Pantau system stability dan energy secara real-time

## 🔧 API Endpoints

### Basic Endpoints
- `GET /api/status` - Status server
- `GET /api/simulation/state` - State simulasi saat ini

### Simulation Control
- `POST /api/simulation/start` - Mulai simulasi
- `POST /api/simulation/stop` - Hentikan simulasi  
- `POST /api/simulation/reset` - Reset simulasi

### Tetrahedron Pairs
- `GET /api/pairs` - Ambil semua pairs
- `POST /api/pairs/create` - Buat pair baru
- `GET /api/pairs/{id}` - Ambil pair specific
- `DELETE /api/pairs/{id}` - Hapus pair

### WebSocket
- `WS /api/ws` - Real-time updates

## 🐛 Troubleshooting

### Common Issues

#### 1. MongoDB Connection Error
```
Error: Connection refused to MongoDB
```
**Solution:**
- Pastikan MongoDB service berjalan
- Check connection string di `.env`
- Verify port 27017 tidak digunakan aplikasi lain

#### 2. Frontend tidak dapat connect ke Backend
```
Error: Network Error / CORS Error
```
**Solution:**
- Pastikan backend berjalan di port 8001
- Check `REACT_APP_BACKEND_URL` di frontend/.env
- Verify CORS configuration di backend

#### 3. WebSocket Connection Failed
```
WebSocket connection failed
```
**Solution:**
- Check firewall settings
- Verify WebSocket support di deployment environment
- Fallback ke periodic refresh (sudah implemented)

#### 4. Package Installation Errors
```
Error: Package not found
```
**Solution:**
```bash
# Clear cache dan reinstall
rm -rf node_modules package-lock.json
yarn install

# Python packages
pip install --upgrade pip
pip install -r requirements.txt
```

### Performance Issues

#### High Memory Usage
- Batasi jumlah tetrahedron pairs (max 50 untuk optimal performance)
- Monitor system resources saat simulasi berjalan
- Gunakan production build untuk frontend

#### Slow Response Time
- Check MongoDB indexes
- Optimize simulation update frequency
- Use connection pooling untuk database

## 🔒 Security Considerations

### Production Deployment

1. **Environment Variables**: Jangan commit file `.env` ke repository
2. **CORS**: Konfigurasi specific origins untuk production
3. **Database**: Gunakan user authentication untuk MongoDB
4. **HTTPS**: Gunakan SSL certificate untuk production
5. **Firewall**: Batasi akses ke port database

### Secure Configuration

```bash
# backend/.env (production)
MONGO_URL="mongodb://username:password@localhost:27017/tetracore_db"
DB_NAME="tetracore_db"
CORS_ORIGINS="https://yourdomain.com,https://www.yourdomain.com"
SECRET_KEY="your-secure-secret-key"
```

## 📚 Scientific Background

Aplikasi ini berdasarkan pada **Methane Metauniverse (MMU) theory** oleh Jürgen Wollbold:

- **Paper**: "The Methane Metauniverse (MMU) A Geometric Explanation of Antiparticles, Entanglement, and Time"
- **DOI**: 10.17605/OSF.IO/MK3XR
- **Konsep**: Reality sebagai fractal elastic lattice dari tetrahedra
- **Implementation**: Counter-tetrahedron stabilization system

### Key Concepts Implemented

1. **Tetrahedron Geometry**: Regular tetrahedron sebagai basic building block
2. **Four Dimensions**: w₁ (projection), w₂ (energy), w₃ (spin), w₄ (mass)
3. **Matter-Antimatter Pairs**: Stabilization melalui counter-tetrahedron
4. **Entanglement**: Physical connection antara paired nodes
5. **Time Oscillation**: Internal vibrations projected sebagai observable time

## 📞 Support

Untuk pertanyaan dan dukungan:

- **Issues**: Submit di GitHub repository
- **Documentation**: Referensi ke MMU paper original
- **Community**: Join discussions tentang theoretical physics implementation

## 📄 License

Project ini menggunakan MIT License. See LICENSE file untuk detail.

---

**Created with ❤️ for advancing theoretical physics simulation**