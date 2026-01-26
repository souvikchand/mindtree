from uuid import UUID, uuid4
from pydantic import BaseModel, Field
from typing import Literal


class Asset(BaseModel):
    """Represents a digital asset in the system."""
    asset_id: UUID = Field(default_factory=uuid4)
    asset_type: Literal["image"]
    uri: str

    metadata: dict = Field(default_factory=dict)
