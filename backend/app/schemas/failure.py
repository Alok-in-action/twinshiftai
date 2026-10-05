from datetime import datetime

from pydantic import BaseModel, Field


class FailureAndWorkoverRecord(BaseModel):
    well_id: str = Field(..., description="Unique well identifier")
    event_id: str = Field(..., description="Unique event identifier")
    timestamp: datetime = Field(..., description="Event timestamp")
    failure_type: str = Field(..., description="Type of failure or workover")
    component: str | None = Field(None, description="Failed equipment component")
    description: str | None = Field(None, description="Details of the event")
