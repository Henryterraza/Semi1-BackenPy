from flask import Blueprint
import controllers.fileController as fileController

fileController_bp = Blueprint('fileController_bp', __name__, url_prefix = '/api')

@fileController_bp.route('/user/file', methods=['POST'])
def uploadFile():
    return fileController.uploadFile()

@fileController_bp.route('/user/file/<int:id_file>', methods=['DELETE'])
def deleteFile(id_file):
    return fileController.deleteFile(id_file)

@fileController_bp.route('/user/file/<int:id_file>', methods=['GET'])
def getFileById(id_file):
    return fileController.getFileById(id_file)

@fileController_bp.route('/user/files', methods=['GET'])
def getAllFiles():
    return fileController.getAllFiles()

@fileController_bp.route('/user/files/<int:id_user>', methods=['GET'])
def getFilesByUserId(id_user):
    return fileController.getFilesByUserId(id_user)