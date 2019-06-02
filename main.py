from flask import Flask, jsonify, request
from pyswip import Prolog
import ManagerRecetas as recetas
import json
import psycopg2 #PostgreSQL lib
import random
import string

app = Flask(__name__)
PORT = 5000
DEBUG = True

prolog = Prolog
prolog.consult("recetas.pl")

results = []

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

#Login
@app.route('/login',methods=['POST','GET'])
def login():

	if request.method == 'POST':
        #Database connection credentials
        dbConnection = getConnection()
        username = request.json['username']
        password = request.json['password']

        cur = dbConnection.cursor()

        print('QUERY:'+"SELECT splogin FROM spLogin('"+username+"','"+password+"');")
        
        cur.execute("SELECT splogin FROM spLogin('"+username+"','"+password+"');")

        queryResponse = cur.fetchone()

        cur.close()
        
        print(queryResponse[0])
        if queryResponse[0] == True:
            print('Credenciales correctos para '+username)
            print('Generating authentication token...')
            authToken = generateToken()

            #bloque para la actualizacion del token en la base de datos despues de ser generada

            anotherCursor = dbConnection.cursor()

            print('QUERY:'+"SELECT spsetauthtoken FROM spSetAuthToken('"+username+"','"+authToken+"')")

            anotherCursor.execute("SELECT spsetauthtoken FROM spSetAuthToken('"+username+"','"+authToken+"')")


            respuestaSetAuthTokenProcedure = anotherCursor.fetchone()#variable booleano que dice si la actualizacion del token fue exitosa o no

            anotherCursor.close()
            dbConnection.commit()
            dbConnection.close()

            #fin del bloque

            if (respuestaSetAuthTokenProcedure[0] == True):
                print('spSetAuthTokenProcedure:'+str(respuestaSetAuthTokenProcedure[0]))
                return jsonify(token=authToken)
            else:
                return jsonify(token='')

        else:
            print('Credenciales incorrectos')
            dbConnection.close()
            return jsonify(token = '')
    else:
        dbConnection.close()
        return jsonify(token = '')


def generateToken():

    letters = string.ascii_lowercase

    authToken = ""

    return authToken.join(random.choice(letters) for i in range(0,10))


def getConnection():
    return psycopg2.connect(
            host = 'ec2-23-21-91-183.compute-1.amazonaws.com',
            database = 'd4p1vjd3bc3tvv',
            user = 'enagxtinofjzfe',
            password = '9503c71e6865bfb9f9d4428548a03d81d8f26eb37a8d07a1c76a45adae1ea300'
        )

@app.route('/register',methods=['POST'])
def register():
    #Database connection credentials
        dbConnection = getConnection()

        name = request.json['name']
        email = request.json['email']
        username = request.json['username']
        password = request.json['password']

        cur = dbConnection.cursor()

        inputTuple = name+"','"+email+"','"+username+"','"+password

        print("QUERY: "+"SELECT spnewuser FROM spNewUser('"+inputTuple+"')")


        cur.execute("SELECT spnewuser FROM spNewUser('"+inputTuple+"')")

        response = cur.fetchone()

        cur.close()
        dbConnection.commit()
        dbConnection.close()

        print("spNewUser: "+str(response[0]))
        if (response[0]==True):

            return jsonify(response=True)

        else:

            return jsonify(response=False)