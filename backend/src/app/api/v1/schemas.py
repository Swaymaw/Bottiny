from pydantic import BaseModel

from src.app.core.models import FlowSpec


class FlowSummary(BaseModel):
    name: str
    enabled: bool


class FlowDetail(FlowSummary):
    spec: FlowSpec


class EnabledState(BaseModel):
    enabled: bool
