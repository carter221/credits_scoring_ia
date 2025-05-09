from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "API de Scoring Crédit Home Credit - Status: En ligne (mode test)"

@app.route('/predict', methods=['POST'])
def predict():
    return jsonify({
        'result': 'good'
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5007, debug=True)
