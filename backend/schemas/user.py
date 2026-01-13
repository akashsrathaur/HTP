"""
Pydantic schemas for user-related operations.
"""

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    """Schema for user registration."""
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., min_length=8, description="Password (min 8 characters)")
    name: str = Field(..., min_length=1, max_length=255, description="User's full name")


class UserLogin(BaseModel):
    """Schema for user login."""
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., description="User's password")


class UserResponse(BaseModel):
    """Schema for user response (without sensitive data)."""
    id: str = Field(..., description="User's UUID")
    email: str = Field(..., description="User's email")
    name: str = Field(..., description="User's name")
    aadhaar_verified: bool = Field(..., description="Whether Aadhaar is verified")
    pan_verified: bool = Field(..., description="Whether PAN is verified")
    
    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    """Schema for authentication token response."""
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")
    user: UserResponse = Field(..., description="User information")
