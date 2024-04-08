from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

from routes.auth import create_user, login, add_service, update_user, delete_user, get_user, create_service, update_service, delete_service, get_service

app = Flask(__name__)

# Configuration de la clé secrète pour JWT
app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # Changez ceci en une clé secrète forte dans un environnement de production
jwt = JWTManager(app)

app.add_url_rule('/login', view_func=login, methods=['POST'])

app.add_url_rule('/create_user', view_func=create_user, methods=['POST'])

app.add_url_rule('/update_user', view_func=update_user, methods=['PUT'])

app.add_url_rule('/delete_user', view_func=delete_user, methods=['DELETE'])

app.add_url_rule('/get_user', view_func=get_user, methods=['GET'])

app.add_url_rule('/create_service', view_func=create_service, methods=['POST'])

app.add_url_rule('/update_service', view_func=update_service, methods=['PUT'])

app.add_url_rule('/delete_service', view_func=delete_service, methods=['DELETE'])

app.add_url_rule('/get_service', view_func=get_service, methods=['GET'])

if __name__ == '__main__':
    app.run(debug=True)
