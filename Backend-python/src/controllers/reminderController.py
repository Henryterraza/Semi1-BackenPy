import os
from models.reminder import Reminder
from models.task import Task
from flask import request, jsonify
from config.db import get_db


def createReminder():
    db = next(get_db())
    try:
        data = request.get_json()
        task_id = data.get('task_id')
        reminder_datetime = data.get('reminder_datetime')

        if not task_id or not reminder_datetime:
            return jsonify({
                "message": "Los campos task_id y reminder_datetime son obligatorios.",
                "status": False,
            }), 400

        new_reminder = Reminder(
            task_id=task_id,
            reminder_datetime=reminder_datetime,
            sent=False  
        )

        db.add(new_reminder)
        db.commit()

        return jsonify({
            "message": "Recordatorio creado exitosamente.",
            "reminder": new_reminder.to_dict(),  # Asegúrate de que el modelo tenga este método
            "status": True,
        }), 201

    except Exception as error:
        print(f"Error al crear recordatorio: {error}")
        return jsonify({
            "message": "Error al crear recordatorio.",
            "error": str(error),
            "status": False,
        }), 500

def getAllReminders():
    db = next(get_db())
    try:
        reminders = db.query(Reminder).all()

        reminders_list = [reminder.to_dict() for reminder in reminders]

        return jsonify({
            "reminders": reminders_list,
            "status": True,
        }), 200

    except Exception as error:
        print(f"Error al obtener recordatorios: {error}")
        return jsonify({
            "message": "Error al obtener recordatorios.",
            "error": str(error),
            "status": False,
        }), 500
    
def getReminderById(reminder_id):
    db = next(get_db())
    try:
        reminder = db.query(Reminder).filter(Reminder.reminder_id == reminder_id).first()

        if not reminder:
            return jsonify({
                "message": "Recordatorio no encontrado.",
                "status": False,
            }), 404

        return jsonify({
            "reminder": reminder.to_dict(),
            "status": True,
        }), 200

    except Exception as error:
        print(f"Error al obtener recordatorio: {error}")
        return jsonify({
            "message": "Error al obtener recordatorio.",
            "error": str(error),
            "status": False,
        }), 500
    
def updateReminder(reminder_id):
    db = next(get_db())
    try:
        reminder = db.query(Reminder).filter(Reminder.reminder_id == reminder_id).first()

        if not reminder:
            return jsonify({
                "message": "Recordatorio no encontrado.",
                "status": False,
            }), 404

        data = request.get_json()
        reminder_datetime = data.get('reminder_datetime')
        sent = data.get('sent')

        if reminder_datetime is not None:
            reminder.reminder_datetime = reminder_datetime
        if sent is not None:
            reminder.sent = sent

        db.commit()  # Guardar los cambios en la base de datos

        return jsonify({
            "message": "Recordatorio actualizado exitosamente.",
            "reminder": reminder.to_dict(),
            "status": True,
        }), 200

    except Exception as error:
        print(f"Error al actualizar recordatorio: {error}")
        return jsonify({
            "message": "Error al actualizar recordatorio.",
            "error": str(error),
            "status": False,
        }), 500
    
def deleteReminder(reminder_id):
    db = next(get_db())
    try:
        reminder = db.query(Reminder).filter(Reminder.reminder_id == reminder_id).first()

        if not reminder:
            return jsonify({
                "message": "Recordatorio no encontrado.",
                "status": False,
            }), 404

        db.delete(reminder)  # Eliminar el recordatorio
        db.commit()  # Guardar cambios en la base de datos

        return jsonify({
            "message": "Recordatorio eliminado exitosamente.",
            "status": True,
        }), 200

    except Exception as error:
        print(f"Error al eliminar recordatorio: {error}")
        return jsonify({
            "message": "Error al eliminar recordatorio.",
            "error": str(error),
            "status": False,
        }), 500
    
def getRemindersByUserId(user_id):
    db = next(get_db())
    try:
        # Consultar los recordatorios basados en el user_id relacionado con tasks
        reminders = db.query(Reminder).join(Task).filter(Task.user_id == user_id).all()

        if not reminders:
            return jsonify({
                "message": "No se encontraron recordatorios para este usuario",
                "status": False,
            }), 404

        return jsonify({
            "reminders": [reminder.to_dictTask() for reminder in reminders],
            "status": True,
        }), 200

    except Exception as error:
        print(f"Error al obtener recordatorios por user_id: {error}")
        return jsonify({
            "message": "Error al obtener recordatorios",
            "error": str(error),
            "status": False,
        }), 500