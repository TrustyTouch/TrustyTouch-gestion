from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required

from flask_cors import cross_origin

import hashlib
import psycopg2

# Configuration de la connexion à la base de données
conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="postgres",
    host="host.docker.internal",
    port="5432"
)

# Route pour créer un nouvel utilisateur
@cross_origin()
def create_user():
    data = request.json
    nom = data.get('nom')
    hashed_password = data.get('mot_de_passe')
    id_roles = data.get('id_roles')
    code_parainage = data.get('code_parainage')
    
    try:
        cur = conn.cursor()
        hashed_password = hashlib.sha256(data['mot_de_passe'].encode('utf-8')).hexdigest()
        cur.execute("INSERT INTO utilisateurs (nom, mot_de_passe, id_roles, code_parainage) VALUES (%s, %s, %s, %s) RETURNING id", (nom, hashed_password, id_roles, code_parainage))
        id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        
        return jsonify({'id': id, 'nom': nom, 'id_roles': id_roles, 'code_parainage': code_parainage}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500

# Route pour la modification d'un compte utilisateur par son ID
@jwt_required()
@cross_origin()
def update_user(id):
    data = request.json
    nom = data.get('nom')
    biographie = data.get('biographie')

    try:
        cur = conn.cursor()
        cur.execute("UPDATE utilisateurs SET nom = %s, biographie = %s WHERE id = %s", (nom, biographie, id))
        conn.commit()
        cur.close()
        return jsonify({'message': 'Utilisateur mis à jour avec succès'}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500

# Route pour la suppression d'un compte utilisateur par son ID
@jwt_required()
@cross_origin()
def delete_user(id):
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM services s WHERE s.id_createur = %s", (id,))
        cur.execute("DELETE FROM utilisateurs WHERE id = %s", (id,))
        conn.commit()
        cur.close()
        return jsonify({'message': 'Utilisateur supprimé avec succès'}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500

# Route pour la récupération d'un utilisateur
@jwt_required()
@cross_origin()
def get_user(id):
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM utilisateurs WHERE id = %s", (id,))
        user = cur.fetchone()
        cur.close()
        if user:
            id, nom, _, roles, code, biographie = user
            user_dict = {'id': id, 'nom': nom, 'id_roles': roles, 'code_parainage': code, 'biographie': biographie }
            return jsonify(user_dict), 200
        else:
            return jsonify({'error': 'Utilisateur non trouvé'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route pour la récupération de tous les utilisateur
@jwt_required()
@cross_origin()
def get_users():
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM utilisateurs")
        users = cur.fetchall()
        cur.close()
        user_list = [{'id': id, 'nom': nom, 'id_roles': roles, 'code_parainage': code} for id, nom, _, roles, code, _ in users]
        return jsonify(user_list), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500