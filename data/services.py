from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

from data import users, services

# Route pour la création des services proposés par les prestataires
@jwt_required()  # L'utilisateur doit être authentifié pour accéder à cette route
def create_service():
    data = request.get_json()
    service_name = data.get('service_name')
    createur = data.get('createur')
    # Stocker les informations sur le service dans une base de données
    services[service_name] = {'createur': createur}
    return jsonify({'message': 'Service ajouté avec succès'})

# Route pour la modification des services proposés par les prestataires
@jwt_required()  # L'utilisateur doit être authentifié pour accéder à cette route
def update_service():
    data = request.get_json()
    service_name = data.get('service_name')
    createur = data.get('createur')
    # Stocker les informations sur le service dans une base de données
    services[service_name] = {'createur': createur}
    return jsonify({'message': 'Service modifié avec succès'})

# Route pour la suppression des services proposés par les prestataires
@jwt_required()  # L'utilisateur doit être authentifié pour accéder à cette route
def delete_service():
    data = request.get_json()
    service_name = data.get('service_name')
    createur = data.get('createur')
    # Stocker les informations sur le service dans une base de données
    services[service_name] = {'createur': createur}
    return jsonify({'message': 'Service supprimé avec succès'})

# Route pour la récupération des services proposés par les prestataires
@jwt_required()  # L'utilisateur doit être authentifié pour accéder à cette route
def get_service():
    data = request.get_json()
    service_name = data.get('service_name')
    createur = data.get('createur')
    # Stocker les informations sur le service dans une base de données
    services[service_name] = {'createur': createur}
    return jsonify({'message': 'Service trouvé avec succès'})
