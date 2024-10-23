from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, func
from sqlalchemy.orm import relationship
from config.db import Base

class File(Base):
    __tablename__ = 'files' 

    file_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    file_name = Column(String(255), nullable=False)
    file_type = Column(String(255), nullable=False)
    s3_path = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

    # user = relationship('Users', back_populates='schedules')

    def to_dict(self):
        return {
            'file_id': self.file_id,
            'user_id': self.user_id,
            'file_name': self.file_name,
            'file_type': self.file_type,
            's3_path': self.s3_path,
            'created_at': self.created_at
        }
