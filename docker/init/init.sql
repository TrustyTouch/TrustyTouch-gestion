CREATE TABLE roles (
    id serial PRIMARY KEY,
    nom_role VARCHAR(50)
);

INSERT INTO roles (nom_role) VALUES 
    ('demandeur'),
    ('prestataire'),
    ('administrateur');

CREATE TABLE categories (
    id serial PRIMARY KEY,
    nom VARCHAR(50),
    image VARCHAR(100)
);

INSERT INTO categories (nom) VALUES 
    ('Electricien'),
    ('Vidéos'),
    ('Travaux publics'),
    ('Divertissement'),
    ('Immobilier'),
    ('Santé'),
    ('Agricole'),
    ('Nettoyage');

CREATE TABLE utilisateurs (
    id serial PRIMARY KEY,
    nom VARCHAR(50),
    mot_de_passe VARCHAR(255),
    id_roles INT REFERENCES roles(id), -- Référence à l'ID du rôle de l'utilisateur
    code_parainage INT,
    biographie TEXT NOT NULL DEFAULT ''
);

CREATE TABLE services (
    id serial PRIMARY KEY,
    titre VARCHAR(100),
    description TEXT,
    id_createur INT,
    FOREIGN KEY (id_createur) REFERENCES utilisateurs(id),
    id_categorie INT,
    FOREIGN KEY (id_categorie) REFERENCES categories(id),
    prix DECIMAL(10, 2),
    images TEXT
);

CREATE TABLE notations (
    id serial PRIMARY KEY,
    id_user INT,
    FOREIGN KEY (id_user) REFERENCES utilisateurs(id),
    id_service INT,
    FOREIGN KEY (id_service) REFERENCES services(id),
    note INT
);

CREATE TABLE etapes (
    id serial PRIMARY KEY,
    id_service INT,
    id_demandeur INT,
    statut INT,
    FOREIGN KEY (id_service) REFERENCES services(id),
    FOREIGN KEY (id_demandeur) REFERENCES utilisateurs(id)
);

CREATE TABLE parrainage (
    id serial PRIMARY KEY,
    id_paraineur INT,
    FOREIGN KEY (id_paraineur) REFERENCES utilisateurs(id),
    id_paraine INT,
    FOREIGN KEY (id_paraine) REFERENCES utilisateurs(id)
);