from typing import Generic, TypeVar, Optional, Any
from pydantic import BaseModel, Field

T = TypeVar("T")

class APIResponse(BaseModel, Generic[T]):
    """
    Standardized API response envelope for all endpoint outputs.
    Ensures consistent communication formatting between backend and frontend.
    """
    status: str = Field(..., description="The status of the request: success, fail, or error")
    message: str = Field(..., description="An informative message regarding the request outcome")
    data: Optional[T] = Field(default=None, description="The payload payload carrying the requested resource data")
    meta: Optional[dict[str, Any]] = Field(default=None, description="Optional metadata carrying extra pagination or telemetry details")

    class Config:
        json_schema_extra = {
            "example": {
                "status": "success",
                "message": "Successfully retrieved resource details",
                "data": None,
                "meta": None
            }
        }
