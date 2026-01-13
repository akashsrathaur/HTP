"""
Public VID verification route.

This endpoint is PUBLIC (no authentication required) and allows
anyone to verify a VID or QR code to check identity verification status.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime

from database import get_db
from models.virtual_id import VirtualID
from models.user import User
from models.audit_log import AuditLog, AuditAction
from schemas.virtual_id import VIDVerifyRequest, VIDVerifyResponse
from security.crypto import verify_qr_payload, hash_identifier


router = APIRouter(tags=["VID Verification"])


def mask_name(name: str) -> str:
    """
    Mask a name for privacy.
    
    Example: "John Doe" -> "John D***"
    """
    parts = name.split()
    if len(parts) == 0:
        return "***"
    
    if len(parts) == 1:
        # Single name: show first 3 chars
        if len(parts[0]) <= 3:
            return parts[0]
        return parts[0][:3] + "***"
    
    # Multiple parts: show first name, mask last name
    first_name = parts[0]
    last_initial = parts[-1][0] if parts[-1] else ""
    return f"{first_name} {last_initial}***"


def calculate_age_group(birth_year: int = None) -> str:
    """
    Calculate age group.
    
    Since we don't store birth dates in this simulation,
    we return a generic "18+" for verified users.
    
    In production, this would calculate from actual DOB.
    """
    # Simulation: return generic age group
    return "18+"


@router.post("/verify-vid", response_model=VIDVerifyResponse)
async def verify_vid(
    request: VIDVerifyRequest,
    req: Request,
    db: AsyncSession = Depends(get_db)
):
    """
    Verify a Virtual ID or QR code.
    
    PUBLIC ENDPOINT - No authentication required.
    
    This endpoint:
    1. Verifies QR signature (if QR code provided)
    2. Checks VID validity (expiry, usage, revocation)
    3. Returns minimal user information if valid
    4. Increments usage counter
    5. Creates audit log
    
    Rate limited to prevent abuse.
    """
    # Extract VID
    vid = request.get_vid()
    
    if not vid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Either 'vid' or 'qr_payload' must be provided"
        )
    
    # If QR payload provided, verify signature
    if request.qr_payload:
        is_valid, error_msg = verify_qr_payload(request.qr_payload)
        if not is_valid:
            # Log failed verification
            audit_log = AuditLog(
                vid_hash=hash_identifier(vid),
                ip_hash=hash_identifier(req.client.host),
                action=AuditAction.FAILED_VERIFICATION,
                result=f"Invalid QR signature: {error_msg}"
            )
            db.add(audit_log)
            await db.commit()
            
            return VIDVerifyResponse(
                valid=False,
                message=f"Invalid QR code: {error_msg}"
            )
    
    # Find VID in database
    result = await db.execute(
        select(VirtualID).where(VirtualID.vid == vid)
    )
    vid_record = result.scalar_one_or_none()
    
    if not vid_record:
        # Log failed verification
        audit_log = AuditLog(
            vid_hash=hash_identifier(vid),
            ip_hash=hash_identifier(req.client.host),
            action=AuditAction.FAILED_VERIFICATION,
            result="VID not found"
        )
        db.add(audit_log)
        await db.commit()
        
        return VIDVerifyResponse(
            valid=False,
            message="VID not found"
        )
    
    # Check if revoked
    if vid_record.revoked:
        audit_log = AuditLog(
            vid_hash=hash_identifier(vid),
            ip_hash=hash_identifier(req.client.host),
            action=AuditAction.FAILED_VERIFICATION,
            result="VID revoked"
        )
        db.add(audit_log)
        await db.commit()
        
        return VIDVerifyResponse(
            valid=False,
            message="VID has been revoked"
        )
    
    # Check if expired
    if datetime.utcnow() > vid_record.expires_at:
        audit_log = AuditLog(
            vid_hash=hash_identifier(vid),
            ip_hash=hash_identifier(req.client.host),
            action=AuditAction.EXPIRED,
            result="VID expired"
        )
        db.add(audit_log)
        await db.commit()
        
        return VIDVerifyResponse(
            valid=False,
            message="VID has expired"
        )
    
    # Check usage limit
    if vid_record.usage_count >= vid_record.usage_limit:
        audit_log = AuditLog(
            vid_hash=hash_identifier(vid),
            ip_hash=hash_identifier(req.client.host),
            action=AuditAction.FAILED_VERIFICATION,
            result="VID usage limit reached"
        )
        db.add(audit_log)
        await db.commit()
        
        return VIDVerifyResponse(
            valid=False,
            message="VID has already been used"
        )
    
    # VID is valid - get user information
    result = await db.execute(
        select(User).where(User.id == vid_record.user_id)
    )
    user = result.scalar_one_or_none()
    
    if not user:
        # Should never happen, but handle gracefully
        return VIDVerifyResponse(
            valid=False,
            message="User not found"
        )
    
    # Increment usage counter
    vid_record.usage_count += 1
    
    # Create audit log
    audit_log = AuditLog(
        vid_hash=hash_identifier(vid),
        ip_hash=hash_identifier(req.client.host),
        action=AuditAction.VERIFIED,
        result="VID verified successfully"
    )
    db.add(audit_log)
    
    await db.commit()
    
    # Return minimal user information
    return VIDVerifyResponse(
        valid=True,
        message="VID verified successfully",
        name=mask_name(user.name),
        age_group=calculate_age_group(),
        aadhaar_verified=user.aadhaar_verified,
        pan_verified=user.pan_verified
    )
