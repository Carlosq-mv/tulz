from pydantic import BaseModel, ConfigDict
from models.contact import Status


# base schema for contact
class ContactBase(BaseModel):
    username: str
   
   
# used to create a contact 
class ContactCreate(ContactBase):
    user_id: int
   
   
# used to return contact  
class ContactResponse(ContactBase):
    id: int
    user_id: int
    status: Status | None = None
    model_config = ConfigDict(from_attributes=True)


# used for search criteria
class ContactSearch(BaseModel):
    id: int | None = None
    user_id: int | None = None
    username: str | None = None