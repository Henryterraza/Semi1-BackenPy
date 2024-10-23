from sqlalchemy import Column, Integer, TIMESTAMP, ForeignKey, func, Text
from sqlalchemy.orm import relationship
from config.db import Base

class Recognition(Base):
    __tablename__ = 'image_recognition_results' 

    result_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    file_id = Column(Integer, ForeignKey('files.file_id', ondelete='CASCADE'), nullable=False)
    recognition_result = Column(Text, nullable=False)
    processed_at = Column(TIMESTAMP, server_default=func.now())
 
    # user = relationship('Users', back_populates='schedules')

    def to_dict(self):
        return {
            'result_id': self.result_id,
            'user_id': self.user_id,
            'file_id': self.file_id,
            'recognition_result': self.recognition_result,
            'processed_at': self.processed_at
        }
