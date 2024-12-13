from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship
from database import Base
from models.enum.status import Status
from datetime import datetime


class Contact(Base):
    __tablename__= "contacts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False) 
    status = Column(Enum(Status), default=Status.PENDING, nullable=False)
    date_added = Column(DateTime, default=None, nullable=True)
    last_updated = Column(DateTime, default=datetime.now(), onupdate=datetime.now, nullable=False)

    user = relationship("User", back_populates="contacts")  

    def __repr__(self):
        return f"<Contact(id={self.id}, foregin_id={self.user_id}, username={self.username}, status={self.status})"
