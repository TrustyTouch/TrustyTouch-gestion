from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

import psycopg2

from data import users, services

# Configuration de la connexion à la base de données
conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="postgres",
    host="localhost",
    port="5432"
)

# Route pour créer un nouvel utilisateur
def create_user():
    data = request.json
    nom = data.get('nom')
    
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO utilisateurs (nom) VALUES (%s) RETURNING id", (nom))
        user_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        return jsonify({'id': user_id, 'nom': nom}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500

# Route pour la modification d'un compte utilisateur par son ID
def update_user(user_id):
    data = request.json
    nom = data.get('nom')

    try:
        cur = conn.cursor()
        cur.execute("UPDATE utilisateurs SET nom = %s WHERE id = %s", (nom, user_id))
        conn.commit()
        cur.close()
        return jsonify({'message': 'Utilisateur mis à jour avec succès'}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500

# Route pour la suppression d'un compte utilisateur par son ID
def delete_user(user_id):
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM utilisateurs WHERE id = %s", (user_id,))
        conn.commit()
        cur.close()
        return jsonify({'message': 'Utilisateur supprimé avec succès'}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500

# Route pour la récupération d'un utilisateur
def get_user(user_id):
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM utilisateurs WHERE id = %s", (user_id,))
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