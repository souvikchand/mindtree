import time
from uuid import UUID, uuid4
from pydantic import BaseModel, Field
from typing import Literal


class Node(BaseModel):
    node_id: UUID = Field(default_factory=uuid4)
    graph_id: UUID

    label: str
    payload_type: Literal["str", "int", "image"]
    payload: dict

    metadata: dict = Field(default_factory=dict)
    created_at: float = Field(default_factory= lambda: time.time())
    updated_at: float = Field(default_factory=lambda: __import__('time').time())

