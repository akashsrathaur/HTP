"""
Audit log model - tracks all VID operations for security and compliance.
Stores hashed identifiers only, no PII.
"""

from sqlalchemy import Column, Integer, String, DateTime, Enum
from datetime import datetime
import enum
from database import Base


class AuditAction(str, enum.Enum):
    """Enum for audit log actions."""
    CREATED = "created"
    VERIFIED = "verified"
    EXPIRED = "expired"
    REVOKED = "revoked"
    FAILED_VERIFICATION = "failed_verification"


class AuditLog(Base):
    """
    Audit log for VID operations.
    
    Privacy-preserving: Stores hashed VID and IP, no direct identifiers.
    """
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Hashed identifiers (privacy-preserving)
    vid_hash = Column(String(64), nullable=False, index=True)  # SHA-256 of VID
    ip_hash = Column(String(64), nullable=True)  # SHA-256 of IP address
    
    # Action details
    action = Column(Enum(AuditAction), nullable=False)
    result = Column(String(255), nullable=False)  # Success message or failure reason
    
    # Timestamp
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    def __repr__(self):
        return f"<AuditLog(id={self.id}, action={self.action}, timestamp={self.timestamp})>"
