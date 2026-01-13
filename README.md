# 🔐 Privacy-Preserving Virtual Identity System

A privacy-first system for generating temporary, one-time-use virtual identities that prove verification status without exposing sensitive government identifiers.

## ⚠️ IMPORTANT DISCLAIMER

**THIS IS AN EDUCATIONAL/MVP SYSTEM FOR DEMONSTRATION PURPOSES ONLY**

- ✅ Demonstrates privacy-preserving identity concepts
- ✅ Shows secure cryptographic techniques
- ✅ Implements zero-knowledge proof principles
- ❌ **NOT** integrated with real Aadhaar or PAN APIs
- ❌ **NOT** affiliated with or endorsed by any government entity
- ❌ **NOT** for production use with real government data
- ❌ **NEVER** use with actual Aadhaar or PAN numbers

All identity verification in this system is **SIMULATED** for educational purposes.

## 🎯 Features

### Privacy-by-Design
- **Never stores** Aadhaar or PAN numbers
- **Only stores** verification flags and non-reversible hashes
- **Minimal data disclosure** - only name (masked), age group, and verification status
- **Zero-knowledge** approach to identity verification

### Temporary Virtual IDs
- **12-digit cryptographically secure** identifiers
- **One-time use** - automatically invalidated after verification
- **Time-limited** - expires after 1 hour
- **Revocable** - users can instantly revoke VIDs
- **QR code** - signed with HMAC for tamper protection

### Security Features
- **JWT authentication** for user sessions
- **Bcrypt password hashing** with 12 rounds
- **HMAC-SHA256 signatures** for QR codes
- **Rate limiting** on verification endpoints
- **Audit logging** with privacy-preserving hashed identifiers
- **Security headers** (HSTS, X-Frame-Options, etc.)

## 🏗️ Architecture

### Backend (FastAPI)
```
backend/
├── main.py              # FastAPI application entry point
├── config.py            # Configuration management
├── database.py          # SQLAlchemy setup
├── models/              # Database models
│   ├── user.py          # User model (verification flags only)
│   ├── virtual_id.py    # Virtual ID model
│   └── audit_log.py     # Audit log model
├── routes/              # API endpoints
│   ├── auth.py          # Registration & login
│   ├── verification.py  # Simulated Aadhaar/PAN verification
│   ├── virtual_id.py    # VID generation & management
│   └── verify_vid.py    # Public VID verification
├── auth/                # Authentication utilities
│   ├── jwt_handler.py   # JWT token management
│   └── password.py      # Password hashing
├── security/            # Security utilities
│   └── crypto.py        # VID generation, hashing, signing
└── schemas/             # Pydantic schemas
    ├── user.py
    ├── verification.py
    └── virtual_id.py
```

### Frontend (HTML/CSS/JS)
```
frontend/
├── index.html           # Landing page
├── register.html        # User registration
├── login.html           # User login
├── dashboard.html       # User dashboard
├── verify-identity.html # Identity verification (simulated)
├── generate-vid.html    # VID generation with QR code
├── verify-vid.html      # Public VID verification
├── styles.css           # Responsive CSS
└── app.js               # API client & utilities
```

### Database Schema
```sql
users:
  - id (UUID)
  - email (unique)
  - password_hash
  - name
  - aadhaar_verified (boolean)
  - pan_verified (boolean)
  - aadhaar_hash (SHA-256)
  - pan_hash (SHA-256)

virtual_ids:
  - vid (12-digit string)
  - user_id (FK to users)
  - created_at
  - expires_at
  - usage_limit (default: 1)
  - usage_count
  - revoked (boolean)

audit_logs:
  - id
  - vid_hash (SHA-256)
  - ip_hash (SHA-256)
  - action (enum)
  - result
  - timestamp
```

## 🚀 Setup Instructions

### Prerequisites
- Python 3.10+
- Node.js (for serving frontend)
- Modern web browser with camera (for QR scanning)

### Backend Setup

1. **Navigate to backend directory**
```bash
cd HTP/backend
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Create environment file**
```bash
cp ../.env.example .env
```

5. **Generate secret keys**
```bash
python -c "import secrets; print('JWT_SECRET_KEY=' + secrets.token_urlsafe(32))"
python -c "import secrets; print('HMAC_SECRET_KEY=' + secrets.token_urlsafe(32))"
```

Add these to your `.env` file.

6. **Run the backend**
```bash
python main.py
```

Backend will run on `http://localhost:8000`

API documentation available at `http://localhost:8000/docs`

### Frontend Setup

1. **Navigate to frontend directory**
```bash
cd HTP/frontend
```

2. **Serve with Python's HTTP server**
```bash
python -m http.server 3000
```

Or use any static file server:
```bash
npx serve -p 3000
```

Frontend will run on `http://localhost:3000`

## 📖 Usage Guide

### 1. Register & Login
1. Visit `http://localhost:3000`
2. Click "Get Started" to register
3. Enter name, email, and password
4. You'll be automatically logged in

### 2. Verify Identity (Simulated)
1. Go to dashboard
2. Click "Verify Identity"
3. Enter any 12-digit number for Aadhaar
4. Enter any 6-digit OTP
5. Enter any valid PAN format (e.g., ABCDE1234F)
6. Both verifications will succeed (simulated)

### 3. Generate Virtual ID
1. After verification, click "Generate Virtual ID"
2. A 12-digit VID and QR code will be generated
3. VID expires in 1 hour
4. Valid for one-time use only

