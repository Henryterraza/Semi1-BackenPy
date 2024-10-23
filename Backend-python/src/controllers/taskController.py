import os
from flask import request, jsonify
import requests
import json

def createTask():
    try:
        data = request.get_json()
        title = data.get('title')
        description = data.get('description')
        user_id = data.get('user_id')
        due_date = data.get('due_date')
        priority = data.get('priority')
        status = data.get('status')

        # Validación de campos requeridos
        if not all([title, description, user_id, due_date, priority, status]):
            return jsonify({
                'message': "Todos los campos son obligatorios: title, description, user_id, due_date, priority, status.",
                'status': False,
            }), 400
        
        body = {
            'title': title,
            'description': description,
            'user_id': user_id,
            'due_date': due_date,
            'priority': priority,
            'status': status,
        }

        # Enviar el cuerpo anidado si es necesario
        response = requests.post(
            f"{os.getenv('APIGATEWAY')}/Test/create-task",
            json={'body': json.dumps(body)}  # Cambiado para anidar como en Node.js
        )

        
        # Manejar errores de respuesta
        if not response.ok:
            error_data = response.json()
            raise Exception(error_data.get('message', 'Error desconocido al crear la tarea'))

        # Deserializar la respuesta
        response_data = response.json()
        task_response = json.loads(response_data.get('body'))  # Deserializamos el cuerpo que viene en 'data.body'

        return jsonify({
            'message': task_response.get('message', 'Tarea creada exitosamente.'),
            'taskId': task_response.get('taskId'),
            'status': True,
        }), 201  # Código de estado 201 para creación exitosa

    except Exception as error:
        print('Error creando la tarea:', error)

        return jsonify({
            'message': 'Error interno al crear la tarea',
            'error': str(error),
            'status': False,
        }), 500


def updateTask(task_id):
    try:
        data = request.get_json()
        title = data.get('title')
        description = data.get('description')
        due_date = data.get('due_date')
        priority = data.get('priority')
        status = data.get('status')

        if not task_id:
            return jsonify({
                'message': "El campo task_id es obligatorio.",
                'status': False,
            }), 400

        body = {
            'title': title,
            'description': description,
            'task_id': task_id,
            'due_date': due_date,
            'priority': priority,
            'status': status,
        }

        response = requests.put(
            f"{os.getenv('APIGATEWAY')}/Test/updateTask",
            json={'body': json.dumps(body)} 
        )

        if not response.ok:
            data = response.json()
            raise Exception(data.get('message', 'Error updating task'))

        response_data = response.json()
        task_response = json.loads(response_data.get('body'))

        return jsonify({
            'message': task_response['message'],
            # 'taskId': task_response['taskId'],
            'status': task_response['status'],
        }), response_data['statusCode']

    except Exception as error:
        print('Error updating task:', error)

        return jsonify({
            'message': 'Error interno al actualizar la tarea',
            'error': str(error),
            'status': False,
        }), 500
    
def deleteTask(task_id):
    try:
        if not task_id:
            return jsonify({
                'message': "El campo task_id es obligatorio.",
                'status': False,
            }), 400
        
        body = {
            'task_id': task_id
        }

        response = requests.delete(
            f"{os.getenv('APIGATEWAY')}/Test/deleteTask",
            json={'body': json.dumps(body)} 
        )

        if not response.ok:
            data = response.json()
            raise Exception(data.get('message', 'Error deleting task'))

        response_data = response.json()
        task_response = json.loads(response_data.get('body'))

        return jsonify({
            'message': task_response['message'],
            # 'taskId': task_response['taskId'],
            'status': task_response['status'],
        }), response_data['statusCode']

    except Exception as error:
        print('Error deleting task:', error)

        return jsonify({
            'message': 'Error interno al eliminar la tarea',
            'error': str(error),
            'status': False,
        }), 500


def getTask(task_id):
    try:
        if not task_id:
            return jsonify({
                'message': "El campo task_id es obligatorio.",
                'status': False,
            }), 400
        
        body = {
            'task_id': task_id
        }

        response = requests.post(
            f"{os.getenv('APIGATEWAY')}/Test/getTaskById",
            json={'body': json.dumps(body)}  
        )

        if not response.ok:
            data = response.json()
            raise Exception(data.get('message', 'Error get task'))

        response_data = response.json()
        task_response = json.loads(response_data.get('body'))

        return jsonify({
            'task': task_response.get('task'),
            'status': task_response.get('status'),
        }), response_data['statusCode']

    except Exception as error:
        print('Error get task:', error)

        return jsonify({
            'message': 'Error interno al obtener la tarea',
            'error': str(error),
            'status': False,
        }), 500

def getAllTask():
    try:
        response = requests.get(
            f"{os.getenv('APIGATEWAY')}/Test/getAllTask",
            headers={'Content-Type': 'application/json'}
        )

        if not response.ok:
            data = response.json()
            raise Exception(data.get('message', 'Error get task'))

        response_data = response.json()
        tasks_response = json.loads(response_data.get('body'))

        return jsonify({
            'tasks': tasks_response.get('tasks'),
            'status': tasks_response.get('status'),
        }), response.status_code

    except Exception as error:
        print('Error get task:', error)

        return jsonify({
            'message': 'Error interno al obtener las tareas',
            'error': str(error),
            'status': False,
        }), 500