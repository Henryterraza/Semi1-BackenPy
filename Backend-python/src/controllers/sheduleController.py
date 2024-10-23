from models.schedule import Schedule
import os
from flask import request, jsonify
from config.db import get_db


def createSchedule():
    db = next(get_db())
    try:
        data = request.get_json()

        user_id = data.get('user_id')
        course_name = data.get('course_name')
        event_datetime = data.get('event_datetime')
        professor = data.get('professor')
        location = data.get('location')

        if not user_id or not course_name or not event_datetime:
            return jsonify({
                "message": "user_id, course_name y event_datetime son campos obligatorios.",
                "status": False
            }), 400
        
        new_schedule = Schedule(
            user_id=user_id,
            course_name=course_name,
            event_datetime=event_datetime,
            professor=professor,
            location=location
        )

        db.add(new_schedule)
        db.commit()

        return jsonify({
            "message": "Horario creado exitosamente",
            "schedule": new_schedule.to_dict(),
            "status": True
        }), 201

    except Exception as error:
        print(f"Error al crear el horario: {error}")
        return jsonify({
            "message": "Error en la creación del horario",
            "error": str(error),
            "status": False
        }), 500


def getAllSchedules():
    db = next(get_db())
    try:
        schedules = db.query(Schedule).all()

        schedules_list = [schedule.to_dict() for schedule in schedules]

        return jsonify({
            "schedules": schedules_list,
            "status": True
        }), 200

    except Exception as error:
        print(f"Error al obtener los horarios: {error}")
        return jsonify({
            "message": "Error al obtener los horarios",
            "error": str(error),
            "status": False
        }), 500
    

def getScheduleById(schedule_id):
    db = next(get_db())
    try:
        schedule = db.query(Schedule).filter_by(schedule_id=schedule_id).first()

        if not schedule:
            return jsonify({
                "message": "Horario no encontrado",
                "status": False
            }), 404

        return jsonify({
            "schedule": schedule.to_dict(),  # Método to_dict() necesario en el modelo Schedule
            "status": True
        }), 200

    except Exception as error:
        print(f"Error al obtener el horario: {error}")
        return jsonify({
            "message": "Error al obtener el horario",
            "error": str(error),
            "status": False
        }), 500


def updateSchedule(schedule_id):
    db = next(get_db())
    try:
        data = request.get_json()

        schedule = db.query(Schedule).filter_by(schedule_id=schedule_id).first()

        if not schedule:
            return jsonify({
                "message": "Horario no encontrado",
                "status": False
            }), 404

        schedule.user_id = data.get('user_id', schedule.user_id)
        schedule.course_name = data.get('course_name', schedule.course_name)
        schedule.event_datetime = data.get('event_datetime', schedule.event_datetime)
        schedule.professor = data.get('professor', schedule.professor)
        schedule.location = data.get('location', schedule.location)

        db.commit()

        return jsonify({
            "message": "Horario actualizado exitosamente",
            "schedule": schedule.to_dict(),
            "status": True
        }), 200

    except Exception as error:
        print(f"Error al actualizar el horario: {error}")
        return jsonify({
            "message": "Error al actualizar el horario",
            "error": str(error),
            "status": False
        }), 500

def deleteSchedule(schedule_id):
    db = next(get_db())
    try:
        schedule = db.query(Schedule).filter_by(schedule_id=schedule_id).first()

        if not schedule:
            return jsonify({
                "message": "Horario no encontrado",
                "status": False
            }), 404

        db.delete(schedule)
        db.commit()

        return jsonify({
            "message": "Horario eliminado exitosamente",
            "status": True
        }), 200

    except Exception as error:
        print(f"Error al eliminar el horario: {error}")
        return jsonify({
            "message": "Error al eliminar el horario",
            "error": str(error),
            "status": False
        }), 500
    
def getSchedulesByUserId(user_id):
    db = next(get_db())
    try:
        # Consultar los horarios basados en el user_id
        schedules = db.query(Schedule).filter_by(user_id=user_id).all()

        if len(schedules) == 0:
            return jsonify({
                "message": "No se encontraron horarios para este usuario",
                "status": False
            }), 404

        schedules_list = [schedule.to_dict() for schedule in schedules]

        return jsonify({
            "schedules": schedules_list,
            "status": True
        }), 200

    except Exception as error:
        print(f"Error al obtener horarios por user_id: {error}")
        return jsonify({
            "message": "Error al obtener horarios",
            "error": str(error),
            "status": False
        }), 500