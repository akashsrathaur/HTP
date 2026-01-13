"""Routes package."""

from routes.auth import router as auth_router
from routes.verification import router as verification_router
from routes.virtual_id import router as virtual_id_router
from routes.verify_vid import router as verify_vid_router

__all__ = ["auth_router", "verification_router", "virtual_id_router", "verify_vid_router"]
