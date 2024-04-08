FROM python:3.12.2

# Définition du répertoire de travail dans le conteneur
WORKDIR /app

# Copie du fichier des dépendances et installation de ces dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie de l'ensemble de l'application dans le conteneur
COPY . .

# Affichage du contenu du répertoire pour vérifier la structure des fichiers
RUN ls -la

# Configuration des variables d'environnement nécessaires
ENV PYTHONPATH "${PYTHONPATH}:/app"
ENV FLASK_APP src/app.py

# Exposition du port sur lequel l'application s'exécute
EXPOSE 5000

# Commande pour démarrer l'application
CMD ["flask", "run", "--host=0.0.0.0"]