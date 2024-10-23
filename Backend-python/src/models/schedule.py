from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from config.db import Base

class Schedule(Base):
    __tablename__ = 'schedules' 

    schedule_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    course_name = Column(String(255), nullable=False)
    professor = Column(String(255))
    location = Column(String(255))
    event_datetime = Column(DateTime(timezone=True), nullable=False)

    # user = relationship('Users', back_populates='schedules')

    def to_dict(self):
        return {
            'schedule_id': self.schedule_id,
            'user_id': self.user_id,
            'course_name': self.course_name,
            'professor': self.professor,
            'location': self.location,
            'event_datetime': self.event_datetime
        }
