from fastapi import HTTPException
from schemas.user_schema import UserCreate, UserLogin, UserBase
from actions.dal.userDAO import UserDAO
from models.user import User

class UserServices():
    def __init__(self, dao: UserDAO):
        """ Initialize UserServices with an instance of UserDAO
            UserDAO is responsible for data access layer got db interactions

        Args:
            dao (UserDAO): Data access layer for User
        """
        
        self.dao = dao

    
    async def add_user(self, user: UserCreate) -> User:
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


    async def login_user(self, user: UserLogin) -> User:
        """ Handles user login by validating user credentials.
            Checks if the user exists and then if the password is correct.
        
        Args:
            user (UserLogin): Login data.

        Raises:
            HTTPException: User does not exists based on login data.
            HTTPException: Password is not correct.
            HTTPException: Error logging user at current moment. 

        Returns:
            User: The newly logged in user. 
        """

        # validate login data
        await self.validate_user_login_data(user)
        
        # get the current user 
        current_user = self.dao.get_user(user)

        # if we can't find a user then raise an error
        if current_user is None:
            raise HTTPException(status_code=404, detail="User does not exist")  
        
        # check if the provided password is correct
        if not current_user.check_password(user.password):
            raise HTTPException(status_code=404, detail="The password you entered is incorrect. Please try again.") 
       
        # log the user in (set logged_in status to True) 
        user = self.dao.login_user(current_user)

        # if something goes wrong with logging in, raise an error
        if not user:
            raise HTTPException(status_code=404, detail="Can not login at the current moment") 

        return user


    async def logout_user(self, username: str, email: str) -> User:
        """ Logs out the user by updating logged in status in database.

        Args:
            username (str): _description_
            email (str): _description_

        Returns:
            User: The logged-out user object. 
        """
        return self.dao.logout_user(username, email)
        
    
    async def get_current_user(self, username: str, email: str) -> User:
        """ Retrieves the current logged in user from the database.

        Args:
            username (str): Username of current user. 
            email (str): Email of current user.

        Returns:
            User: The user object. 
        """
        return self.dao.get_user_by_username_and_email(username, email)
        
        
    async def check_user_exists(self, user: UserCreate) -> User:
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