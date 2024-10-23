from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os

from routes.userRoutes import userController_bp
from routes.taskRoutes import taskController_bp
from routes.sheduleRoutes import sheduleController_bp
from routes.reminderRoutes import reminderController_bp
from routes.fileRoutes import fileController_bp
from routes.translateRoutes import translateController_bp
from routes.rekognitionRoutes import rekognitionController_bp
from routes.pollyRoutes import pollyController_bp

server = Flask(__name__)
CORS(server)
load_dotenv()
PORT = int(os.getenv('PORT'))

server.register_blueprint(userController_bp)
server.register_blueprint(taskController_bp)
server.register_blueprint(sheduleController_bp)
server.register_blueprint(reminderController_bp)
server.register_blueprint(fileController_bp)
server.register_blueprint(translateController_bp)
server.register_blueprint(rekognitionController_bp)
server.register_blueprint(pollyController_bp)

@server.route('/', methods=['GET'])
def home():
    return jsonify({'message':'Servidor Python'})

if __name__ == '__main__':
    server.run(host='0.0.0.0', debug=True, port=PORT)