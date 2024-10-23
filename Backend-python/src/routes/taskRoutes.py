from flask import Blueprint
import controllers.taskController as taskController

taskController_bp = Blueprint('taskController_bp', __name__, url_prefix = '/api')

@taskController_bp.route('/user/task', methods=['POST'])
def createTask():
    return taskController.createTask()

@taskController_bp.route('/user/task/<int:id_task>', methods=['PUT'])
def updateTask(id_task):
    return taskController.updateTask(id_task)

@taskController_bp.route('/user/task/<int:id_task>', methods=['DELETE'])
def deleteTask(id_task):
    return taskController.deleteTask(id_task)

@taskController_bp.route('/user/task/<int:id_task>', methods=['GET'])
def getTask(id_task):
    return taskController.getTask(id_task)

@taskController_bp.route('/user/tasks', methods=['GET'])
def getAllTask():
    return taskController.getAllTask()



