from sqlalchemy import Column, Integer, String, Text, Date, Enum, ForeignKey, func, TIMESTAMP
from sqlalchemy.orm import relationship
from config.db import Base
import enum


class PriorityEnum(enum.Enum):
    alta = 'alta'
    media = 'media'
    baja = 'baja'

# Define un Enum para los estados
class StatusEnum(enum.Enum):
    pendiente = 'pendiente'
    en_progreso = 'en progreso'
    completada = 'completada'

class Task(Base):
    __tablename__ = 'tasks' 

    task_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    due_date = Column(Date, nullable=False)
    priority = Column(Enum(PriorityEnum), nullable=False)
    status = Column(Enum(StatusEnum), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    
    reminders = relationship('Reminder', back_populates='task')

    def to_dict(self):
        return {
            'task_id': self.task_id,
            'user_id': self.user_id,
            'title': self.title,
            'description': self.description,
            'due_date': self.due_date,
            'priority': self.priority.value,
            'status': self.status.value,
            'created_at': self.created_at
        }