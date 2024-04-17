from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from datetime import timedelta 

from flask_cors import cross_origin

import hashlib

from . import db

@jwt_required()
@cross_origin()
def get_nb_user():
    conn = db.getconn()

    try:
        cur = conn.cursor()
        cur.execute("SELECT COUNT(id) FROM utilisateurs")
        count = cur.fetchone()
        cur.close()
        return jsonify({"nb_utilisateurs": count}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@jwt_required()
@cross_origin()
def get_nb_presta():
    conn_auth = db.getconn_auth()

    try:
        cur = conn_auth.cursor()
        cur.execute("SELECT COUNT(id) FROM utilisateurs WHERE id_roles=2")
        count = cur.fetchone()
        cur.close()
        return jsonify({"nb_prestataires": count}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route pour créer un nouvel utilisateur
@cross_origin()
def create_user():
    conn_auth = db.getconn_auth()
    conn = db.getconn()
    data = request.json
    nom = data.get('nom')
    email = data.get('email')
    hashed_password = hashlib.sha256(data.get('mot_de_passe').encode('utf-8')).hexdigest()
    id_roles = data.get('id_roles')
    code_parainage = data.get('code_parainage')
    
    try:
        # Vérifier si l'e-mail existe déjà dans la base de données
        cur = conn_auth.cursor()
        cur.execute("SELECT email FROM utilisateurs WHERE email = %s", (email,))
        existing_email = cur.fetchone()
        cur.close()
        if existing_email:
            return jsonify({'message': 'L\'adresse e-mail existe déjà'}), 400

        # Insérer l'utilisateur dans la base de données des utilisateurs authentifiés
        cur = conn_auth.cursor()
        cur.execute("INSERT INTO utilisateurs (email, mot_de_passe, id_roles) VALUES (%s, %s, %s) RETURNING id", (email, hashed_password, id_roles))
        id = cur.fetchone()[0]
        conn_auth.commit()
        cur.close()
        
        # Insérer l'utilisateur dans la base de données principale
        cur = conn.cursor()
        cur.execute("INSERT INTO utilisateurs (id, nom, code_parainage) VALUES (%s, %s, %s)", (id, nom, code_parainage))
        conn.commit()
        cur.close()

        return jsonify({'id': id, 'nom': nom, 'code_parainage': code_parainage}), 201

    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500

# Route pour la modification d'un compte utilisateur par son ID
@jwt_required()
@cross_origin()
def update_user(id):
    conn = db.getconn()
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
    conn_auth = db.getconn_auth()
    conn = db.getconn()
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM services s WHERE s.id_createur = %s", (id,))
        cur.execute("DELETE FROM utilisateurs WHERE id = %s", (id,))
        conn.commit()
        cur.close()

        cur = conn_auth.cursor()
        cur.execute("DELETE FROM utilisateurs WHERE id = %s", (id,))
        conn_auth.commit()
        cur.close()
        
        return jsonify({'message': 'Utilisateur supprimé avec succès'}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500

# Route pour la récupération d'un utilisateur
@jwt_required()
@cross_origin()
def get_user(id):
    conn = db.getconn()
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM utilisateurs WHERE id = %s", (id,))
        user = cur.fetchone()
        cur.close()
        
        if user:
            id, nom, code, biographie = user
            user_dict = {'id': id, 'nom': nom, 'code_parainage': code, 'biographie': biographie }
            return jsonify(user_dict), 200
        else:
            return jsonify({'error': 'Utilisateur non trouvé'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route pour la récupération de tous les utilisateur
@jwt_required()
@cross_origin()
def get_users():
    conn = db.getconn()
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM utilisateurs")
        users = cur.fetchall()
        cur.close()
        user_list = [{'id': id, 'nom': nom, 'code_parainage': code} for id, nom, code, _ in users]
        return jsonify(user_list), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

# Route pour la connexion d'un utilisateur
@cross_origin()
def login():
    conn_auth = db.getconn_auth()
    data = request.get_json()
    email = data.get('email')
    mot_de_passe = data.get('mot_de_passe')

    cur = conn_auth.cursor()
    cur.execute("SELECT id, mot_de_passe, id_roles FROM utilisateurs WHERE email = %s", (email,))
    utilisateur = cur.fetchone()
    cur.close()
    
    if utilisateur:
        id, mdp, roles = utilisateur

        # Calculer le hachage SHA-256 du mot de passe fourni
        mdp_input = hashlib.sha256(mot_de_passe.encode('utf-8')).hexdigest()

        # Comparer les hachages
        if mdp == mdp_input:
            # Générer un jeton d'accès JWT valide pour cet utilisateur
            access_token = create_access_token(identity=id, expires_delta=timedelta(hours=4), additional_claims={"id_role": roles})
            return jsonify({'message': 'Connexion réussie', 'access_token': access_token}), 200
        else:
            return jsonify({'message': 'Nom d\'utilisateur ou mot de passe incorrect'}), 401
    else:
        return jsonify({'message': 'Nom d\'utilisateur ou mot de passe incorrect'}), 401