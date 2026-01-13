"""
Privacy-Preserving Virtual Identity System
Main FastAPI application entry point.

IMPORTANT LEGAL NOTICE:
This system is for EDUCATIONAL/MVP purposes only.
It simulates Aadhaar and PAN verification.
It does NOT integrate with official government APIs.
It is NOT affiliated with or endorsed by any government entity.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from contextlib import asynccontextmanager

from database import init_db
from routes import auth_router, verification_router, virtual_id_router, verify_vid_router
from config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events.
    """
    # Startup: Initialize database
    await init_db()
    print("✅ Database initialized")
    yield
    # Shutdown: cleanup if needed
    print("👋 Shutting down")


# Create FastAPI app
app = FastAPI(
    title="Privacy-Preserving Virtual Identity System",
    description="""
    A privacy-first system for generating temporary virtual identities.
    
    ⚠️ **IMPORTANT DISCLAIMER**:
    - This is an EDUCATIONAL/MVP system
    - Aadhaar and PAN verification are SIMULATED
    - NOT affiliated with any government entity
    - NOT for production use with real government data
    
    🔒 **Privacy Features**:
    - Never stores Aadhaar or PAN numbers
    - Only stores verification flags and hashes
    - Temporary, one-time-use Virtual IDs
    - Cryptographically signed QR codes
    - Minimal data disclosure
    """,
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security headers middleware
@app.middleware("http")
async def add_security_headers(request, call_next):
    """Add security headers to all responses."""
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response


# Register routers
app.include_router(auth_router)
app.include_router(verification_router)
app.include_router(virtual_id_router)
app.include_router(verify_vid_router)


@app.get("/")
async def root():
    """Root endpoint with system information."""
    return {
        "message": "Privacy-Preserving Virtual Identity System",
        "version": "1.0.0",
        "status": "operational",
        "disclaimer": "EDUCATIONAL USE ONLY - Simulated verification",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
