from flask import Blueprint
import controllers.translateController as translateController

translateController_bp = Blueprint('translateController_bp', __name__, url_prefix = '/api')

@translateController_bp.route('/user/trasnlate', methods=['POST'])
def translateDocument():
    return translateController.translateDocument()

