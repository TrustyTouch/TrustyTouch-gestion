from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required

from flask_cors import cross_origin

from . import db

# Route pour créer une nouvelle étape
@jwt_required()
@cross_origin()
def create_etape():
    conn = db.getconn()
    data = request.json
    id_service = data.get('id_service')
    id_demandeur = data.get('id_demandeur')
    statut = data.get('statut')
    
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO etapes (statut, id_service, id_demandeur) VALUES (%s, %s, %s) RETURNING id", (statut, id_service, id_demandeur))
        id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        return jsonify({'id': id, 'statut': statut, 'id_service': id_service, 'id_demandeur': id_demandeur}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500

# Route pour la modification d'une étape en fonction de l'ID du service
@jwt_required()
@cross_origin()
def update_etape(id):
    conn = db.getconn()
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
@cross_origin()
def delete_etape(id):
    conn = db.getconn()
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
@cross_origin()
def get_etape(id_demandeur):
    conn = db.getconn()
    try:
        cur = conn.cursor()
        cur.execute("SELECT e.id, e.id_service, u.id, e.statut, s.titre, u.nom FROM etapes e JOIN services s ON (e.id_service = s.id) JOIN utilisateurs u ON (s.id_createur = u.id) WHERE u.id = %s", (id_demandeur,))
        etapes = cur.fetchall()
        cur.close()
        etape_list = [{'id': id, 'id_service': id_service, 'id_demandeur': id_demandeur, 'statut': statut, 'titre': titre, 'nom': nom} for id, id_service, id_demandeur, statut, titre, nom in etapes]
        return jsonify(etape_list), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
