from enum import Enum

class Status(str, Enum):
    PENDING = "PENDING"         # Initial state when a request is created
    REQUESTED = "REQUESTED"     # A user has requested to add the contact
    ACCEPTED = "ACCEPTED"       # The contact request has been accepted
    REJECTED = "REJECTED"       # The contact request has been explicitly rejected
    BLOCKED = "BLOCKED"         # The contact is blocked by the user
    REMOVED = "REMOVED"         # The contact has been removed from the user's list