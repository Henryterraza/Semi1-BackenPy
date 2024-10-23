from flask import Blueprint
import controllers.reminderController as reminderController

reminderController_bp = Blueprint('reminderController_bp', __name__, url_prefix = '/api')

@reminderController_bp.route('/user/reminder', methods=['POST'])
def createReminder():
    return reminderController.createReminder()

@reminderController_bp.route('/user/reminder/<int:id_reminder>', methods=['PUT'])
def updateReminder(id_reminder):
    return reminderController.updateReminder(id_reminder)

@reminderController_bp.route('/user/reminder/<int:id_reminder>', methods=['DELETE'])
def deleteReminder(id_reminder):
    return reminderController.deleteReminder(id_reminder)

@reminderController_bp.route('/user/reminder/<int:id_reminder>', methods=['GET'])
def getReminderById(id_reminder):
    return reminderController.getReminderById(id_reminder)

@reminderController_bp.route('/user/reminders', methods=['GET'])
def getAllReminders():
    return reminderController.getAllReminders()

@reminderController_bp.route('/user/reminders/<int:id_user>', methods=['GET'])
def getRemindersByUserId(id_user):
    return reminderController.getRemindersByUserId(id_user)