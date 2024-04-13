CREATE TABLE roles (
    id serial PRIMARY KEY,
    nom_role VARCHAR(50)
);

INSERT INTO roles (nom_role) VALUES 
    ('demandeur'),
    ('prestataire'),
    ('administrateur');

CREATE TABLE utilisateurs (
    id serial PRIMARY KEY,
    nom VARCHAR(50),
    mot_de_passe VARCHAR(255),
    id_roles INT REFERENCES roles(id) -- Référence à l'ID du rôle de l'utilisateur
);