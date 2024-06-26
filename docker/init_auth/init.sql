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
    email TEXT,
    mot_de_passe VARCHAR(255),
    id_roles INT REFERENCES roles(id), -- Référence à l'ID du rôle de l'utilisateur
    date_crea DATE DEFAULT CURRENT_DATE
);