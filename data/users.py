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

# Route pour créer un nouvel utilisateur
def create_user():
    data = request.json
    nom = data.get('nom')
    mot_de_passe = data.get('mot_de_passe')
    id_roles = data.get('id_roles')
    code_parainage = data.get('code_parainage')
    
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO utilisateurs (nom, mot_de_passe, id_roles, code_parainage) VALUES (%s, %s, %s, %s) RETURNING id", (nom, mot_de_passe, id_roles, code_parainage))
        id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        return jsonify({'id': id, 'nom': nom, 'mot_de_passe': mot_de_passe, 'id_roles': id_roles, 'code_parainage': code_parainage}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500

# Route pour la modification d'un compte utilisateur par son ID
def update_user(id):
    data = request.json
    nom = data.get('nom')

    try:
        cur = conn.cursor()
        cur.execute("UPDATE utilisateurs SET nom = %s WHERE id = %s", (nom, id))
        conn.commit()
        cur.close()
        return jsonify({'message': 'Utilisateur mis à jour avec succès'}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500

# Route pour la suppression d'un compte utilisateur par son ID
def delete_user(id):
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM utilisateurs WHERE id = %s", (id,))
        conn.commit()
        cur.close()
        return jsonify({'message': 'Utilisateur supprimé avec succès'}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500

# Route pour la récupération d'un utilisateur
def get_user(id):
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM utilisateurs WHERE id = %s", (id,))
        user = cur.fetchone()
        cur.close()
        if user:
            user_dict = {'id': user[0], 'nom': user[1]}
            return jsonify(user_dict), 200
        else:
            return jsonify({'error': 'Utilisateur non trouvé'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route pour la récupération de tous les utilisateur
def get_users():
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM utilisateurs")
        users = cur.fetchall()
        cur.close()
        user_list = [{'id': user[0], 'nom': user[1]} for user in users]
        return jsonify(user_list), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500