"""
Virtual ID model - stores temporary, one-time-use virtual identifiers.
"""

from sqlalchemy import Column, String, Boolean, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class VirtualID(Base):
    """
    Virtual ID model for temporary identity tokens.
    
    Each VID is:
    - Time-limited (expires_at)
    - Usage-limited (usage_limit, usage_count)
    - Revocable (revoked flag)
    - Auditable (linked to user)
    """
    __tablename__ = "virtual_ids"
    
    vid = Column(String(12), primary_key=True)  # 12-digit unique identifier
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    
    # Usage tracking
    usage_limit = Column(Integer, default=1, nullable=False)  # Default: one-time use
    usage_count = Column(Integer, default=0, nullable=False)
    
    # Status flags
    revoked = Column(Boolean, default=False, nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="virtual_ids")
    
    @property
    def is_valid(self) -> bool:
        """Check if VID is currently valid."""
        if self.revoked:
            return False
        if datetime.utcnow() > self.expires_at:
            return False
        if self.usage_count >= self.usage_limit:
            return False
        return True
    
    @property
    def is_used(self) -> bool:
        """Check if VID has been used up."""
        return self.usage_count >= self.usage_limit
    
    def __repr__(self):
        return f"<VirtualID(vid={self.vid}, user_id={self.user_id}, valid={self.is_valid})>"
