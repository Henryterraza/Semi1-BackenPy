from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from sqlalchemy.orm import relationship
from config.db import Base

class User(Base):
    __tablename__ = 'users' 

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    mfa_enabled = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # album = relationship('Album', back_populates='user')

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'full_name': self.full_name,
            'email': self.email,
            'password': self.password,
            'mfa_enabled': self.mfa_enabled,
            'created_at': self.created_at
        }
