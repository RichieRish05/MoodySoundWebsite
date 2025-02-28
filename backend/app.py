from flask import Flask, jsonify
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

@app.get('/hello')
def hello():
    return jsonify({'message': 'Hello, world!'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
