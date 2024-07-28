from .common import TunedModel

__all__ = (
    "ShowStyle",
)


class ShowStyle(TunedModel):
    id: int
    name: str
    name_for_menu: str
