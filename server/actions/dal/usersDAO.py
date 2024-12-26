from sqlalchemy.orm import Session
from sqlalchemy import or_

from schemas.user_schema import UserCreate, UserLogin
from models.user import User



class UserDAO():
    # initialize UserDAO with database
    def __init__(self, db: Session):
        self.db = db


    # create and add new user to database
    def create_user(self, user: UserCreate) -> User:
        new_user = User(name=user.name, email=user.email, username=user.username)
        new_user.set_password(user.password)
        self.db.add(new_user)
        self.db.commit()

        # return the user or None
        return new_user 

  
    # get all the users in the database
    def get_all_users(self) -> list[User]:
        return self.db.query(User).all()


    # get the user with UserCreate schema
    def get_user_by_data(self, user: UserCreate) -> User:
        u = self.db.query(User).filter(
            or_ (
                User.email == user.email,
                User.username == user.username
            )
        ).first()

        return u       


    # get the user with username and email
    def get_user_by_username_and_email(self, username: str, email: str) -> User:
        user = self.db.query(User).filter(User.username == username, User.email == email).first()
        return user


    # get the user with only the username
    def get_user_by_username(self, username: str) -> User:
        user = self.db.query(User).filter(User.username == username).first()
        return user


    # get user by id
    def get_user_by_id(self, id: int) -> User:
        user = self.db.query(User).filter(User.id == id).first()
        return user


   # get a user with login data
    def get_user(self, user: UserLogin) -> User:
        current_user = self.db.query(User).filter(User.username == user.username, User.email == user.email).first()
        return current_user
 
   