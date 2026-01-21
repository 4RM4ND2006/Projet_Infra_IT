from flask import Flask, render_template_string, render_template, jsonify, request, redirect, url_for, session, make_response
import sqlite3

app = Flask(__name__)                                                                                                                                                                                                                                                                                                                              
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# Fonction de vérification de session
def est_authentifie():
    return session.get('authentifie')

@app.route('/')
def hello_world():
    return render_template('hello.html')

# EXERCICE 1 & 2 : Fiche par nom + Protection Basic Auth
@app.route('/fiche_nom/<nom>')
def fiche_nom(nom):
    # --- DEBUT DU BLOC DE PROTECTION ---
    auth = request.authorization
    if not auth or auth.username != 'user' or auth.password != '12345':
        return make_response('Identifiants incorrects', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
    # --- FIN DU BLOC DE PROTECTION ---

    con = sqlite3.connect("database.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM clients WHERE nom = ?", (nom,))
    user = cur.fetchone()
    con.close()
    return render_template("affichage_client.html", user=user)

@app.route('/recherche/<titre>')
def recherche_livre(titre):
    db = sqlite3.connect("database.db")
    db.row_factory = sqlite3.Row
    livre = db.execute("SELECT * FROM livres WHERE titre LIKE ?", ('%' + titre + '%',)).fetchall()
    db.close()
    resultats = [dict(row) for row in livre]
    return {"livres_trouves": resultats}

@app.route('/lecture')
def lecture():
    if not est_authentifie():
        return redirect(url_for('authentification'))
    return "<h2>Bravo, vous êtes authentifié</h2>"

@app.route('/authentification', methods=['GET', 'POST'])
def authentification():
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == 'password':
            session['authentifie'] = True
            return redirect(url_for('lecture'))
        else:
            return render_template('formulaire_authentification.html', error=True)
    return render_template('formulaire_authentification.html', error=False)

@app.route('/fiche_client/<int:post_id>')
def Readfiche(post_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clients WHERE id = ?', (post_id,))
    data = cursor.fetchall()
    conn.close()
    return render_template('read_data.html', data=data)

@app.route('/consultation/')
def ReadBDD():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clients;')
    data = cursor.fetchall()
    conn.close()
    return render_template('read_data.html', data=data)

@app.route('/enregistrer_client', methods=['GET', 'POST'])
def enregistrer_client():
    if request.method == 'POST':
        nom = request.form['nom']
        prenom = request.form['prenom']
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO clients (created, nom, prenom, adresse) VALUES (?, ?, ?, ?)', (1002938, nom, prenom, "ICI"))
        conn.commit()
        conn.close()
        return redirect('/consultation/')
    return render_template('formulaire.html')

@app.route('/emprunter/<int:id_livre>')
def emprunter(id_livre):
    db = sqlite3.connect("database.db")
    db.execute("UPDATE livres SET disponible = 0 WHERE id = ?", (id_livre,))
    db.commit()
    db.close()
    return {"message": f"Le livre {id_livre} a été emprunté avec succès."}

@app.route('/supprimer_livre/<int:id_livre>')
def supprimer_livre(id_livre):
    db = sqlite3.connect("database.db")
    db.execute("DELETE FROM livres WHERE id = ?", (id_livre,))
    db.commit()
    db.close()
    return {"message": f"Le livre {id_livre} a été supprimé."}

@app.route('/etat_stocks')
def etat_stocks():
    db = sqlite3.connect("database.db")
    cursor = db.cursor()
    cursor.execute("SELECT COUNT(*) FROM livres WHERE disponible = 1")
    disponibles = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM livres WHERE disponible = 0")
    empruntes = cursor.fetchone()[0]
    db.close()
    return {
        "livres_disponibles": disponibles,
        "livres_empruntes": empruntes,
        "total": disponibles + empruntes
    }

if __name__ == "__main__":
    app.run(debug=True)
