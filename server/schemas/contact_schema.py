from datetime import datetime
from pydantic import BaseModel, ConfigDict
from models.contact import Status


# base schema for contact
class ContactBase(BaseModel):
    username: str
   
   
# used to create a contact 
class ContactForm(BaseModel):
    current_user_id: int
    friend_id: int
   
   
# used to return contact  
class ContactResponse(BaseModel):
    id: int
    current_user_id: int  # ID of the user who initiated the contact
    friend_id: int   # ID of the user being contacted
    status: Status | None = None  # Contact status (e.g., PENDING, ACCEPTED)
    date_added: datetime | None = None  # Optional, for accepted contacts
    last_updated: datetime  # Timestamp for when the contact was last updated
    model_config = ConfigDict(from_attributes=True)


# used for search criteria
class ContactSearch(BaseModel):
    id: int | None = None
    user_id: int | None = None
    username: str | None = None