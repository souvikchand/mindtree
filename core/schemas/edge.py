import time
from uuid import UUID, uuid4
from pydantic import BaseModel, Field
from typing import Optional


class Edge(BaseModel):
    edge_id: UUID = Field(default_factory=uuid4)
    graph_id: UUID

    source_node_id: UUID
    target_node_id: UUID

    label: Optional[str] = None
    metadata: dict = Field(default_factory=dict)

#