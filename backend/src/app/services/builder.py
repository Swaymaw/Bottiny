from src.app.nodes import basic, buttons, llm  # noqa
from src.app.core.flow import Flow
from src.app.core.models import FlowSpec

from src.app.core.node import NODE_TYPES


def build_flow(spec: FlowSpec) -> Flow:
    ids = {n.id for n in spec.nodes}

    if len(ids) != len(spec.nodes):
        raise ValueError("duplicate node ids")
    if spec.start not in ids:
        raise ValueError(f"start node '{spec.start}' does not exist")

    flow = Flow(start=spec.start)
    for n in spec.nodes:
        if n.type not in NODE_TYPES:
            raise ValueError(f"unknown node type '{n.type}'")
        flow.add(NODE_TYPES[n.type](n.id, **n.config))

    for e in spec.edges:
        if e.from_ not in ids or e.to not in ids:
            raise ValueError(f"edge {e.from_} -> {e.to} refers to a missing node")
        flow.connect(e.from_, e.port, e.to)

    return flow
