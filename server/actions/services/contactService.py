from fastapi import HTTPException
from schemas.contact_schema import *
from actions.dal.contactDAO import ContactDAO
from actions.dal.usersDAO import UserDAO
from models.contact import Contact
from models.user import User
from models.enum.status import Status


class ContactService():
    def __init__(self, dao: ContactDAO, user_dao: UserDAO):
        self.dao = dao
        self.user_dao = user_dao


    async def add_contact(self, contact: ContactForm) -> ContactResponse:
        await self.has_empty_fields(contact)    # check if the payload is present
        await self.is_self_contact(contact)   # check current user isn't adding themself as contact
        await self.contact_exists(contact)    # check if the contact already exists
        await self.does_user_exists(contact)        # check if the user to be added as contact, exists
        # add/create the new contact between the current user, and the recipient
        return self.dao.create_contact(contact)


    async def remove_contact(self, user: User, id: int) -> ContactResponse:
        await self.contact_exists_by_id(user, id)
        return self.dao.update_contact_status(id, Status.REMOVED, user)

   
    async def block_contact(self, user: User, id: int) -> ContactResponse:
        await self.contact_exists_by_id(user, id)
        return self.dao.update_contact_status(id, Status.BLOCKED, user)


    async def accept_contact(self, user: User, id: int) -> ContactResponse:
        await self.contact_exists_by_id(user, id)
        return self.dao.update_contact_status(id, Status.ACCEPTED, user)

    
    async def reject_contact(self, user: User, id: int) -> ContactResponse:
        await self.contact_exists_by_id(user, id)
        return self.dao.update_contact_status(id, Status.REJECTED, user)


    async def unblock_contact(self, user: User, id: int) -> ContactResponse:
        await self.contact_exists_by_id(user, id)
        return self.dao.update_contact_status(id, Status.PENDING, user)
    

    async def get_all_contacts(self, user: User) -> list[ContactResponse]:
        return self.dao.get_all_contacts(user)
    
    
    async def get_contact_requests_to_me(self, user: User):
        return self.dao.get_contact_requests_to_me(user)
    
    async def get_blocked_contacts(self, user: User):
        return self.dao.get_contacts(user, Status.BLOCKED)


    async def get_my_contacts(self, user: User):
        return self.dao.get_contacts(user, Status.ACCEPTED)


    async def get_requests_sent(self, user: User):
        return self.dao.get_requests_sent(user)


    async def search_contact(self, contact_criteria: ContactSearch) -> ContactResponse:
        if contact_criteria is None:
            raise HTTPException(status_code=400, detail="No search criteria present.")

        if contact_criteria.id is None and contact_criteria.user_id is None and contact_criteria.username is None:
            raise HTTPException(status_code=400, detail="No search criteria present.")

        contact = self.dao.search_contact(contact_criteria)
        if contact is None:
            raise HTTPException(status_code=400, detail="Contact does not exist.")
        
        return contact


    async def does_user_exists(self, c: ContactForm) -> None:
        if self.user_dao.get_user_by_id(c.friend_id) is None:
            raise HTTPException(status_code=400, detail="User does not exists.")


    async def contact_exists_by_id(self, user: User, contact_id: int) -> None:
        if not self.dao.contact_exists_by_id(user, contact_id):
            raise HTTPException(status_code=400, detail="Contact does not exist.")    
    
    async def contact_exists(self, c: ContactResponse) -> None:
        print(self.dao.contact_exists(c))
        if self.dao.contact_exists(c):
             raise HTTPException(status_code=400, detail="User is already in your contact list.")


    async def has_empty_fields(self, c: ContactForm) -> None:
        if not c.current_user_id or not c.friend_id:
            raise HTTPException(status_code=400, detail="Fill required fields to add contact.")
    

    async def is_self_contact(self, c: ContactForm) -> None:
        if c.current_user_id == c.friend_id:
            raise HTTPException(status_code=400, detail="Can not add yourself as a contact.")
    