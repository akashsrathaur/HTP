"""
JWT token handling for user authentication.
"""

from datetime import datetime, timedelta
from jose import JWTError, jwt
from config import settings
from typing import Optional


def create_access_token(user_id: str) -> str:
    """
    Create a JWT access token for a user.
    
    Args:
        user_id: User's UUID
        
    Returns:
        Encoded JWT token
    """
    expire = datetime.utcnow() + timedelta(hours=settings.jwt_expiry_hours)
    
    payload = {
        "sub": user_id,  # Subject: user ID
        "exp": expire,   # Expiration time
        "iat": datetime.utcnow()  # Issued at
    }
    
    token = jwt.encode(
        payload,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm
    )
    
    return token


def verify_token(token: str) -> Optional[str]:
    """
    Verify and decode a JWT token.
    
    Args:
        token: JWT token string
        
    Returns:
        User ID if valid, None if invalid or expired
    """
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm]
        )
        
        user_id: str = payload.get("sub")
        if user_id is None:
            return None
            
        return user_id
        
    except JWTError:
        return None
