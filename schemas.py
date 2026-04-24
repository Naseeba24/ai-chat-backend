from pydantic import BaseModel


class MessageRequest(BaseModel):
    event_id: str
    user_id: str
    message: str