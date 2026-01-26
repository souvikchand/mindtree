from datetime import datetime, timezone
from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class Graph(BaseModel):
    graph_id: UUID = Field(default_factory=uuid4)
    name: str
    is_auto_named: bool = False

    created_at: datetime = Field(default_factory= lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory= lambda: datetime.now(timezone.utc))

    metadata: dict = Field(default_factory=dict)


class GraphSnapshot(BaseModel):
    graph: Graph
    snapshot_id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory= lambda: datetime.now(timezone.utc))
    description: str = ""