from flask import Flask, jsonify, request
from pyswip import Prolog
import ManagerRecetas as recetas

app = Flask(__name__)
PORT = 5000
DEBUG = True

prolog = Prolog
prolog.consult("recetas.pl")

@app.route('/', methods=['GET'])
def home():
    return '''<h3>Prueba Api Lenguajes de Programacion</h3>'''

@app.route('/api/recetas/set', methods=['GET'])
def setReceta():
    nombre = request.args['nombre']
    instrucciones = request.args['instrucciones']
    tipo = request.args['tipo']
    ingredientes = request.args['ingredientes']
    imagenes = request.args['urls']
    recetas.addReceta(nombre, tipo, instrucciones, ingredientes, imagenes, prolog)
    return jsonify(True)

@app.route('/api/recetas/all', methods=['GET'])
def getRecetas():
    results = []
    query = "receta(X,_,_,_,_)"
    resultado = list(prolog.query(query))
    for r in resultado:
        results.append(r['X'])

    return jsonify(results)

@app.route('/api/recetas', methods=['GET'])
def nombreReceta():
    results = []
    if 'nombreReceta' in request.args:
        nombreReceta = request.args['nombreReceta']
    else:
        return nombreTipo()

    nombreReceta = "'" + nombreReceta + "'"
    query = "buscarNombre(" + nombreReceta + ",X)"
    for r in prolog.query(query):
        receta = r['X']
        results.append(receta)
    return jsonify(results)

@app.route('/api/recetas', methods=['GET'])
def nombreTipo():
    results = []
    if 'nombreTipo' in request.args:
        nombreTipo = request.args['nombreTipo']
    else:
        return nombreIngrediente()

    nombreTipo = "'" + nombreTipo + "'"
    query = "buscarTipo(" + nombreTipo + ",X)"
    for r in prolog.query(query):
        receta = r['X']
        results.append(receta)
    return jsonify(results)

@app.route('/api/recetas', methods=['GET'])
def nombreIngrediente():
    results = []
    if 'nombreIngrediente' in request.args:
        nombreIngrediente = request.args['nombreIngrediente']
    else:
        return "Error: No se encuentra el tipo a buscar, especifica uno."

    nombreIngrediente = "'" + nombreIngrediente + "'"
    query = "buscarIngrediente(" + nombreIngrediente + ",X)"
    for r in prolog.query(query):
        receta = r['X']
        results.append(receta)
    return jsonify(results)
