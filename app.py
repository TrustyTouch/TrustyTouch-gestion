import sys
from signal import signal, SIGTERM, SIGINT

from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

from routes.auth import login
from data.services import create_service, update_service, delete_service, get_service
from data.users import create_user, update_user, delete_user, get_users, get_user

app = Flask(__name__)

# Configuration de la clé secrète pour JWT
app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # Changez ceci en une clé secrète forte dans un environnement de production
jwt = JWTManager(app)

app.add_url_rule('/login', view_func=login, methods=['POST'])

app.add_url_rule('/create_user', view_func=create_user, methods=['POST'])

app.add_url_rule('/update_user', view_func=update_user, methods=['PUT'])

app.add_url_rule('/delete_user', view_func=delete_user, methods=['DELETE'])

app.add_url_rule('/get_users', view_func=get_users, methods=['GET'])

app.add_url_rule('/get_user=', view_func=get_user, methods=['GET'])

app.add_url_rule('/create_service', view_func=create_service, methods=['POST'])

app.add_url_rule('/update_service', view_func=update_service, methods=['PUT'])

app.add_url_rule('/delete_service', view_func=delete_service, methods=['DELETE'])

app.add_url_rule('/get_service', view_func=get_service, methods=['GET'])

def handle_signal(*args, **kwargs):
    sys.exit(0)
signal(SIGTERM, handle_signal)
# signal(SIGINT, handle_signal)

if __name__ == '__main__':
    app.run(debug=True)
