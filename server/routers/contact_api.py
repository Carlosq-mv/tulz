from fastapi import APIRouter, Depends, Request

from schemas.contact_schema import *
from actions.services.contactService import ContactService
from dependencies import get_contact_services

c_api = APIRouter()


# add a contact API route
@c_api.post("/add-contact", response_model=ContactResponse)
async def add_contact(request: Request, contact: ContactCreate, contact_service: ContactService = Depends(get_contact_services)) -> ContactResponse:
    return await contact_service.add_contact(user=request.state.user, contact=contact)


# get all of users contacts API route
@c_api.get("/my-contacts", response_model=list[ContactResponse])
async def get_my_contacts(request: Request, contact_service: ContactService = Depends(get_contact_services)) -> list[ContactResponse]:
    return await contact_service.get_all_contacts(user=request.state.user)


# block a certain contact API route
@c_api.put("/block-contact/{contact_id}", response_model=ContactResponse)
async def block_contact(request: Request, contact_id: int, contact_service: ContactService = Depends(get_contact_services)) -> ContactResponse:
    return await contact_service.block_contact(user=request.state.user, id=contact_id)


# unblock a certain contact API route
@c_api.put("/unblock-contact/{contact_id}", response_model=ContactResponse)
async def unblock_contact(request: Request, contact_id: int, contact_service: ContactService = Depends(get_contact_services)) -> ContactResponse:
    return await contact_service.unblock_contact(user=request.state.user, id=contact_id)


# accept a certain contact request API route
@c_api.put("/accept-contact/{contact_id}", response_model=ContactResponse)
async def accept_contact(request: Request, contact_id: int, contact_service: ContactService = Depends(get_contact_services)) -> ContactResponse:
    return await contact_service.accept_contact(user=request.state.user, id=contact_id)


# reject a certain contact request API route
@c_api.put("/reject-contact/{contact_id}", response_model=ContactResponse)
async def reject_contact(request: Request, contact_id: int, contact_service: ContactService = Depends(get_contact_services)) -> ContactResponse:
    return await contact_service.reject_contact(user=request.state.user, id=contact_id)


# remove a certain contact API route
@c_api.put("/remove-contact/{contact_id}", response_model=ContactResponse)
async def remove_contact(request: Request, contact_id: int, contact_service: ContactService = Depends(get_contact_services)) -> ContactResponse:
    return await contact_service.remove_contact(user=request.state.user, id=contact_id)


# get a certain contact by ContactSearch API route
@c_api.get("/get-contact/", response_model=ContactResponse)
async def get_contact(contact_criteria: ContactSearch = Depends(), contact_service: ContactService = Depends(get_contact_services)) -> ContactResponse:
    return await contact_service.get_contact(contact_criteria)