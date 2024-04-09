from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

from data import users, services

app = Flask(__name__)

# Configuration de la clé secrète pour JWT
app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # Changez ceci en une clé secrète forte dans un environnement de production
jwt = JWTManager(app)

# Route pour la connexion d'un utilisateur
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if username in users and users[username]['password'] == password:
        # Créer un jeton d'accès JWT valide pour cet utilisateur
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token)
    else:
        return jsonify({'message': 'Nom d\'utilisateur ou mot de passe incorrect'})

if __name__ == '__main__':
    app.run(debug=True)
