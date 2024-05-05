from flask import Flask, jsonify, request
from pymongo import MongoClient
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import certifi
import uuid
from bson import ObjectId

app = Flask(__name__)

uri  = 'mongodb+srv://jMejia2:fCn5fSLzmA07nh3H@cluster0.p0kwqwt.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'

client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client.get_database("miInventario")
collection = db.productos

# Obtener todos los productos
@app.route('/productos', methods=['GET'])
def get_productos():
    productos = list(collection.find({}, {'_id': 0}))
    return jsonify(productos)

# Obtener un producto por su ID
@app.route('/productos/<string:id>', methods=['GET'])
def get_producto(id):
    producto = collection.find_one({'id': id}, {'_id': 0})
    if producto:
        return jsonify(producto)
    return jsonify({"error": "Producto no encontrado"}), 404

# Crear un nuevo producto
@app.route('/productos', methods=['POST'])
def crear_producto():
    nuevo_producto = request.get_json()
    nuevo_producto['_id'] = str(uuid.uuid4())
    nuevo_producto['_id'] = nuevo_producto['_id']
    resultado = collection.insert_one(nuevo_producto)
    return jsonify(nuevo_producto), 201

# Actualizar un producto
@app.route('/productos/<string:id>', methods=['PUT'])
def actualizar_producto(id):
    producto_data = request.get_json()
    resultado = collection.update_one({'id': id}, {'$set': producto_data})
    if resultado.modified_count > 0:
        return jsonify(producto_data)
    return jsonify({"error": "Producto no encontrado"}), 404

# Eliminar un producto
@app.route('/productos/<string:id>', methods=['DELETE'])
def eliminar_producto(id):
    resultado = collection.delete_one({'id': id})
    if resultado.deleted_count > 0:
        return jsonify({"mensaje": "Producto eliminado"})
    return jsonify({"error": "Producto no encontrado"}), 404

if __name__ == '__main__':
    app.run(debug=True)