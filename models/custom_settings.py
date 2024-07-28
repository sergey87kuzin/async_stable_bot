from typing import Any

from models import ShowUser
from models.common import TunedModel


class ShowCustomSettings(TunedModel):
    id: int
    name: str
    model_id: str
    users: list[ShowUser]
