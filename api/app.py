from flask import Flask, request, jsonify, send_from_directory
import numpy as np
import pickle, os

app = Flask(__name__, static_folder="static")

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data = pickle.load(open(os.path.join(BASE, "model", "model.pkl"), "rb"))

model = data["model"]
mean  = data["mean"]
std   = data["std"]

@app.route("/predict", methods=["POST"])
def predict():
    d = request.json

    X = np.array([[ 
        d["valor"],
        d["prazo"],
        d["desconto"],
        d["relacionamento"],
        d["historico"]
    ]])

    X = (X - mean) / std
    prob = float(model.proba(X)[0])

    if prob >= 0.7:
        status = "Alta chance"
    elif prob >= 0.4:
        status = "Risco"
    else:
        status = "Baixa chance"

    return jsonify({
        "probabilidade": round(prob, 3),
        "status": status
    })

@app.route("/")
def index():
    return send_from_directory("static", "index.html")

app.run(debug=True)
