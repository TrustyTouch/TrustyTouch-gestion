import sys
import secrets
from signal import signal, SIGTERM

from flask_cors import CORS, cross_origin
from time import sleep

from flask import Flask
from flask_jwt_extended import JWTManager

from data.services import create_service, update_service, delete_service, get_service, get_services, get_my_services, get_nb_services
from data.users import create_user, update_user, delete_user, get_users, get_user, login, get_nb_user, get_nb_presta
from data.etapes import create_etape, update_etape, delete_etape, get_etape

app = Flask(__name__)
cors = CORS(app)

# Générer une clé JWT secrète aléatoire
jwt_secret_key = secrets.token_urlsafe(32)

# Configuration de la clé secrète pour JWT
app.config['JWT_SECRET_KEY'] = jwt_secret_key
jwt = JWTManager(app)

app.add_url_rule('/login', view_func=login, methods=['POST'])

app.add_url_rule('/create_user', view_func=create_user, methods=['POST'])

app.add_url_rule('/update_user/<id>', view_func=update_user, methods=['PUT'])

app.add_url_rule('/delete_user/<id>', view_func=delete_user, methods=['DELETE'])

app.add_url_rule('/get_users', view_func=get_users, methods=['GET'])

app.add_url_rule('/get_user/<id>', view_func=get_user, methods=['GET'])

app.add_url_rule('/create_service', view_func=create_service, methods=['POST'])

app.add_url_rule('/update_service/<id>', view_func=update_service, methods=['PUT'])

app.add_url_rule('/delete_service/<id>', view_func=delete_service, methods=['DELETE'])

app.add_url_rule('/get_service/<id>', view_func=get_service, methods=['GET'])

app.add_url_rule('/get_services/<id_categorie>', view_func=get_services, methods=['GET'])

app.add_url_rule('/get_my_services', view_func=get_my_services, methods=['GET'])

app.add_url_rule('/create_etape', view_func=create_etape, methods=['POST'])

app.add_url_rule('/update_etape/<id>', view_func=update_etape, methods=['PUT'])

app.add_url_rule('/delete_etape/<id>', view_func=delete_etape, methods=['DELETE'])

app.add_url_rule('/get_etape/<id_demandeur>', view_func=get_etape, methods=['GET'])

app.add_url_rule('/get_nb_user', view_func=get_nb_user, methods=['GET'])

app.add_url_rule('/get_nb_presta', view_func=get_nb_presta, methods=['GET'])

app.add_url_rule('/get_nb_services', view_func=get_nb_services, methods=['GET'])

def handle_signal(*args, **kwargs):
    sys.exit(0)
signal(SIGTERM, handle_signal)

if __name__ == '__main__':
    sleep(1)
    app.run(debug=True)
    
