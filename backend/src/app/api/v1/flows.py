from fastapi import APIRouter, HTTPException

from src.app.api.v1.schemas import EnabledState, FlowDetail, FlowSummary
from src.app.core.models import FlowSpec
from src.app.services import store

router = APIRouter(prefix="/flows", tags=["flows"])


@router.post("", response_model=FlowSummary, status_code=201)
async def create_flow(spec: FlowSpec):
    try:
        row = await store.save_flow(spec)
    except ValueError as e:
        raise HTTPException(422, str(e))
    return FlowSummary(name=row.name, enabled=row.enabled)


@router.get("", response_model=list[FlowSummary])
async def list_flows():
    rows = await store.list_flows()
    return [FlowSummary(name=r.name, enabled=r.enabled) for r in rows]


@router.get("/{name}", response_model=FlowDetail)
async def get_flow(name: str):
    row = await store.get_flow_row(name)
    if row is None:
        raise HTTPException(404, "flow not found")
    return FlowDetail(name=row.name, enabled=row.enabled, spec=row.spec)


@router.post("/{name}/enable", response_model=EnabledState)
async def enable_flow(name: str):
    if not await store.set_enabled(name, True):
        raise HTTPException(404, "flow not found")
    return EnabledState(enabled=True)


@router.post("/{name}/disable", response_model=EnabledState)
async def disable_flow(name: str):
    if not await store.set_enabled(name, False):
        raise HTTPException(404, "flow not found")
    return EnabledState(enabled=False)
