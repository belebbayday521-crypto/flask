#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Flask, request, render_template, redirect, flash
from flask import session, g
import pymysql.cursors

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.secret_key = 'une cle(token) : grain de sel(any random string)'


def get_db():
    if 'db' not in g:
        g.db = pymysql.connect(
            host="serveurmysql.iut-bm.univ-fcomte.fr",  # localhost sur les machines perso.
            user="ybelebba",
            password="secret",
            database="BDD_ybelebba",
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
    return g.db


@app.teardown_appcontext
def teardown_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()


@app.route('/')
@app.route('/etudiant/show')
def show_etudiants():
    mycursor = get_db().cursor()

    sql = '''
          SELECT etudiant.id_etudiant  AS id
               , etudiant.nom_etudiant AS nom
               , etudiant.groupe_etudiant_id
               , groupe.libelle_groupe AS libelle
          FROM etudiant
                   INNER JOIN groupe ON groupe.id_groupe = etudiant.groupe_etudiant_id
          ORDER BY etudiant.nom_etudiant; \
          '''

    mycursor.execute(sql)

    liste_etudiants = mycursor.fetchall()

    return render_template('etudiant/show_etudiants.html', etudiants=liste_etudiants)


@app.route('/etudiant/add', methods=['GET'])
def add_etudiant():
    mycursor = get_db().cursor()

    sql = '''
          SELECT id_groupe AS id, libelle_groupe AS libelle
          FROM groupe
          ORDER BY libelle_groupe; \
          '''

    mycursor.execute(sql)

    liste_groupes = mycursor.fetchall()

    return render_template('etudiant/add_etudiant.html', groupes=liste_groupes)


@app.route('/etudiant/delete')
def delete_etudiant():
    id = request.args.get('id')

    mycursor = get_db().cursor()
    sql = "DELETE FROM etudiant WHERE id_etudiant = %s"
    mycursor.execute(sql, (id,))
    get_db().commit()

    flash("Étudiant supprimé avec succès !", "alert-danger")

    return redirect('/etudiant/show')


@app.route('/etudiant/edit', methods=['GET'])
def edit_etudiant():
    id = request.args.get('id')
    mycursor = get_db().cursor()

    sql_etudiant = "SELECT id_etudiant AS id, nom_etudiant AS nom, groupe_etudiant_id AS groupe_id FROM etudiant WHERE id_etudiant = %s"
    mycursor.execute(sql_etudiant, (id,))
    etudiant = mycursor.fetchone()

    sql_groupes = "SELECT id_groupe AS id, libelle_groupe AS libelle FROM groupe ORDER BY libelle_groupe"
    mycursor.execute(sql_groupes)
    groupes = mycursor.fetchall()

    return render_template('etudiant/edit_etudiant.html', etudiant=etudiant, groupes=groupes)


@app.route('/etudiant/add', methods=['POST'])
def valid_add_etudiant():
    nom = request.form.get('nom')
    id_groupe = request.form.get('id_groupe')

    mycursor = get_db().cursor()
    sql = "INSERT INTO etudiant (nom_etudiant, groupe_etudiant_id) VALUES (%s, %s)"
    mycursor.execute(sql, (nom, id_groupe))
    get_db().commit()

    flash("Étudiant " + str(nom) + " ajouté avec succès !", "alert-success")

    return redirect('/etudiant/show')


@app.route('/etudiant/edit', methods=['POST'])
def valid_edit_etudiant():
    id = request.form.get('id', 'None id')
    nom = request.form.get('nom', 'None nom')
    id_groupe = request.form.get('id_groupe', 'None id_groupe')

    mycursor = get_db().cursor()
    tuple_update = (nom, id_groupe, id)

    sql = ("UPDATE etudiant SET "
           "nom_etudiant=%s, groupe_etudiant_id=%s WHERE id_etudiant=%s")
    mycursor.execute(sql, tuple_update)
    get_db().commit()

    message = 'Modification du nom :' + str(nom) + ' - id_groupe :' + str(
        id_groupe) + ' pour l\'étudiant d\'identifiant :' + str(id)
    print(message)

    flash("Étudiant " + str(nom) + " modifié avec succès !", "alert-warning")

    return redirect('/etudiant/show')


if __name__ == '__main__':
    app.run(debug=True, port=5000)
