from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

import psycopg2

# Configuration de la connexion à la base de données
conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="postgres",
    host="host.docker.internal",
    port="5432"
)

# Route pour la création de service proposé par un prestataire par l'ID
def create_service():
    # Récupérer les données du service à partir de la requête JSON
    data = request.json
    nom = data.get('nom')

    # Créer un nouvel enregistrement de service dans la base de données
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO services (titre) VALUES (%s) RETURNING id", (nom,))
        service_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        return jsonify({'id': id, 'nom': nom}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500

# Route pour la modification d'un service proposé par un prestataire par l'ID
def update_service(id):
    # Récupérer les données mises à jour du service à partir de la requête JSON
    data = request.json
    nom = data.get('nom')

    # Mettre à jour l'enregistrement de service dans la base de données
    try:
        cur = conn.cursor()
        cur.execute("UPDATE services SET nom = %s WHERE id = %s", (nom, id))
        conn.commit()
        cur.close()
        return jsonify({'message': 'Service mis à jour avec succès'}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500

# Route pour la suppression d'un service proposé par un prestataire par l'ID
def delete_service(id):
    # Supprimer l'enregistrement de service de la base de données
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM services WHERE id = %s", (id,))
        conn.commit()
        cur.close()
        return jsonify({'message': 'Service supprimé avec succès'}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    
# Route pour la récupération d'un service proposé par un prestataire
def get_service(id):
    # Récupérer les données du service depuis la base de données
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM services WHERE id = %s", (id,))
        service = cur.fetchone()
        cur.close()
        if service:
            service_dict = {'id': service[0], 'nom': service[1], 'description': service[2]}
            return jsonify(service_dict), 200
        else:
            return jsonify({'error': 'Service non trouvé'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
