from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

from data import users, services

# Route pour la création d'un compte utilisateur
def create_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')
    # Stocker les informations utilisateur dans une base de données
    users[username] = {'password': password, 'role': role}
    return jsonify({'message': 'Compte utilisateur créé avec succès'})

# Route pour la modification d'un compte utilisateur
def update_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    # Stocker les informations utilisateur dans une base de données
    users[username] = {'password': password}
    return jsonify({'message': 'Utilisateur modifié avec succès'})

# Route pour la suppression d'un compte utilisateur
def delete_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    # Stocker les informations utilisateur dans une base de données
    users[username] = {'password': password}
    return jsonify({'message': 'Utilisateur supprimé avec succès'})

# Route pour la récupération d'un compte utilisateur
def get_user():
    data = request.get_json()
    username = data.get('username')
    # Stocker les informations utilisateur dans une base de données
    users[username] = {}
    return jsonify({'message': 'Utilisateur trouvé avec succès'})