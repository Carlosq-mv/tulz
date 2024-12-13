from datetime import datetime
from sqlalchemy import exists, not_
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from schemas.user_schema import UserBase, UserResponse
from schemas.contact_schema import * 
from models.contact import Contact 
from models.user import User

from models.enum.status import Status

class ContactDAO():
    # initialize ContactDAO with database
    def __init__(self, db: Session):
        self.db = db
        # Exclude these statuses when querying to add a new contact.
        # This ensures that if a contact has any of these statuses (REMOVED, REJECTED, PENDING, BLOCKED),
        # it is excluded from queries, allowing the same contact to be added again.
        # For example, if a contact was previously REMOVED, it can be re-added since the relationship is no longer active.
        self.excluded_status = [Status.REMOVED, Status.REJECTED, Status.PENDING, Status.BLOCKED]


    # create a new contact request
    def request_to_add_contact(self, user: User, contact: ContactCreate) -> Contact:
        try:
            # contact with REQUESTED status
            new_contact = Contact(user_id=user.id, username=contact.username, status=Status.REQUESTED)
            self.db.add(new_contact)
            self.db.commit()

            # return the contact object
            return new_contact
        except SQLAlchemyError as e:
            # handle database errors
            self.db.rollback()
            raise ValueError(f"Error requesting new contact: {str(e)}")
    
   
    # update the contact status (e.g. from REQUESTED -> ACCEPTED) 
    def update_contact_status(self, user: User, contact_id: int, status: Status) -> Contact:
        try:
            # retrieve the contact
            contact = self.db.query(Contact).filter(Contact.user_id == user.id, Contact.id == contact_id).first()
            
            if not contact:
                raise ValueError("Contact not found.")
           
            # if ACCEPTED, add the time it was ACCEPTED (added) 
            if status == Status.ACCEPTED:
                contact.date_added = datetime.now()
            # if BLOCKED or REMOVED, remove date_added field
            elif status == Status.BLOCKED or status == Status.REMOVED:
                contact.date_added = None

            contact.last_updated = datetime.now()
            contact.status = status
            self.db.commit()

            # return contact objects
            return contact
        except SQLAlchemyError as e:
            # handle database errors
            self.db.rollback()
            raise ValueError(f"Error updating contact: {str(e)}")


    # get all of the current user's contacts, regardless of status
    def get_all_contacts(self, user: User) -> list[Contact]:
        return self.db.query(Contact).filter(Contact.user_id == user.id).all()
   
   
    # get contact via search criteria (contact id, or contact username) 
    def get_contact(self, contact: ContactSearch) -> Contact:
        if contact.id :
            return self.db.query(Contact).filter(Contact.id == contact.id).first()
        if contact.username:
            return self.db.query(Contact).filter(Contact.username == contact.username).first()


    # check if contact exists by username
    def contact_exists(self, user: User, contact: ContactResponse) -> bool:
        return self.db.query(
            exists().where(
                Contact.user_id == user.id, 
                Contact.username == contact.username,
                not_(Contact.status.in_(self.excluded_status))
            )
        ).scalar()


    # check if contact exists by id
    def contact_exists_by_id(self, user: User, contact_id: int) -> bool:
        return self.db.query(
            exists().where(
                Contact.user_id == user.id, 
                Contact.id == contact_id,
                not_(Contact.status.in_(self.excluded_status))
            )
        ).scalar()