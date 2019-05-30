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

@app.route('/api/recetas', methods=['POST'])
def setReceta():
    receta = request.json['recipe']
    nombre = receta[0]
    tipo = receta[1]
    instrucciones = receta[2]
    ingredientes = receta[3]
    imagenes = receta[4]
    recetas.addReceta(nombre, tipo, instrucciones, ingredientes, imagenes, prolog)
    prolog.consult("recetas.pl")
    return jsonify(True)

@app.route('/api/recetas/all', methods=['GET'])
def getRecetas():
    results = []
    query = "receta(X,Y,Z,W,K)"
    resultado = list(prolog.query(query))

    recipes = []
    for r in resultado:
        name = r['X']
        type = r['Y']
        stringInstructions = ''.join(str(e) for e in r['Z'])
        stringIngredients = ''.join(str(e) for e in r['W'])
        stringImages = ''.join(str(e) for e in r['K'])

        ingredients = []
        ingredient = ""
        for l in stringIngredients:
            if(l == "|"):
                if(ingredient != ""):
                    ingredients.append(ingredient)
                    ingredient = ""
            else:
                ingredient += l
        ingredients.append(ingredient)

        images = []
        url = ""
        for l in stringImages:
            if(l == "|"):
                if(url != ""):
                    images.append(url)
                    url = ""
            else:
                url += l
        images.append(url)

        recipe = {  'name': name,
                    'type': type,
                    'preparation': stringInstructions,
                    'ingredients': ingredients,
                    'URLs': images }

        recipes.append(recipe)

    return jsonify({ 'recipes': recipes })

@app.route('/api/recetas', methods=['GET'])
def nombreReceta():
    result = []
    if 'nombreReceta' in request.args:
        nombreReceta = request.args['nombreReceta']
    else:
        return nombreTipo()

    nombreReceta = "'" + nombreReceta + "'"
    query = "buscarNombre(" + nombreReceta + ",X)"
    for r in prolog.query(query):
        nombre = r['X']

    auxQuery = "receta('" + nombre + "',Y,Z,W,K)"
    for r in prolog.query(auxQuery):
        name = nombre
        type = r['Y']
        stringInstructions = ''.join(str(e) for e in r['Z'])
        stringIngredients = ''.join(str(e) for e in r['W'])
        stringImages = ''.join(str(e) for e in r['K'])

        ingredients = []
        ingredient = ""
        for l in stringIngredients:
            if(l == "|"):
                if(ingredient != ""):
                    ingredients.append(ingredient)
                    ingredient = ""
            else:
                ingredient += l
        ingredients.append(ingredient)

        images = []
        url = ""
        for l in stringImages:
            if(l == "|"):
                if(url != ""):
                    images.append(url)
                    url = ""
            else:
                url += l
        images.append(url)

        recipe = {  'name': name,
                    'type': type,
                    'preparation': stringInstructions,
                    'ingredients': ingredients,
                    'URLs': images }
    result.append(recipe)

    return jsonify({ 'recipes': result })

@app.route('/api/recetas', methods=['GET'])
def nombreTipo():
    results = []
    if 'nombreTipo' in request.args:
        nombreTipo = request.args['nombreTipo']
    else:
        return nombreIngrediente()

    nombreTipo = "'" + nombreTipo + "'"
    query = "buscarTipo(" + nombreTipo + ",X)"
    listaNombres = []
    for r in prolog.query(query):
         listaNombres.append(r['X'])

    for nombre in listaNombres:
        auxQuery = "receta('" + nombre + "',Y,Z,W,K)"
        for r in prolog.query(auxQuery):
            name = nombre
            type = r['Y']
            stringInstructions = ''.join(str(e) for e in r['Z'])
            stringIngredients = ''.join(str(e) for e in r['W'])
            stringImages = ''.join(str(e) for e in r['K'])

            ingredients = []
            ingredient = ""
            for l in stringIngredients:
                if(l == "|"):
                    if(ingredient != ""):
                        ingredients.append(ingredient)
                        ingredient = ""
                else:
                    ingredient += l
            ingredients.append(ingredient)

            images = []
            url = ""
            for l in stringImages:
                if(l == "|"):
                    if(url != ""):
                        images.append(url)
                        url = ""
                else:
                    url += l
            images.append(url)

            recipe = {  'name': name,
                        'type': type,
                        'preparation': stringInstructions,
                        'ingredients': ingredients,
                        'URLs': images }

            results.append(recipe)

    return jsonify({ 'recipes': results })

@app.route('/api/recetas', methods=['GET'])
def nombreIngrediente():
    results = []
    if 'nombreIngrediente' in request.args:
        nombreIngrediente = request.args['nombreIngrediente']
    else:
        return "Error: No se encuentra el tipo a buscar, especifica uno."

    nombreIngrediente = "'|" + nombreIngrediente + "'"
    query = "buscarIngrediente(" + nombreIngrediente + ",X)"
    listaNombres = []
    for r in prolog.query(query):
        listaNombres.append(r['X'])

    for nombre in listaNombres:
        auxQuery = "receta('" + nombre + "',Y,Z,W,K)"
        for r in prolog.query(auxQuery):
            name = nombre
            type = r['Y']
            stringInstructions = ''.join(str(e) for e in r['Z'])
            stringIngredients = ''.join(str(e) for e in r['W'])
            stringImages = ''.join(str(e) for e in r['K'])

            ingredients = []
            ingredient = ""
            for l in stringIngredients:
                if(l == "|"):
                    if(ingredient != ""):
                        ingredients.append(ingredient)
                        ingredient = ""
                else:
                    ingredient += l
            ingredients.append(ingredient)

            images = []
            url = ""
            for l in stringImages:
                if(l == "|"):
                    if(url != ""):
                        images.append(url)
                        url = ""
                else:
                    url += l
            images.append(url)

            recipe = {  'name': name,
                        'type': type,
                        'preparation': stringInstructions,
                        'ingredients': ingredients,
                        'URLs': images }

            results.append(recipe)

    return jsonify({ 'recipes': results })
