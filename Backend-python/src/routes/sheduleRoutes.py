from flask import Blueprint
import controllers.sheduleController as sheduleController

sheduleController_bp = Blueprint('sheduleController_bp', __name__, url_prefix = '/api')

@sheduleController_bp.route('/user/shedule', methods=['POST'])
def createSchedule():
    return sheduleController.createSchedule()

@sheduleController_bp.route('/user/shedule/<int:id_shedule>', methods=['PUT'])
def updateSchedule(id_shedule):
    return sheduleController.updateSchedule(id_shedule)

@sheduleController_bp.route('/user/shedule/<int:id_shedule>', methods=['DELETE'])
def deleteSchedule(id_shedule):
    return sheduleController.deleteSchedule(id_shedule)

@sheduleController_bp.route('/user/shedule/<int:id_shedule>', methods=['GET'])
def getScheduleById(id_shedule):
    return sheduleController.getScheduleById(id_shedule)

@sheduleController_bp.route('/user/shedules', methods=['GET'])
def getAllSchedules():
    return sheduleController.getAllSchedules()

@sheduleController_bp.route('/user/shedules/<int:id_user>', methods=['GET'])
def getSchedulesByUserId(id_user):
    return sheduleController.getSchedulesByUserId(id_user)