from datetime import timedelta
from typing import Tuple
from fastapi import HTTPException
from schemas.user_schema import UserCreate, UserLogin, UserBase, UserResponse
from actions.dal.usersDAO import UserDAO
from models.user import User
from actions.util.jwtHelper import ACCESS_TOKEN_EXPIRE_MIN, JwtHelper
from schemas.token_schema import TokenData

class UserServices():
    def __init__(self, dao: UserDAO):
        """ Initialize UserServices with an instance of UserDAO
            UserDAO is responsible for data access layer got db interactions

        Args:
            dao (UserDAO): Data access layer for User
        """
        
        self.dao = dao

    
    async def add_user(self, user: UserCreate) -> UserResponse:
        """ Add a new user to the system and provides data validation.
            It will first validate the user data and check if the user
            exists. If the user exists raise an HTTPException.
            
        Args:
            user (UserCreate): User data to create new user.

        Raises:
            HTTPException: If a user already has the same email or username.

        Returns:
            User: The created user object. 
        """

        # validate the data
        await self.validate_user_create_data(user)
        # check if the user already exists
        if await self.check_user_exists(user):
            raise HTTPException(status_code=400, detail="Email and(or) username already registered.")

        # create and return the new user
        return self.dao.create_user(user) 


    async def login_user(self, user: UserLogin) -> Tuple[str, str, User]:
        """ Handles user login by validating user credentials.
            Checks if the user exists and then if the password is correct.
            Then it will create the access & refresh tokem
        
        Args:
            user (User): User object.
            jwt_access_token: JWT access token (15 min).
            jwt_refresh_token: JWT refresh token (7 dayshg).

        Raises:
            HTTPException: User does not exists based on login data.
            HTTPException: Password is not correct.
            HTTPException: Error logging user at current moment. 

        Returns:
            Tuple[str, str, User]: Tuple with both tokens & the newly logged in user. 
        """

        # validate login data
        await self.validate_user_login_data(user)
        
        # get the current user 
        current_user = self.dao.get_user(user)

        # if we can't find a user then raise an error
        if current_user is None:
            raise HTTPException(status_code=404, detail="User does not exist. Please try again.")  
        
        # check if the provided password is correct
        if not current_user.check_password(user.password):
            raise HTTPException(status_code=404, detail="The password you entered is incorrect. Please try again.") 
       
        expires_time = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MIN)

        # create both tokens
        jwt_access_token = await JwtHelper.create_access_token({"user_id":current_user.id}, expires_delta=expires_time)
        jwt_refresh_token = await JwtHelper.create_refresh_token({"user_id":current_user.id})

        # return the token and user object
        return jwt_access_token, jwt_refresh_token, current_user


    async def handle_refresh_token(self, refresh_token: str) -> Tuple[str, str, int]:
        """ Handles refreshing token once the access token expires.
            Validates the refresh token and then will create a new
            access & refresh token.

        Args:
            refresh_token (str): Current refresh token that is in cookie. 

        Raises:
            HTTPException: There is no refresh token.
            HTTPException: Token payload does not have 'user_id'. 

        Returns:
            Tuple[str, str]: Tuples with the new tokens and user id,
        """
        if not refresh_token or refresh_token is None:
            raise HTTPException(status_code=401, detail="Refresh token missing")
          
        # Verify and decode the refresh token
        payload = await JwtHelper.verify_refresh_token(refresh_token)  

        user_id = payload.get("user_id")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        # Generate a new access token
        expires_time = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MIN)

        # create both tokens
        new_access_token = await JwtHelper.create_access_token({"user_id":user_id}, expires_delta=expires_time)
        new_refresh_token = await JwtHelper.create_refresh_token({"user_id":user_id})

        return new_access_token, new_refresh_token, user_id


    async def get_all_users(self) -> list[UserResponse]:
        """ Retrieves all users in database.

        Returns:
            list[User]: List of users in databae. 
        """
        return self.dao.get_all_users()
        
    
    async def get_current_user(self, username: str, email: str) -> UserResponse:
        """ Retrieves the current logged in user from the database.

        Args:
            username (str): Username of current user. 
            email (str): Email of current user.

        Returns:
            User: The user object. 
        """
        return self.dao.get_user_by_username_and_email(username, email)
        
        
    async def check_user_exists(self, user: UserCreate) -> UserResponse:
        """ Helper function that checks if a user already exists in database.

        Args:
            user (UserCreate): User data.  

        Returns:
            User: The user object 
        """
        u = self.dao.get_user_by_data(user)
        return u


    async def validate_user_create_data(self, user: UserCreate):
        """ Validates the user creation data to ensure all required fields are present.

        Args:
            user (UserCreate): The user data. 

        Raises:
            HTTPException: Any missing field for required data. 
        """
        if not user.username or not user.email or not user.password or not user.name:
            raise HTTPException(status_code=400, detail="All fields are required. Please try again.")


    async def validate_user_login_data(self, user: UserLogin):
        """ Validates the login data to ensure all required fields are provided.

        Args:
            user (UserLogin): The user data. 

        Raises:
            HTTPException: Any missing field for required data. 
        """
        if not user.username or not user.email or not user.password:
            raise HTTPException(status_code=400, detail="All fields are required. Please try again.")

    
    async def valid_email(self ,email: str):
        """ Validate the email format.

        Args:
            email (str): User entered email.

        Raises:
            HTTPException: Email is invalid format. 
        """
        if "@" not in email:
            raise HTTPException(status_code=400, detail="Invalid email format. Please try again.")