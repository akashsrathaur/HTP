"""
Pydantic schemas for Virtual ID operations.
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Dict


class VIDGenerateResponse(BaseModel):
    """Schema for VID generation response."""
    vid: str = Field(..., description="12-digit Virtual ID")
    qr_payload: Dict[str, str] = Field(..., description="Signed QR code payload")
    expires_at: datetime = Field(..., description="Expiry timestamp")
    usage_limit: int = Field(..., description="Maximum number of uses")


class VIDVerifyRequest(BaseModel):
    """Schema for VID verification request."""
    vid: Optional[str] = Field(None, description="12-digit VID (if manual entry)")
    qr_payload: Optional[Dict[str, str]] = Field(None, description="QR code payload (if scanned)")
    
    def get_vid(self) -> Optional[str]:
        """Extract VID from either direct input or QR payload."""
        if self.vid:
            return self.vid
        if self.qr_payload and "vid" in self.qr_payload:
            return self.qr_payload["vid"]
        return None


class VIDVerifyResponse(BaseModel):
    """
    Schema for VID verification response.
    
    Returns minimal information to protect privacy.
    """
    valid: bool = Field(..., description="Whether VID is valid")
    message: str = Field(..., description="Verification result message")
    
    # Only included if valid=True
    name: Optional[str] = Field(None, description="Masked name (e.g., 'John D***')")
    age_group: Optional[str] = Field(None, description="Age group (e.g., '18-25')")
    aadhaar_verified: Optional[bool] = Field(None, description="Aadhaar verification status")
    pan_verified: Optional[bool] = Field(None, description="PAN verification status")


class VIDItem(BaseModel):
    """Schema for a single VID in list response."""
    vid: str = Field(..., description="Virtual ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    expires_at: datetime = Field(..., description="Expiry timestamp")
    usage_count: int = Field(..., description="Number of times used")
    usage_limit: int = Field(..., description="Maximum uses allowed")
    revoked: bool = Field(..., description="Whether VID is revoked")
    is_valid: bool = Field(..., description="Whether VID is currently valid")
    
    class Config:
        from_attributes = True


class VIDListResponse(BaseModel):
    """Schema for listing user's VIDs."""
    vids: list[VIDItem] = Field(..., description="List of user's VIDs")
    total: int = Field(..., description="Total number of VIDs")
