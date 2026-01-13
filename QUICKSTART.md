# 🚀 Quick Start Guide

## Privacy-Preserving Virtual Identity System

### ⚡ 5-Minute Setup

#### Step 1: Start the Backend

```bash
cd HTP
./start-backend.sh
```

The script will:
- ✅ Activate virtual environment
- ✅ Install dependencies (if needed)
- ✅ Generate secret keys
- ✅ Create `.env` file
- ✅ Start server on http://localhost:8000

#### Step 2: Start the Frontend (New Terminal)

```bash
cd HTP
./start-frontend.sh
```

Frontend will run on http://localhost:3000

#### Step 3: Use the System

1. **Open Browser**: http://localhost:3000

2. **Register**:
   - Click "Get Started"
   - Enter name, email, password
   - You'll be logged in automatically

3. **Verify Identity** (Simulated):
   - Go to "Verify Identity"
   - Aadhaar: Enter any 12 digits (e.g., `123456789012`)
   - OTP: Enter any 6 digits (e.g., `123456`)
   - PAN: Enter valid format (e.g., `ABCDE1234F`)
   - Click verify for each

4. **Generate VID**:
   - Click "Generate Virtual ID"
   - You'll get a 12-digit VID and QR code
   - Expires in 1 hour
   - One-time use

5. **Verify VID** (As a stranger):
   - Open http://localhost:3000/verify-vid.html
   - Scan QR code OR enter VID manually
   - See minimal info: masked name, age group, verification status

6. **Revoke VID**:
   - Click "Revoke VID" on generation page
   - VID becomes immediately invalid

### 📚 Documentation

- **Full Guide**: [README.md](README.md)
- **Architecture**: [ARCHITECTURE.md](ARCHITECTURE.md)
- **Legal**: [LEGAL.md](LEGAL.md)
- **API Docs**: http://localhost:8000/docs (when backend running)

### ⚠️ Important Reminders

> [!WARNING]
> **EDUCATIONAL USE ONLY**
> - This system simulates Aadhaar/PAN verification
> - NOT for production use with real data
> - NOT affiliated with any government entity

### 🐛 Troubleshooting

**Backend won't start?**
```bash
cd HTP/backend
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

**Frontend won't start?**
```bash
cd HTP/frontend
python3 -m http.server 3000
```

**Port already in use?**
- Backend: Change port in `backend/main.py` (line with `uvicorn.run`)
- Frontend: Use different port: `python3 -m http.server 8080`

### 🎯 What to Try

1. ✅ Create multiple users
2. ✅ Generate multiple VIDs
3. ✅ Test VID expiry (wait 1 hour)
4. ✅ Test one-time use (verify same VID twice)
5. ✅ Test revocation
6. ✅ Check audit logs in database
7. ✅ Explore API docs at /docs

### 📁 Project Structure

```
HTP/
├── backend/          # FastAPI backend
├── frontend/         # HTML/CSS/JS frontend
├── README.md         # Full documentation
├── LEGAL.md          # Legal disclaimer
├── ARCHITECTURE.md   # System architecture
├── start-backend.sh  # Backend launcher
└── start-frontend.sh # Frontend launcher
```

### 🔐 Security Features

- ✅ Never stores Aadhaar/PAN numbers
- ✅ Bcrypt password hashing
- ✅ JWT authentication
- ✅ HMAC-signed QR codes
- ✅ One-time use VIDs
- ✅ Auto-expiring identifiers
- ✅ Privacy-preserving audit logs

### 🎓 Learning Points

This system demonstrates:
- Privacy-by-design architecture
- Cryptographic security (hashing, signing)
- Virtual identity concepts
- Full-stack web development
- API design with FastAPI
- Modern frontend development

---

**Ready to start?** Run `./start-backend.sh` and `./start-frontend.sh`!
