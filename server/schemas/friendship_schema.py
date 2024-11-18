from pydantic import BaseModel, ConfigDict
from datetime import datetime


class AddFriendship(BaseModel):
    user_id: int
    friend_id: int

    
class FriendshipResponse(AddFriendship):
    created_at: datetime = None
    
    model_config = ConfigDict(from_attributes=True)

