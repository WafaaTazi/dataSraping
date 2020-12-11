import sqlite3

try:
    sqliteConnection = sqlite3.connect('pfa.db')
    sqlite_create_table_query = '''CREATE TABLE Test (
                                Date VARCHAR(10),
                                Code_Isin VARCHAR(10),
                                Instrument VARCHAR(10),
                                Nombre_de_titres VARCHAR(10),
                                Cours VARCHAR(10),
                                Facteur_flottant VARCHAR(10),
                                Facteur_de_plafonnement VARCHAR(10),
                                Capitalisation_flottante VARCHAR(10),
                                Poids VARCHAR(10)
                                );'''

    cursor = sqliteConnection.cursor()
    print("Successfully Connected to SQLite")
    cursor.execute(sqlite_create_table_query)
    sqliteConnection.commit()
    print("SQLite table created")

    cursor.close()

except sqlite3.Error as error:
    print("Error while creating a sqlite table", error)
finally:
    if (sqliteConnection):
        sqliteConnection.close()
        print("sqlite connection is closed")

