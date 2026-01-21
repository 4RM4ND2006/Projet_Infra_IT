import sqlite3

connection = sqlite3.connect('database.db')
cursor = connection.cursor()

# On supprime l'ancienne table si elle existe pour repartir de zéro
cursor.execute("DROP TABLE IF EXISTS livres")

# Ta commande SQL pour créer la table
cursor.execute("""
CREATE TABLE livres (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titre TEXT NOT NULL,
    auteur TEXT NOT NULL,
    disponible INTEGER DEFAULT 1
)
""")

# Optionnel : Ajoute quelques livres de test pour voir si ça marche
cursor.execute("INSERT INTO livres (titre, auteur, disponible) VALUES (?, ?, ?)", ('Le Petit Prince', 'Antoine de Saint-Exupéry', 1))
cursor.execute("INSERT INTO livres (titre, auteur, disponible) VALUES (?, ?, ?)", ('1984', 'George Orwell', 1))

connection.commit()
connection.close()
print("Base de données bibliothèque initialisée !")
