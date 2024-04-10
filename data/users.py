from flask import Flask, jsonify, request

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
        return jsonify({'id': id, 'nom': nom, 'mot_de_passe': hashed_password, 'id_roles': id_roles, 'code_parainage': code_parainage}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500

# Route pour la modification d'un compte utilisateur par son ID
def update_user(id):
    data = request.json
    nom = data.get('nom')
    id_roles = data.get('id_roles')
    code_parainage = data.get('code_parainage')

    try:
        cur = conn.cursor()
        cur.execute("UPDATE utilisateurs SET nom = %s, id_roles = %s, code_parainage = %s WHERE id = %s", (nom, id_roles, code_parainage, id))
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
            user_dict = {'id': user[0], 'nom': user[1], 'mot_de_passe': user[2], 'id_roles': user[3], 'code_parainage': user[4]}
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
        user_list = [{'id': user[0], 'nom': user[1], 'mot_de_passe': user[2], 'id_roles': user[3], 'code_parainage': user[4]} for user in users]
        return jsonify(user_list), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500