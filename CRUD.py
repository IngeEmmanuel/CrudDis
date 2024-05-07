from flask import Flask, jsonify, request
from pymongo import MongoClient
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import uuid
import os
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()

caPath = os.environ['MONGO_PEM']
print(caPath)
uri  = "mongodb+srv://cluster0.p0kwqwt.mongodb.net/?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(uri,
                     tls=True,
                     tlsCertificateKeyFile=caPath,
                     server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client.get_database("miInventario")
collection = db.productos
doc_count = collection.count_documents({})
print(doc_count)

# Obtener todos los productos
@app.route('/allProductos', methods=['GET'])
def get_productos():
    productos = list(collection.find({}, {'_id': 0}))
    return jsonify(productos)

# Obtener un producto por su nombre
@app.route('/producto', methods=['GET'])
def get_producto_por_nombre():
    nombre = request.args.get('nombre')
    if nombre:
        producto = collection.find_one({'nombre': nombre}, {'_id': 0})
        if producto:
            return jsonify(producto)
        return jsonify({"error": "Producto no encontrado"}), 404
    return jsonify({"error": "Se requiere un nombre de producto"}), 400

# Crear un nuevo producto
@app.route('/newProducto', methods=['POST'])
def crear_producto():
    nuevo_producto = request.get_json()
    nuevo_producto['_id'] = str(uuid.uuid4())
    nuevo_producto['_id'] = nuevo_producto['_id']
    resultado = collection.insert_one(nuevo_producto)
    return jsonify(nuevo_producto), 201

# Actualizar un producto
@app.route('/editProducto/<string:nombre>', methods=['PUT'])
def actualizar_producto(nombre):
    producto_data = request.get_json()
    print(producto_data)
    resultado = collection.update_one({'nombre': nombre}, {'$set': producto_data})
    if resultado.modified_count > 0:
        return jsonify(producto_data)
    return jsonify({"error": "Producto no encontrado"}), 404

# Eliminar un producto
@app.route('/deleteProducto/<string:nombre>', methods=['DELETE'])
def eliminar_producto(nombre):
    resultado = collection.delete_one({'nombre': nombre})
    if resultado.deleted_count > 0:
        return jsonify({"mensaje": f"El producto {nombre} ha sido eliminado"})
    return jsonify({"error": "Producto no encontrado"}), 404

if __name__ == '__main__':
    app.run(debug=True)