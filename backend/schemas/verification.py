"""
Pydantic schemas for identity verification operations.
"""

from pydantic import BaseModel, Field, field_validator
import re


class AadhaarVerifyRequest(BaseModel):
    """
    Schema for Aadhaar verification request.
    
    IMPORTANT: This is for SIMULATED verification only.
    In production, this would integrate with official UIDAI APIs.
    """
    aadhaar_number: str = Field(..., description="12-digit Aadhaar number")
    otp: str = Field(..., description="6-digit OTP (simulated)")
    
    @field_validator("aadhaar_number")
    @classmethod
    def validate_aadhaar(cls, v: str) -> str:
        """Validate Aadhaar number format (12 digits)."""
        if not re.match(r"^\d{12}$", v):
            raise ValueError("Aadhaar number must be exactly 12 digits")
        return v
    
    @field_validator("otp")
    @classmethod
    def validate_otp(cls, v: str) -> str:
        """Validate OTP format (6 digits)."""
        if not re.match(r"^\d{6}$", v):
            raise ValueError("OTP must be exactly 6 digits")
        return v


class PANVerifyRequest(BaseModel):
    """
    Schema for PAN verification request.
    
    IMPORTANT: This is for SIMULATED verification only.
    In production, this would integrate with official Income Tax APIs.
    """
    pan_number: str = Field(..., description="10-character PAN number")
    
    @field_validator("pan_number")
    @classmethod
    def validate_pan(cls, v: str) -> str:
        """
        Validate PAN number format.
        Format: ABCDE1234F (5 letters, 4 digits, 1 letter)
        """
        v = v.upper()
        if not re.match(r"^[A-Z]{5}\d{4}[A-Z]$", v):
            raise ValueError("Invalid PAN format. Expected: ABCDE1234F")
        return v


class VerificationResponse(BaseModel):
    """Schema for verification response."""
    success: bool = Field(..., description="Whether verification succeeded")
    message: str = Field(..., description="Verification result message")
    verified: bool = Field(..., description="Verification status")
