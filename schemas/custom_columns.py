import datetime
from typing import Annotated
from sqlalchemy import text  # noqa
from sqlalchemy.orm import mapped_column


intpk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[
    datetime.datetime,
    mapped_column(default=datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None))
]
# created_at = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]
