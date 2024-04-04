CREATE TABLE utilisateurs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(50),
    mot_de_passe VARCHAR(50)
);

CREATE TABLE services (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titre VARCHAR(100),
    date_publication DATE
)