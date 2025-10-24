from datetime import date
from pydantic import BaseModel


class RetrospectiveCreateRequest(BaseModel):
    start_date: date
    end_date: date


class RetrospectiveResponse(BaseModel):
    content: str
