from fastapi import Depends
from sqlalchemy.orm import Session

from database import SessionLocal
from actions.dal.usersDAO import UserDAO 
from actions.dal.contactDAO import ContactDAO
from actions.services.userServices import UserServices
from actions.services.contactService import ContactService


def get_db():
    """ Creates and yields a new database session for each request.
    
        This function uses FastAPI's dependency injection system to provide
        a database session to route handlers. The session is automatically
        closed once the request is finished.
        
        The `SessionLocal()` object represents a session factory bound to
        the database, and `yield` is used to return the session to the route
        while ensuring it gets closed after the request is completed.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
def get_user_services(db: Session = Depends(get_db)) -> UserServices:
    """ Provides an instance of UserServices for handling user-related operations.
    
        This function is used by FastAPI's dependency injection system to inject
        an instance of the `UserServices` class into the route handlers that
        require it. The `UserDAO` (data access object) is created with the provided
        database session (`db`), and `UserServices` is initialized with `UserDAO`.

    Args:
        db (Session, optional): The database session injected by FastAPI's Depends. 
                                Defaults to Depends(get_db).

    Returns:
        UserServices: An instance of the UserServices class, which handles
        user-related logic, such as user registration, login, and logout.
    """
    dao = UserDAO(db)
    return UserServices(dao)


def get_contact_services(db: Session = Depends(get_db)) -> ContactService:
    """ Provides an instance of ContactService for handling contact-related operations
    
        This function is used by FastAPI's dependency injection system to inject
        an instance of the `ContactService` class into the route handlers that
        require it. The `ContactDAO` (data access object) is created with the provided
        database session (`db`), and `ContactService` is initialized with `ContactDAO`.   

    Args:
        db (Session, optional): The database session injected by FastAPI's Depends. 
                                Defaults to Depends(get_db).

    Returns:
        ContactService: An instance of the ContactService class, which handles
        contact-related logic, such blocking, unblocking, rejecting, accepting contact
        requests, etc. 
    """
    contact_dao = ContactDAO(db)
    user_dao = UserDAO(db)
    return ContactService(contact_dao, user_dao)