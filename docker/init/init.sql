CREATE TABLE utilisateurs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(50),
    mot_de_passe VARCHAR(50),
    id_roles INT, -- Référence à l'ID du rôle de l'utilisateur
    FOREIGN KEY (id_roles) REFERENCES roles(id),
    code_parainage INT
);

CREATE TABLE services (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titre VARCHAR(100),
    description TEXT,
    id_createur INT,
    FOREIGN KEY (id_createur) REFERENCES utilisateurs(id),
    id_categorie INT,
    FOREIGN KEY (id_categorie) REFERENCES categories(id),
    prix DECIMAL(10, 2),
    images TEXT
);

CREATE TABLE categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(50),
    image VARCHAR(100)
);

CREATE TABLE notations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_user INT,
    FOREIGN KEY (id_user) REFERENCES utilisateurs(id),
    id_service INT,
    FOREIGN KEY (id_service) REFERENCES services(id),
    note INT
);

CREATE TABLE etapes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_service INT,
    id_demandeur INT,
    statut INT,
    FOREIGN KEY (id_service) REFERENCES services(id),
    FOREIGN KEY (id_demandeur) REFERENCES utilisateurs(id)
);

CREATE TABLE parrainage (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_paraineur INT,
    FOREIGN KEY (id_paraineur) REFERENCES utilisateurs(id),
    id_paraine INT,
    FOREIGN KEY (id_paraine) REFERENCES utilisateurs(id)
);

CREATE TABLE roles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom_role VARCHAR(50)
);

INSERT INTO roles (nom_role) VALUES 
    ('demandeur'),
    ('prestataire'),
    ('administrateur');