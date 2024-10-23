from flask import Blueprint
import controllers.userController as userController

userController_bp = Blueprint('userController_bp', __name__, url_prefix = '/api')

@userController_bp.route('/users/register', methods=['POST'])
def createUser():
    return userController.createUser()

@userController_bp.route('/auth/confirm', methods=['POST'])
def comfirmUser():
    return userController.confirmUser()

@userController_bp.route('/auth/login', methods=['POST'])
def authUser():
    return userController.authUser()

@userController_bp.route('/users/profile/<int:id_user>', methods=['GET'])
def getUserProfile(id_user):
    return userController.getUserProfile(id_user)

@userController_bp.route('/users/profile/<int:id_user>', methods=['PUT'])
def updateUserProfile(id_user):
    return userController.updateUserProfile(id_user)

@userController_bp.route('/users/delete/<int:id_user>', methods=['DELETE'])
def deleteUser(id_user):
    return userController.deleteUser(id_user)
