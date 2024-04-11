from datetime import timedelta 
from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

from flask_cors import cross_origin

import secrets
import psycopg2
import hashlib

# Configuration de la connexion à la base de données
conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="postgres",
    host="host.docker.internal",
    port="5432"
)

app = Flask(__name__)

# Générer une clé JWT secrète aléatoire
jwt_secret_key = secrets.token_urlsafe(32)

# Configuration de la clé secrète pour JWT
app.config['JWT_SECRET_KEY'] = jwt_secret_key
jwt = JWTManager(app)

# Route pour la connexion d'un utilisateur
@cross_origin()
def login():  
    data = request.get_json()
    nom = data.get('nom')
    mot_de_passe = data.get('mot_de_passe')

    cur = conn.cursor()
    cur.execute("SELECT * FROM utilisateurs WHERE nom = %s", (nom,))
    utilisateur = cur.fetchone()
    cur.close()

    if utilisateur:
        # Récupérer le hachage du mot de passe depuis la base de données
        id, nom, mdp, roles, code = utilisateur

        # Calculer le hachage SHA-256 du mot de passe fourni
        mdp_input = hashlib.sha256(mot_de_passe.encode('utf-8')).hexdigest()

        # Comparer les hachages
        if mdp == mdp_input:
            # Générer un jeton d'accès JWT valide pour cet utilisateur
            access_token = create_access_token(identity=nom, expires_delta=timedelta(hours=4))        
            user_dict = {'id': id, 'nom': nom, 'id_roles': roles, 'code_parainage': code}
            return jsonify({'message': 'Connexion réussie', 'access_token': access_token, 'user': user_dict}), 200
        else:
            return jsonify({'message': 'Nom d\'utilisateur ou mot de passe incorrect'}), 401
    else:
        return jsonify({'message': 'Nom d\'utilisateur ou mot de passe incorrect'}), 401

if __name__ == '__main__':
    app.run(debug=True)
