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

# Route pour créer une nouvelle étape
@jwt_required()
def create_etape():
    data = request.json
    id_service = data.get('id_service')
    id_demandeur = data.get('id_demandeur')
    statut = data.get('statut')
    
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO etapes (statut, id_service, id_demandeur) VALUES (%s, %s, %s) RETURNING id", (statut, id_service, id_demandeur))
        conn.commit()
        cur.close()
        return jsonify({'id': id, 'statut': statut, 'id_service': id_service, 'id_demandeur': id_demandeur}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500

# Route pour la modification d'une étape en fonction de l'ID du service
@jwt_required()
def update_etape(id):
    data = request.json
    id_demandeur = data.get('id_demandeur')
    statut = data.get('statut')

    try:
        cur = conn.cursor()
        cur.execute("UPDATE etapes SET statut = %s, id_demandeur = %s WHERE id = %s", (statut, id_demandeur, id))
        conn.commit()
        cur.close()
        return jsonify({'message': 'Etape mise à jour avec succès'}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500

# Route pour la suppression d'une étape en fonction de l'ID du service
@jwt_required()
def delete_etape(id):
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM etapes WHERE id = %s", (id,))
        conn.commit()
        cur.close()
        return jsonify({'message': 'Etape supprimée avec succès'}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500

# Route pour la récupération d'une étape en fonction de l'ID du service
@jwt_required()
def get_etape(id):
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM etapes WHERE id = %s", (id,))
        etape = cur.fetchone()
        cur.close()
        if etape:
            etape_dict = {'id': etape[0], 'id_service': etape[1], 'id_demandeur': etape[2], 'statut': etape[3]}
            return jsonify(etape_dict), 200
        else:
            return jsonify({'error': 'Etape non trouvée'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500