from flask import Flask, jsonify, request

app = Flask(__name__)
PORT = 5000
DEBUG = False


@app.route('/', methods=['GET'])
def test():
    return jsonify({'message' : 'It works!'})

if __name__ == '__main__':
    app.run(port = PORT, debug = DEBUG)
