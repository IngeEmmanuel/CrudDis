from pymongo import MongoClient
import certifi

MONGO_URI = 'mongodb+srv://emmanuelduran:1hrl6yKWPY618xRk@cruddis.wymoipj.mongodb.net/?retryWrites=true&w=majority&appName=CrudDis'
ca = certifi.where()

def dbConnection():
    try:
        client = MongoClient(MONGO_URI, tlsCAFile=ca)
        db = client["dbb_products_app"]
    except ConnectionError:
        print('Error de conexión con la bdd')
    return db
