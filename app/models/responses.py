from pydantic import BaseModel, model_validator
from datetime import datetime, timezone
from typing import Optional, Dict, List
import ujson as json


class BaseWithTimestamp(BaseModel):
    timestamp: Optional[datetime]

    @model_validator(mode="before")
    def validate_model(cls, data):
        # This will run regardless of which fields are present
        if "timestamp" not in data or data["timestamp"] is None:
            data["timestamp"] = datetime.now(timezone.utc)
        elif isinstance(data["timestamp"], str):
            data["timestamp"] = datetime.fromisoformat(data["timestamp"])
        return data

    def to_dict(self, remove_none=True):
        response = self.model_dump()
        if remove_none:
            response = {k: v.isoformat() if isinstance(v, datetime) else v for k, v in response.items() if v is not None}
        return response

    def __str__(self):
        return json.dumps(self.to_dict(), indent=2)

    def __repr__(self):
        return self.__str__()

class VersionResponse(BaseWithTimestamp):
    name: str
    version: str

class StatusResponse(VersionResponse):
    services: List[str]

