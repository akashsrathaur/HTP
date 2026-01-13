"""
Virtual ID management routes.

Handles VID generation, listing, and revocation.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timedelta

from database import get_db
from models.user import User
from models.virtual_id import VirtualID
from models.audit_log import AuditLog, AuditAction
from schemas.virtual_id import VIDGenerateResponse, VIDListResponse, VIDItem
from security.crypto import generate_vid, generate_qr_payload, hash_identifier
from routes.auth import get_current_user
from config import settings


router = APIRouter(prefix="/vid", tags=["Virtual ID Management"])


@router.post("/generate", response_model=VIDGenerateResponse, status_code=status.HTTP_201_CREATED)
async def generate_virtual_id(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Generate a new Virtual ID.
    
    Requirements:
    - User must be authenticated
    - User must have verified Aadhaar
    - User must have verified PAN
    
    Returns:
    - 12-digit VID
    - Signed QR code payload
    - Expiry timestamp
    """
    # Check verification status
    if not current_user.aadhaar_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Aadhaar verification required before generating VID"
        )
    
    if not current_user.pan_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="PAN verification required before generating VID"
        )
    
    # Generate unique VID
    vid = generate_vid()
    
    # Ensure VID is unique (very unlikely collision, but check anyway)
    result = await db.execute(
        select(VirtualID).where(VirtualID.vid == vid)
    )
    existing_vid = result.scalar_one_or_none()
    
    if existing_vid:
        # Regenerate if collision (extremely rare)
        vid = generate_vid()
    
    # Calculate expiry
    expires_at = datetime.utcnow() + timedelta(minutes=settings.vid_expiry_minutes)
    
    # Create VID record
    new_vid = VirtualID(
        vid=vid,
        user_id=current_user.id,
        expires_at=expires_at,
        usage_limit=settings.vid_usage_limit
    )
    
    db.add(new_vid)
    
    # Create audit log
    audit_log = AuditLog(
        vid_hash=hash_identifier(vid),
        action=AuditAction.CREATED,
        result="VID created successfully"
    )
    db.add(audit_log)
    
    await db.commit()
    
    # Generate signed QR payload
    qr_payload = generate_qr_payload(vid, expires_at)
    
    return VIDGenerateResponse(
        vid=vid,
        qr_payload=qr_payload,
        expires_at=expires_at,
        usage_limit=settings.vid_usage_limit
    )


@router.get("/list", response_model=VIDListResponse)
async def list_virtual_ids(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    List all VIDs for the current user.
    
    Returns both active and expired/used VIDs for user's reference.
    """
    result = await db.execute(
        select(VirtualID)
        .where(VirtualID.user_id == current_user.id)
        .order_by(VirtualID.created_at.desc())
    )
    vids = result.scalars().all()
    
    vid_items = [VIDItem.model_validate(vid) for vid in vids]
    
    return VIDListResponse(
        vids=vid_items,
        total=len(vid_items)
    )


@router.post("/revoke/{vid}")
async def revoke_virtual_id(
    vid: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Revoke a Virtual ID.
    
    Makes the VID immediately invalid, even if not yet used or expired.
    """
    # Find VID
    result = await db.execute(
        select(VirtualID).where(
            VirtualID.vid == vid,
            VirtualID.user_id == current_user.id
        )
    )
    vid_record = result.scalar_one_or_none()
    
    if not vid_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="VID not found or does not belong to you"
        )
    
    if vid_record.revoked:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="VID already revoked"
        )
    
    # Revoke VID
    vid_record.revoked = True
    
    # Create audit log
    audit_log = AuditLog(
        vid_hash=hash_identifier(vid),
        action=AuditAction.REVOKED,
        result="VID revoked by user"
    )
    db.add(audit_log)
    
    await db.commit()
    
    return {
        "success": True,
        "message": "VID revoked successfully"
    }
