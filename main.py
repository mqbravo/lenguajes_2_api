from flask import Flask, jsonify, request
from pyswip import Prolog
import ManagerRecetas as recetas

app = Flask(__name__)
PORT = 5000
DEBUG = True

prolog = Prolog
prolog.consult("recetas.pl")

results = []

@app.route('/', methods=['GET'])
def home():
    return '''<h3>Prueba Api Lenguajes de Programacion</h3>'''

#@app.route('/api/recetas/set', methods=['POST'])
#def setReceta():
#    return jsonify(results)

@app.route('/api/recetas/all', methods=['GET'])
def getRecetas():
    query = "receta(X)"
    resultado = list(prolog.query(query))
    for r in resultado:
        results.append(r['X'])

    return jsonify(results)

@app.route('/api/recetas', methods=['GET'])
def nombreReceta():
    nombreReceta = request.args['nombreReceta']
    nombreReceta = "'" + nombreReceta + "'"
    query = "buscarNombre(" + nombreReceta + ",X)"
    for r in prolog.query(query):
        receta = r['X']
        results.append(receta)
    return jsonify(results)


#recetas.addReceta(nombreReceta, prolog)


if __name__ == '__main__':
    app.run(port = PORT, debug = DEBUG)
