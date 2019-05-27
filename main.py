from flask import Flask, jsonify, request
from pyswip import Prolog
import ManagerRecetas as recetas
import json

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
    query = "receta(X,Y,Z,W,K)"
    resultado = list(prolog.query(query))

    recipes = []
    for r in resultado:
        recipe = []
        name = {'name' : r['X'] }
        type = {'type' : r['Y'] }
        stringInstructions = ''.join(str(e) for e in r['Z'])
        stringIngredients = ''.join(str(e) for e in r['W'])
        stringImages = ''.join(str(e) for e in r['K'])

        instructions = []
        instruction = ""
        for l in stringInstructions:
            if(l == "1" or l == "2" or l == "3" or l == "4" or l == "5" or l == "6" or l == "7" or l == "8" or l == "9" ):
                if(instruction == ""):
                    instruction += l
                else:
                    instructions.append(instruction)
                    instruction = l
            else:
                instruction += l
        instructions.append(instruction)

        ingredients = []
        ingredient = ""
        for l in stringIngredients:
            if(l == l.upper()):
                if(ingredient == ""):
                    ingredient += l
                else:
                    ingredients.append(ingredient)
                    ingredient = l
            else:
                ingredient += l
        ingredients.append(ingredient)

        recipe.append(name)
        recipe.append(type)
        recipe.append({'instructions':instructions})
        recipe.append({'ingredients':ingredients})
        #recipe.append({'images':images})
        recipes.append({ 'recipe':recipe })

    results = { 'recipes' : recipes }

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
