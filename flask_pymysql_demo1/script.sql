
DROP TABLE IF EXISTS etudiant;
DROP TABLE IF EXISTS groupe;

CREATE TABLE groupe (
id_groupe INT AUTO_INCREMENT
, libelle_groupe VARCHAR(255)
, PRIMARY KEY(id_groupe)
);

CREATE TABLE etudiant (
id_etudiant INT AUTO_INCREMENT
, nom_etudiant VARCHAR(255)
, groupe_etudiant_id INT
, PRIMARY KEY(id_etudiant)
, FOREIGN KEY (groupe_etudiant_id) REFERENCES groupe(id_groupe)
);



INSERT INTO groupe (id_groupe, libelle_groupe)
VALUES
(NULL, 'A1'),
(NULL, 'A2'),
(NULL, 'B1'),
(NULL, 'B2'),
(NULL, 'C1'),
(NULL, 'C2')
;
INSERT INTO etudiant (id_etudiant, nom_etudiant, groupe_etudiant_id)
VALUES
(NULL, 'tom',1),
(NULL, 'enzo',1),
(NULL, 'laurence',2),
(NULL, 'theo',2),
(NULL, 'mehdi',3)
;


-- afficher les étudiants et le libellé de leur groupe
SELECT etudiant.id_etudiant AS id
     , etudiant.nom_etudiant AS nom
     , etudiant.groupe_etudiant_id
     , groupe.libelle_groupe AS libelle
FROM etudiant
INNER JOIN groupe ON groupe.id_groupe = etudiant.groupe_etudiant_id
ORDER BY etudiant.nom_etudiant;

-- afficher les groupes
SELECT id_groupe AS id, libelle_groupe AS libelle
FROM groupe
ORDER BY libelle_groupe;


-- selectionner un étudiant bien précis
SELECT etudiant.id_etudiant AS id
     , etudiant.nom_etudiant AS nom
     , etudiant.groupe_etudiant_id AS groupe_id
FROM etudiant
WHERE id_etudiant = 1;

-- ajouter un étudiant
INSERT INTO etudiant(id_etudiant, nom_etudiant, groupe_etudiant_id) VALUES (NULL, 'test1', 1);

-- supprimer un étudiant
DELETE FROM etudiant WHERE id_etudiant=2;

-- modifier un étudiant
UPDATE etudiant SET nom_etudiant = 'test2', groupe_etudiant_id = 3 WHERE id_etudiant=3;

-- nombre d'étudiants par groupe
SELECT groupe.libelle_groupe AS libelle
     , COUNT(etudiant.id_etudiant) AS nbre_etudiants
FROM groupe
LEFT JOIN etudiant ON etudiant.groupe_etudiant_id = groupe.id_groupe
GROUP BY groupe.id_groupe, groupe.libelle_groupe
ORDER BY groupe.libelle_groupe;