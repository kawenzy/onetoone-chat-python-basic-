from pydantic import BaseModel,Field
from typing import Optional

class Chat(BaseModel):
    msg: str