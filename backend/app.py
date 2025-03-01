from flask import Flask, jsonify
from flask_cors import CORS
import torch
from services import load_model

app = Flask(__name__)
CORS(app)


# Init the model
model = load_model()

@app.get('/hello')
def hello():
    return jsonify({'message': 'Hello, world!'})


@app.get('/mood')
def predict_mood():
    with torch.no_grad():
        pass



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
