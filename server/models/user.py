from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from database import Base
from models.message import Message
import bcrypt


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    username = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    is_logged_in = Column(Boolean, nullable=False, default=False)

    # Specify foreign keys for the relationships
    messages_sent = relationship("Message", back_populates="sender", foreign_keys=[Message.sender_id])
    messages_received = relationship("Message", back_populates="recipient", foreign_keys=[Message.recipient_id])

    def set_password(self, password: str):
        p = password.encode("utf-8")
        salt = bcrypt.gensalt()
        self.password = bcrypt.hashpw(p, salt).decode("utf-8")
   
    def check_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode("utf-8"), self.password.encode("utf-8"))

    def __repr__(self):
        return f"<User(id={self.id}, name={self.name}, email=({self.email})>"