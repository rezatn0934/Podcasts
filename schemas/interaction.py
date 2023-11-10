from enum import Enum
from typing import Optional

from pydantic import BaseModel


class ActionTypeEnum(str, Enum):
    like = "like"
    comment = "comment"
    book_mark = 'book_mark'


class BaseInteractionSchema(BaseModel):
    channel_id: int
    podcast_id: int
    action_type: ActionTypeEnum


class InteractionSchema(BaseInteractionSchema):
    content: Optional[str] = ''
