"""
User model - stores user accounts with verification status.
NEVER stores actual Aadhaar or PAN numbers, only hashes and verification flags.
"""

from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from database import Base


class User(Base):
    """
    User account model.
    
    Privacy-by-design: Only stores verification flags and non-reversible hashes.
    """
    __tablename__ = "users"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    
    # Verification flags (boolean only, no actual numbers)
    aadhaar_verified = Column(Boolean, default=False, nullable=False)
    pan_verified = Column(Boolean, default=False, nullable=False)
    
    # Non-reversible hashes (SHA-256) for audit purposes only
    aadhaar_hash = Column(String(64), nullable=True)  # SHA-256 produces 64 hex chars
    pan_hash = Column(String(64), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    virtual_ids = relationship("VirtualID", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, aadhaar_verified={self.aadhaar_verified}, pan_verified={self.pan_verified})>"
