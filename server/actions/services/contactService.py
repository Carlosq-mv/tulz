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


    async def add_contact(self, user: User, contact: ContactCreate) -> ContactResponse:
        await self.has_empty_fields(contact)
        await self.self_contact(user, contact)
        await self.contact_exists(user, contact)
        await self.user_contact_exists(contact.username)
        
        return self.dao.request_to_add_contact(user, contact)


    async def remove_contact(self, user: User, id: int) -> ContactResponse:
        await self.contact_exists_by_id(user, id)
        return self.dao.update_contact_status(user, id, Status.REMOVED) 
   
    
    async def block_contact(self, user: User, id: int) -> ContactResponse:
        await self.contact_exists_by_id(user, id)
        return self.dao.update_contact_status(user, id, Status.BLOCKED)


    async def accept_contact(self, user: User, id: int) -> ContactResponse:
        await self.contact_exists_by_id(user, id)
        return self.dao.update_contact_status(user, id, Status.ACCEPTED)

    
    async def reject_contact(self, user: User, id: int) -> ContactResponse:
        await self.contact_exists_by_id(user, id)
        return self.dao.update_contact_status(user, id, Status.REJECTED)


    async def unblock_contact(self, user: User, id: int) -> ContactResponse:
        await self.contact_exists_by_id(user, id)
        return self.dao.update_contact_status(user, id, Status.PENDING)
    

    async def get_all_contacts(self, user: User) -> list[ContactResponse]:
        return self.dao.get_all_contacts(user)
    
    #TODO: finish these service methods & the dao methods associated with this
    async def get_blocked_contacts():
        pass

    async def get_my_contacts():
        pass

    async def get_requests_for_contact():
        pass



    async def get_contact(self, contact_criteria: ContactSearch) -> ContactResponse:
        if contact_criteria is None:
            raise HTTPException(status_code=400, detail="No search criteria present.")

        if contact_criteria.id is None and contact_criteria.user_id is None and contact_criteria.username is None:
            raise HTTPException(status_code=400, detail="No search criteria present.")

        contact = self.dao.get_contact(contact_criteria)
        if contact is None:
            raise HTTPException(status_code=400, detail="Contact does not exist.")
        
        return contact


    async def user_contact_exists(self, username: str) -> None:
        if self.user_dao.get_user_by_username(username) is None:
            raise HTTPException(status_code=400, detail="User does not exists.")


    async def contact_exists_by_id(self, user: User, contact_id: int) -> None:
        if not self.dao.contact_exists_by_id(user, contact_id):
            raise HTTPException(status_code=400, detail="Can not delete this contact.")    
    
    async def contact_exists(self, user: User, contact: ContactResponse) -> None:
        if self.dao.contact_exists(user, contact):
             raise HTTPException(status_code=400, detail="User is already in your contact list.")


    async def has_empty_fields(self, contact: ContactCreate) -> None:
        if not contact.username:
            raise HTTPException(status_code=400, detail="Username needed to add contact.")
    

    async def self_contact(self, user: User, contact: ContactCreate) -> None:
        if user.username == contact.username:
            raise HTTPException(status_code=400, detail="Can not add yourself as a contact.")
    