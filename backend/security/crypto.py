"""
Cryptographic utilities for VID generation and QR code signing.

This module provides:
- Secure VID generation
- SHA-256 hashing for identifiers
- HMAC-SHA256 signing for QR codes
- Signature verification
"""

import secrets
import hashlib
import hmac
import json
from datetime import datetime
from typing import Dict, Optional, Tuple
from config import settings


def generate_vid() -> str:
    """
    Generate a cryptographically secure 12-digit VID.
    
    Uses secrets module for cryptographically strong random numbers.
    Ensures the VID is exactly 12 digits.
    
    Returns:
        12-digit VID as string
    """
    # Generate a random number between 100000000000 and 999999999999
    vid = secrets.randbelow(900000000000) + 100000000000
    return str(vid)


def hash_identifier(identifier: str) -> str:
    """
    Hash an identifier using SHA-256.
    
    Used for storing non-reversible hashes of Aadhaar, PAN, VIDs, and IPs.
    
    Args:
        identifier: String to hash
        
    Returns:
        Hexadecimal SHA-256 hash (64 characters)
    """
    return hashlib.sha256(identifier.encode()).hexdigest()


def sign_qr_data(data: str) -> str:
    """
    Sign data using HMAC-SHA256.
    
    Creates a tamper-proof signature for QR code data.
    
    Args:
        data: Data to sign (typically JSON string)
        
    Returns:
        Hexadecimal HMAC signature
    """
    signature = hmac.new(
        settings.hmac_secret_key.encode(),
        data.encode(),
        hashlib.sha256
    ).hexdigest()
    
    return signature


def verify_qr_signature(data: str, signature: str) -> bool:
    """
    Verify HMAC signature of QR code data.
    
    Args:
        data: Original data
        signature: Signature to verify
        
    Returns:
        True if signature is valid, False otherwise
    """
    expected_signature = sign_qr_data(data)
    
    # Use constant-time comparison to prevent timing attacks
    return hmac.compare_digest(expected_signature, signature)


def generate_qr_payload(vid: str, expires_at: datetime) -> Dict[str, str]:
    """
    Generate a signed QR code payload.
    
    Creates a JSON payload containing:
    - VID
    - Expiry timestamp
    - HMAC signature for tamper protection
    
    Args:
        vid: Virtual ID
        expires_at: Expiry datetime
        
    Returns:
        Dictionary with vid, expires_at (ISO format), and signature
    """
    # Create the data to sign (without signature)
    data = {
        "vid": vid,
        "expires_at": expires_at.isoformat()
    }
    
    # Convert to canonical JSON string for signing
    data_str = json.dumps(data, sort_keys=True)
    
    # Generate signature
    signature = sign_qr_data(data_str)
    
    # Return complete payload
    return {
        "vid": vid,
        "expires_at": expires_at.isoformat(),
        "signature": signature
    }


def verify_qr_payload(payload: Dict[str, str]) -> Tuple[bool, Optional[str]]:
    """
    Verify a QR code payload's signature.
    
    Args:
        payload: Dictionary with vid, expires_at, and signature
        
    Returns:
        Tuple of (is_valid, error_message)
        - (True, None) if valid
        - (False, error_message) if invalid
    """
    # Check required fields
    required_fields = ["vid", "expires_at", "signature"]
    for field in required_fields:
        if field not in payload:
            return False, f"Missing required field: {field}"
    
    # Extract signature
    signature = payload["signature"]
    
    # Reconstruct data without signature
    data = {
        "vid": payload["vid"],
        "expires_at": payload["expires_at"]
    }
    data_str = json.dumps(data, sort_keys=True)
    
    # Verify signature
    if not verify_qr_signature(data_str, signature):
        return False, "Invalid signature - QR code may be tampered"
    
    return True, None
