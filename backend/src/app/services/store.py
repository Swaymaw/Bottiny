# services/store.py
from src.app.core.flow import Flow
from src.app.core.models import FlowSpec
from src.app.db.tables import FlowRow
from src.app.services.builder import build_flow
from src.app.utils.helper import get_db_engine


async def save_flow(spec: FlowSpec) -> FlowRow:
    build_flow(spec)  # validate before saving
    data = spec.model_dump(by_alias=True)
    db = get_db_engine()

    if await db.get(FlowRow, FlowRow.name == spec.name):
        await db.update(FlowRow, FlowRow.name == spec.name, spec=data)
        return await db.get(FlowRow, FlowRow.name == spec.name)
    return await db.add(FlowRow(name=spec.name, spec=data))


async def set_enabled(name: str, enabled: bool) -> bool:
    db = get_db_engine()
    return await db.update(FlowRow, FlowRow.name == name, enabled=enabled) > 0


async def get_flow_row(name: str) -> FlowRow | None:
    db = get_db_engine()
    return await db.get(FlowRow, FlowRow.name == name)


async def list_flows(only_enabled: bool = False) -> list[FlowRow]:
    db = get_db_engine()
    where = [FlowRow.enabled] if only_enabled else []
    return await db.get_all(FlowRow, *where)


async def load_flow(name: str) -> Flow | None:
    db = get_db_engine()
    row = await db.get(FlowRow, FlowRow.name == name, FlowRow.enabled)
    return build_flow(FlowSpec(**row.spec)) if row else None
