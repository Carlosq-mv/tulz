from datetime import datetime
from sqlalchemy import and_, exists, not_, or_
from sqlalchemy.orm import Session, joinedload
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
    def create_contact(self, c: ContactForm) -> Contact:
        try:
            # create new contact with REQUESTED status
            new_contact = Contact(
                current_user_id=c.current_user_id,
                friend_id=c.friend_id,
                status=Status.REQUESTED,
                last_updated=datetime.now()
            )
            self.db.add(new_contact)
            self.db.commit()

            # return the contact object
            return new_contact
        except SQLAlchemyError as e:
            # handle database errors
            self.db.rollback()
            raise ValueError(f"Error requesting new contact: {str(e)}")
    
   
    # update the contact status (e.g. from REQUESTED -> ACCEPTED) 
    def update_contact_status(self, identifier: ContactForm | int, status: Status, user: User | None = None) -> Contact:
        try:
            # Determine if the identifier is a ContactForm or an ID
            if isinstance(identifier, ContactForm):
                # Query based on current_user_id and friend_id
                contact = (
                    self.db.query(Contact)
                    .filter(
                        Contact.current_user_id == identifier.current_user_id,
                        Contact.friend_id == identifier.friend_id,
                    )
                    .first()
                )
            elif isinstance(identifier, int):
                # Query based on the contact ID
                contact = self.db.query(Contact).filter(
                    and_(
                       or_(
                           Contact.current_user_id == user.id, 
                           Contact.friend_id == user.id, 
                       ),
                       Contact.id == identifier
                    )
                ).first()

            
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

            # return contact object
            return contact
        except SQLAlchemyError as e:
            # handle database errors
            self.db.rollback()
            raise ValueError(f"Error updating contact: {str(e)}")


    # get all of the current user's contacts, regardless of status
    def get_all_contacts(self, user: User) -> list[Contact]:
        return self.db.query(Contact).filter(
            Contact.current_user_id == user.id
        ).all()

    # TODO: temp sol'n 
    # get contacts by status
    def get_contacts(self, user: User, status: Status):
        data = (self.db.query(Contact)
                    .join(User, or_(Contact.current_user_id == User.id, Contact.friend_id == User.id))
                    .filter(
                        and_ (
                            or_ (
                                Contact.current_user_id == User.id, 
                                Contact.friend_id == User.id 
                            ),
                            Contact.status == status,
                        )
                    )
                    .options(
                        joinedload(Contact.user_1).defer(User.password),
                        joinedload(Contact.user_2).defer(User.password),
                             )
                    .all()
                )
        result = []
        for contact in data:
            # determine which user is not the current user and assign as the 'other user'
            if contact.current_user_id == user.id:
                contact.other_user = contact.user_2
            else:
                contact.other_user = contact.user_1

            # add the contact j
            result.append(contact)
        
        return result
   
    # get all the request sent by the current user 
    def get_requests_sent(self, user: User):
        return (self.db.query(Contact)
                    .filter(Contact.current_user_id == user.id, Contact.status == Status.REQUESTED)
                    .options(
                        joinedload(Contact.user_2).defer(User.password)
                    )
                    .all()
                )
        

    # get contact via search criteria (contact id, or contact username) 
    def search_contact(self, criteria: ContactSearch) -> Contact:
        if criteria.id :
            return self.db.query(Contact).filter(Contact.id == criteria.id).first()
        if criteria.username:
            # perform a join
            return (self.db.query(Contact, User.username)
                .join(User, or_(
                    User.id == Contact.requester_id,  # Join on requester
                    User.id == Contact.receiver_id     # Or join on receiver
                ))
                .filter(User.username == criteria.username)
                .first()
            )
            # return self.db.query(Contact).filter(Contact.username == criteria.username).first()


    def get_contact_requests_to_me(self, user: User):
        return (self.db.query(Contact)
                    .join(User, Contact.friend_id == User.id)   # Join on the friend user (receiver of the request)
                    .filter(
                        Contact.friend_id == user.id,           # Exclude self-contacts (if applicable)
                        Contact.status == Status.REQUESTED      # Filter by Requested status
                    )
                    .options(joinedload(Contact.user_1))     # Load the user details of the foreign user
                    .all()
                )
       
        
    # check if contact exists 
    def contact_exists(self, c: ContactForm) -> bool:
        return self.db.query(
            exists().where(
                and_(
                   or_(
                        Contact.current_user_id == c.current_user_id, 
                        Contact.friend_id == c.current_user_id,
                    ), 
                    or_(
                        Contact.friend_id == c.friend_id,
                        Contact.current_user_id == c.friend_id,
                    ),
                    not_(Contact.status.in_(self.excluded_status))
                )
            )
        ).scalar()

    def contact_exists_by_id(self, user: User, contact_id: int) -> bool:
        res = self.db.query(
            exists().where(
                and_(
                    or_(
                        Contact.current_user_id == user.id, 
                        Contact.friend_id == user.id
                    ),
                    Contact.id == contact_id,
                    not_(Contact.status.in_(self.excluded_status))
                )
            )
        ).scalar()
        print(res, contact_id, user)
        return res