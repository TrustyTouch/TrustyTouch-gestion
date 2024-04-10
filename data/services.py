from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required

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
@jwt_required()
def create_service():
    # Récupérer les données du service à partir de la requête JSON
    data = request.json
    titre = data.get('titre')
    description = data.get('description')
    id_createur = data.get('id_createur')
    id_categorie = data.get('id_categorie')
    prix = data.get('prix')
    images = data.get('images')

    # Créer un nouvel enregistrement de service dans la base de données
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO services (titre, description, id_createur, id_categorie, prix, images) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id", (titre, description, id_createur, id_categorie, prix, images))
        id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        return jsonify({'id': id, 'titre': titre, 'description': description, 'id_createur': id_createur, 'id_categorie': id_categorie, 'prix': prix, 'images': images}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500

# Route pour la modification d'un service proposé par un prestataire par l'ID
@jwt_required()
def update_service(id):
    # Récupérer les données mises à jour du service à partir de la requête JSON
    data = request.json
    titre = data.get('titre')
    description = data.get('description')
    id_categorie = data.get('id_categorie')
    prix = data.get('prix')
    images = data.get('images')

    # Mettre à jour l'enregistrement de service dans la base de données
    try:
        cur = conn.cursor()
        cur.execute("UPDATE services SET titre = %s, description = %s, id_categorie = %s, prix = %s, images = %s WHERE id = %s",
                    (titre, description, id_categorie, prix, images, id))
        conn.commit()
        cur.close()
        return jsonify({'message': 'Service mis à jour avec succès'}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500


# Route pour la suppression d'un service proposé par un prestataire par l'ID
@jwt_required()
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
    
# Route pour la récupération d'un service proposé par un prestataire en fonction de son titre
@jwt_required()
def get_service(titre):
    # Récupérer les données du service depuis la base de données
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM services WHERE titre = %s", (titre,))
        service = cur.fetchone()
        cur.close()
        if service:
            service_dict = {'id': service[0], 'titre': service[1], 'description': service[2]}
            return jsonify(service_dict), 200
        else:
            return jsonify({'error': 'Service non trouvé'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route pour la récupération d'un service proposé par un prestataire en fonction de sa catégorie
@jwt_required()
def get_services(id_categorie):
    # Récupérer les données du service depuis la base de données
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM services WHERE id_categorie = %s", (id_categorie,))
        service = cur.fetchone()
        cur.close()
        if service:
            service_dict = {'id': service[0], 'titre': service[1], 'id_categorie': service[4]}
            return jsonify(service_dict), 200
        else:
            return jsonify({'error': 'Service non trouvé'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500