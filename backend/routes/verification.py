"""
Identity verification routes (SIMULATED).

IMPORTANT: These endpoints simulate Aadhaar and PAN verification.
In production, these would integrate with official government APIs.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from models.user import User
from schemas.verification import AadhaarVerifyRequest, PANVerifyRequest, VerificationResponse
from security.crypto import hash_identifier
from routes.auth import get_current_user


router = APIRouter(prefix="/verify", tags=["Identity Verification"])


@router.post("/aadhaar", response_model=VerificationResponse)
async def verify_aadhaar(
    request: AadhaarVerifyRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Simulate Aadhaar verification.
    
    SIMULATED: In production, this would:
    1. Send OTP to Aadhaar-linked mobile
    2. Verify OTP with UIDAI
    3. Receive verification response
    
    Current behavior:
    - Validates format only
    - Accepts any 6-digit OTP
    - Stores only verification flag and hash
    """
    # SIMULATION: Accept any valid format OTP
    # In production, verify OTP with UIDAI API
    
    if current_user.aadhaar_verified:
        return VerificationResponse(
            success=True,
            message="Aadhaar already verified",
            verified=True
        )
    
    # Hash the Aadhaar number (NEVER store plaintext)
    aadhaar_hash = hash_identifier(request.aadhaar_number)
    
    # Update user record
    current_user.aadhaar_verified = True
    current_user.aadhaar_hash = aadhaar_hash
    
    await db.commit()
    
    return VerificationResponse(
        success=True,
        message="Aadhaar verification successful (SIMULATED)",
        verified=True
    )


@router.post("/pan", response_model=VerificationResponse)
async def verify_pan(
    request: PANVerifyRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Simulate PAN verification.
    
    SIMULATED: In production, this would:
    1. Verify PAN with Income Tax Department API
    2. Match name with PAN records
    3. Receive verification response
    
    Current behavior:
    - Validates format only
    - Stores only verification flag and hash
    """
    if current_user.pan_verified:
        return VerificationResponse(
            success=True,
            message="PAN already verified",
            verified=True
        )
    
    # Hash the PAN number (NEVER store plaintext)
    pan_hash = hash_identifier(request.pan_number)
    
    # Update user record
    current_user.pan_verified = True
    current_user.pan_hash = pan_hash
    
    await db.commit()
    
    return VerificationResponse(
        success=True,
        message="PAN verification successful (SIMULATED)",
        verified=True
    )
