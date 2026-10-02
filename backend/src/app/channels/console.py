from src.app.core.models import Button


def render(out):
    print(f"assistant> {out.text}")
    for i, b in enumerate(out.buttons, 1):
        print(f"  [{i}] {b.label}")
    if out.buttons:
        print(f"  press <1-{len(out.buttons)}> + enter")


def resolve_button(raw: str, buttons: list[Button]) -> str | None:
    raw = raw.strip().lower()
    for i, b in enumerate(buttons, 1):
        if raw in (str(i), b.id.lower(), b.label.lower()):
            return b.id
    return None
