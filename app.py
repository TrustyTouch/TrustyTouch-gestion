from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

from routes.auth import create_account, login, user_info, add_service

app = Flask(__name__)

# Configuration de la clé secrète pour JWT
app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # Changez ceci en une clé secrète forte dans un environnement de production
jwt = JWTManager(app)

@app.route('/ping')
def ping():
    return "pong"

app.add_url_rule('/create_account', view_func=create_account, methods=['POST'])

app.add_url_rule('/login', view_func=login, methods=['POST'])

app.add_url_rule('/user_info', view_func=user_info, methods=['GET'])

app.add_url_rule('/services', view_func=add_service, methods=['POST'])

if __name__ == '__main__':
    app.run(debug=True)
