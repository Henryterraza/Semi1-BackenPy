from flask import Blueprint
import controllers.pollyController as pollyController

pollyController_bp = Blueprint('pollyController_bp', __name__, url_prefix = '/api')

@pollyController_bp.route('/user/polly', methods=['POST'])
def textToSpeech():
    return pollyController.textToSpeech()