### 4. Share & Verify
1. Share the VID number or QR code
2. Recipient visits `verify-vid.html`
3. Scans QR code or enters VID manually
4. System shows minimal information:
   - Masked name (e.g., "John D***")
   - Age group (e.g., "18+")
   - Verification status (Aadhaar ✅, PAN ✅)
5. VID is marked as used and cannot be reused

### 5. Revoke VID
- Click "Revoke VID" on the generation page
- VID becomes immediately invalid

## 🔒 Security Model

### What We Store
- ✅ User email and hashed password
- ✅ Verification flags (boolean)
- ✅ SHA-256 hashes of Aadhaar/PAN (non-reversible)
- ✅ Virtual IDs with expiry and usage tracking
- ✅ Audit logs with hashed identifiers

### What We NEVER Store
- ❌ Plaintext Aadhaar numbers
- ❌ Plaintext PAN numbers
- ❌ Any reversible encryption of sensitive data
- ❌ Full names in verification responses
- ❌ Birthdates or exact ages
- ❌ Addresses or other PII

### Cryptographic Techniques
- **Password Hashing**: Bcrypt with 12 rounds
- **Identifier Hashing**: SHA-256 (one-way)
- **QR Signing**: HMAC-SHA256 (tamper-proof)
- **VID Generation**: Cryptographically secure random (secrets module)
- **JWT Tokens**: HS256 algorithm

### Attack Prevention
- **Replay Attacks**: One-time use VIDs
- **Tampering**: HMAC signatures on QR codes
- **Brute Force**: Rate limiting on verification
- **SQL Injection**: Parameterized queries (SQLAlchemy)
- **XSS**: Input validation and sanitization
- **CSRF**: CORS configuration

## 📊 API Documentation

### Authentication Endpoints

#### POST /auth/register
Register a new user
```json
Request:
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "securepassword123"
}

Response:
{
  "access_token": "eyJ...",
  "token_type": "bearer",
  "user": {
    "id": "uuid",
    "email": "john@example.com",
    "name": "John Doe",
    "aadhaar_verified": false,
    "pan_verified": false
  }
}
```

#### POST /auth/login
Login with credentials
```json
Request:
{
  "email": "john@example.com",
  "password": "securepassword123"
}

Response: Same as register
```

### Verification Endpoints (Requires Auth)

#### POST /verify/aadhaar
Simulate Aadhaar verification
```json
Request:
{
  "aadhaar_number": "123456789012",
  "otp": "123456"
}

Response:
{
  "success": true,
  "message": "Aadhaar verification successful (SIMULATED)",
  "verified": true
}
```

#### POST /verify/pan
Simulate PAN verification
```json
Request:
{
  "pan_number": "ABCDE1234F"
}

Response:
{
  "success": true,
  "message": "PAN verification successful (SIMULATED)",
  "verified": true
}
```

### VID Management (Requires Auth)

#### POST /vid/generate
Generate a new Virtual ID
```json
Response:
{
  "vid": "123456789012",
  "qr_payload": {
    "vid": "123456789012",
    "expires_at": "2026-01-13T11:46:00",
    "signature": "abc123..."
  },
  "expires_at": "2026-01-13T11:46:00",
  "usage_limit": 1
}
```

#### GET /vid/list
List user's VIDs

#### POST /vid/revoke/{vid}
Revoke a VID

### Public Verification

#### POST /verify-vid
Verify a VID (PUBLIC - no auth required)
```json
Request:
{
  "vid": "123456789012"
  // OR
  "qr_payload": { ... }
}

Response (Valid):
{
  "valid": true,
  "message": "VID verified successfully",
  "name": "John D***",
  "age_group": "18+",
  "aadhaar_verified": true,
  "pan_verified": true
}

Response (Invalid):
{
  "valid": false,
  "message": "VID has expired"
}
```

## 🚢 Deployment

### Free Tier Options

#### Backend
- **Render**: Free tier with 750 hours/month
- **Railway**: Free tier with $5 credit
- **Fly.io**: Free tier available

#### Frontend
- **Netlify**: Free tier for static sites
- **Vercel**: Free tier for static sites
- **GitHub Pages**: Free hosting

### Docker Deployment

Create `Dockerfile`:
```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install -r requirements.txt

COPY backend/ .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t vid-system .
docker run -p 8000:8000 vid-system
```

## 🔮 Future Enhancements

### Production Readiness
- [ ] Integrate with real Aadhaar API (UIDAI)
- [ ] Integrate with real PAN API (Income Tax Dept)
- [ ] Add PostgreSQL for production database
- [ ] Add Redis for rate limiting and caching
- [ ] Implement proper session management
- [ ] Add email verification
- [ ] Add 2FA for user accounts

### Features
- [ ] Mobile app (React Native)
- [ ] Biometric verification
- [ ] Multi-use VIDs with configurable limits
- [ ] VID analytics dashboard
- [ ] Webhook notifications
- [ ] API key management for third-party integrations

### Security
- [ ] Penetration testing
- [ ] Security audit
- [ ] GDPR compliance
- [ ] SOC 2 compliance
- [ ] Bug bounty program

## 📜 License

This project is for educational purposes only. See [LEGAL.md](LEGAL.md) for full legal disclaimer.

## 🤝 Contributing

This is an educational project. Contributions are welcome for:
- Security improvements
- Documentation enhancements
- Bug fixes
- Feature suggestions

## 📞 Support

For questions or issues, please open a GitHub issue.

---

**Remember**: This system is for EDUCATIONAL purposes only. Never use it with real Aadhaar or PAN numbers.
