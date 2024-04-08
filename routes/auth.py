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

# Route pour la création d'un compte utilisateur
def create_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    # Stocker les informations utilisateur dans une base de données
    users[username] = {'password': password, 'services': []}
    return jsonify({'message': 'Compte utilisateur créé avec succès'})

# Route pour la modification d'un compte utilisateur
def update_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    # Stocker les informations utilisateur dans une base de données
    users[username] = {'password': password, 'services': []}
    return jsonify({'message': 'Compte utilisateur créé avec succès'})

# Route pour la suppression d'un compte utilisateur
def delete_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    # Stocker les informations utilisateur dans une base de données
    users[username] = {'password': password, 'services': []}
    return jsonify({'message': 'Compte utilisateur créé avec succès'})

# Route pour la récupération d'un compte utilisateur
def get_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    # Stocker les informations utilisateur dans une base de données
    users[username] = {'password': password, 'services': []}
    return jsonify({'message': 'Compte utilisateur créé avec succès'})

# Route pour la création des services proposés par les prestataires
@jwt_required()  # L'utilisateur doit être authentifié pour accéder à cette route
def create_service():
    data = request.get_json()
    service_name = data.get('service_name')
    provider = data.get('provider')
    # Stocker les informations sur le service dans une base de données
    services[service_name] = {'provider': provider}
    return jsonify({'message': 'Service ajouté avec succès'})

# Route pour la modification des services proposés par les prestataires
@jwt_required()  # L'utilisateur doit être authentifié pour accéder à cette route
def update_service():
    data = request.get_json()
    service_name = data.get('service_name')
    provider = data.get('provider')
    # Stocker les informations sur le service dans une base de données
    services[service_name] = {'provider': provider}
    return jsonify({'message': 'Service ajouté avec succès'})

# Route pour la suppression des services proposés par les prestataires
@jwt_required()  # L'utilisateur doit être authentifié pour accéder à cette route
def delete_service():
    data = request.get_json()
    service_name = data.get('service_name')
    provider = data.get('provider')
    # Stocker les informations sur le service dans une base de données
    services[service_name] = {'provider': provider}
    return jsonify({'message': 'Service ajouté avec succès'})

# Route pour la récupération des services proposés par les prestataires
@jwt_required()  # L'utilisateur doit être authentifié pour accéder à cette route
def get_service():
    data = request.get_json()
    service_name = data.get('service_name')
    provider = data.get('provider')
    # Stocker les informations sur le service dans une base de données
    services[service_name] = {'provider': provider}
    return jsonify({'message': 'Service ajouté avec succès'})

if __name__ == '__main__':
    app.run(debug=True)
