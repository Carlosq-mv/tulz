from sqlalchemy import Column, Integer, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship
from database import Base
from models.enum.status import Status
from datetime import datetime

class Contact(Base):
    __tablename__ = "contacts"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # References to the two users involved in the contact
    current_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    friend_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Contact status (mutual connection between the users)
    status = Column(Enum(Status), default=Status.PENDING, nullable=False)
    
    # The date the contact was accepted 
    date_added = Column(DateTime, default=None, nullable=True)
    
    # Last updated timestamp
    last_updated = Column(DateTime, default=datetime.now(), onupdate=datetime.now, nullable=False)
    
    # Relationships to the user records (two-way relationship)
    user_1 = relationship("User", foreign_keys=[current_user_id], backref="contact_1")
    user_2 = relationship("User", foreign_keys=[friend_id], backref="contact_2")

    def __repr__(self):
        return f"<Contact(id={self.id}, current_user_id={self.current_user_id}, friend_id={self.friend_id}, status={self.status})>"
