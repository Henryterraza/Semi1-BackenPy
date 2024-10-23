from flask import Blueprint
import controllers.rekognitionController as rekognitionController

rekognitionController_bp = Blueprint('rekognitionController_bp', __name__, url_prefix = '/api')

@rekognitionController_bp.route('/user/rekognition', methods=['POST'])
def imageRecognition():
    return rekognitionController.imageRecognition()

