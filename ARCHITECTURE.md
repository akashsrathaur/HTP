# System Architecture

## Overview

The Privacy-Preserving Virtual Identity System is designed with a **privacy-by-design** architecture that ensures sensitive government identifiers are never stored or exposed.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐       │
│  │ Register │  │  Login   │  │Dashboard │  │ Verify   │       │
│  │          │  │          │  │          │  │ Identity │       │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘       │
│  ┌──────────┐  ┌──────────┐                                    │
│  │Generate  │  │ Verify   │                                    │
│  │   VID    │  │   VID    │  (Public)                         │
│  └──────────┘  └──────────┘                                    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ HTTPS
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      FASTAPI BACKEND                            │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    API ROUTES                             │  │
│  │  /auth/*  /verify/*  /vid/*  /verify-vid                 │  │
│  └──────────────────────────────────────────────────────────┘  │
│                              │                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                  MIDDLEWARE                               │  │
│  │  - CORS                                                   │  │
│  │  - Security Headers                                       │  │
│  │  - Rate Limiting                                          │  │
│  │  - JWT Authentication                                     │  │
│  └──────────────────────────────────────────────────────────┘  │
│                              │                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │               BUSINESS LOGIC                              │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐      │  │
│  │  │    Auth     │  │ Verification│  │     VID     │      │  │
│  │  │  (JWT/PWD)  │  │ (Simulated) │  │ Management  │      │  │
│  │  └─────────────┘  └─────────────┘  └─────────────┘      │  │
│  └──────────────────────────────────────────────────────────┘  │
│                              │                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                SECURITY LAYER                             │  │
│  │  - Password Hashing (bcrypt)                              │  │
│  │  - Identifier Hashing (SHA-256)                           │  │
│  │  - QR Signing (HMAC-SHA256)                               │  │
│  │  - VID Generation (secrets)                               │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      DATABASE (SQLite/PostgreSQL)               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │    users     │  │ virtual_ids  │  │ audit_logs   │         │
│  │              │  │              │  │              │         │
│  │ - id         │  │ - vid        │  │ - vid_hash   │         │
│  │ - email      │  │ - user_id    │  │ - action     │         │
│  │ - pwd_hash   │  │ - expires_at │  │ - timestamp  │         │
│  │ - name       │  │ - used       │  │ - ip_hash    │         │
│  │ - *_verified │  │ - revoked    │  │              │         │
│  │ - *_hash     │  │              │  │              │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
└─────────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. Frontend Layer

**Technology**: HTML5, CSS3, Vanilla JavaScript

**Components**:
- **Landing Page**: Marketing and information
- **Authentication**: Register/Login forms
- **Dashboard**: User overview and VID management
- **Identity Verification**: Simulated Aadhaar/PAN verification
- **VID Generation**: Create VIDs with QR codes
- **VID Verification**: Public verification interface with QR scanner

**Key Features**:
- Responsive design
- QR code generation (qrcode.js)
- QR code scanning (html5-qrcode)
- JWT token storage in localStorage
- API client for backend communication

### 2. API Layer

**Technology**: FastAPI (Python)

**Endpoints**:

#### Authentication
- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `GET /auth/me` - Get current user

#### Verification (Simulated)
- `POST /verify/aadhaar` - Simulate Aadhaar verification
- `POST /verify/pan` - Simulate PAN verification

#### VID Management
- `POST /vid/generate` - Generate new VID
- `GET /vid/list` - List user's VIDs
- `POST /vid/revoke/{vid}` - Revoke a VID

#### Public Verification
- `POST /verify-vid` - Verify a VID (no auth required)

### 3. Business Logic Layer

#### Authentication Module
- User registration with email validation
- Password hashing with bcrypt (12 rounds)
- JWT token generation and validation
- Session management

#### Verification Module (Simulated)
- Format validation for Aadhaar (12 digits)
- Format validation for PAN (ABCDE1234F pattern)
- Stores only verification flags and hashes
- **Never stores actual numbers**

#### VID Management Module
- Cryptographically secure VID generation
- QR code payload creation with HMAC signature
- Expiry management (default: 1 hour)
- Usage tracking (default: one-time use)
- Revocation support

#### Verification Module
- QR signature validation
- Expiry checking
- Usage limit enforcement
- Minimal data disclosure
- Audit logging

### 4. Security Layer

#### Cryptographic Functions

**Password Hashing**:
```python
bcrypt.hash(password, rounds=12)
```

**Identifier Hashing**:
```python
SHA-256(identifier) -> 64-char hex
```

**QR Signing**:
```python
HMAC-SHA256(data, secret_key) -> signature
```

**VID Generation**:
```python
secrets.randbelow(900000000000) + 100000000000
```

#### Security Measures
- **Input Validation**: Pydantic schemas
- **SQL Injection Prevention**: SQLAlchemy ORM
- **XSS Prevention**: Input sanitization
- **CSRF Protection**: CORS configuration
- **Rate Limiting**: Per-IP limits on verification
- **Audit Logging**: All VID operations logged

### 5. Data Layer

#### Database Models

**User Model**:
```python
class User:
    id: UUID
    email: str (unique)
    password_hash: str
    name: str
    aadhaar_verified: bool
    pan_verified: bool
    aadhaar_hash: str (SHA-256)
    pan_hash: str (SHA-256)
    created_at: datetime
```

**VirtualID Model**:
```python
class VirtualID:
    vid: str (12 digits, primary key)
    user_id: UUID (foreign key)
    created_at: datetime
    expires_at: datetime
    usage_limit: int (default: 1)
    usage_count: int
    revoked: bool
```

**AuditLog Model**:
```python
class AuditLog:
    id: int
    vid_hash: str (SHA-256)
    ip_hash: str (SHA-256)
    action: enum (created, verified, expired, revoked)
    result: str
    timestamp: datetime
```

## Data Flow Diagrams

### VID Generation Flow

```
User (Authenticated)
    │
    ├─> POST /vid/generate
    │
    ▼
Backend
    │
    ├─> Check: Aadhaar verified?
    ├─> Check: PAN verified?
    │
    ├─> Generate 12-digit VID (cryptographically secure)
    ├─> Set expiry (now + 1 hour)
    ├─> Create VID record in DB
    │
    ├─> Generate QR payload:
    │   {
    │     vid: "123456789012",
    │     expires_at: "2026-01-13T11:46:00",
    │     signature: HMAC-SHA256(vid + expires_at)
    │   }
    │
    ├─> Create audit log
    │
    ▼
Response to User
    {
      vid: "123456789012",
      qr_payload: { ... },
      expires_at: "2026-01-13T11:46:00"
    }
```

### VID Verification Flow

```
Anyone (Public, No Auth)
    │
    ├─> POST /verify-vid
    │   { vid: "123456789012" }
    │   OR
    │   { qr_payload: { ... } }
    │
    ▼
Backend
    │
    ├─> If QR payload: Verify HMAC signature
    │   └─> Invalid? Return error
    │
    ├─> Find VID in database
    │   └─> Not found? Return error
    │
    ├─> Check: Revoked?
    │   └─> Yes? Return error
    │
    ├─> Check: Expired?
    │   └─> Yes? Return error
    │
    ├─> Check: Usage limit reached?
    │   └─> Yes? Return error
    │
    ├─> Increment usage_count
    ├─> Get user info
    ├─> Create audit log
    │
    ▼
Response
    {
      valid: true,
      name: "John D***",        // Masked
      age_group: "18+",
      aadhaar_verified: true,
      pan_verified: true
    }
```

## Privacy-Preserving Techniques

### 1. Data Minimization
- Only collect essential data
- No storage of government identifiers
- Minimal disclosure in verification

### 2. Hashing (One-Way)
- SHA-256 for identifiers
- Cannot reverse to original
- Used for audit and deduplication only

### 3. Temporary Identifiers
- VIDs expire after 1 hour
- One-time use by default
- User-revocable

### 4. Cryptographic Signatures
- HMAC-SHA256 for QR codes
- Prevents tampering
- Verifiable without exposing secrets

### 5. Masked Data Disclosure
- Names: "John D***"
- Age: "18+" (group, not exact)
- Only verification status, not details

## Scalability Considerations

### Current (MVP)
- SQLite database
- In-memory rate limiting
- Single server deployment

### Production Enhancements
- PostgreSQL with connection pooling
- Redis for rate limiting and caching
- Load balancer for multiple instances
- CDN for frontend assets
- Database replication
- Horizontal scaling with stateless API

## Security Hardening

### Current
- HTTPS recommended
- Security headers
- JWT authentication
- Password hashing
- Input validation

### Production Enhancements
- WAF (Web Application Firewall)
- DDoS protection
- Intrusion detection
- Security monitoring
- Regular penetration testing
- Bug bounty program

## Monitoring & Observability

### Recommended
- Application logs
- Error tracking (Sentry)
- Performance monitoring (New Relic)
- Uptime monitoring
- Database query analysis
- Audit log analysis

---

**Last Updated**: January 13, 2026
