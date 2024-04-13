from pydantic import BaseModel
from typing import Union


class CreateChannel(BaseModel):
    channel_name: Union[str, None] = None
