from pydantic import BaseModel, EmailStr, ConfigDict, Field

# base schame for user
class UserBase(BaseModel):
    name: str
    username: str
    email: EmailStr

# user to create new user
class UserCreate(UserBase):
    password: str

# used for user login
class UserLogin(BaseModel):
    username: str
    email: str
    password: str

        
# used to return user 
class UserResponse(UserBase):
    id: int
    is_logged_in: bool
    model_config = ConfigDict(from_attributes=True)