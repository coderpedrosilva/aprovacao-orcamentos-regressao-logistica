import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, request, jsonify, send_from_directory
import numpy as np
import pickle

app = Flask(__name__, static_folder="static", static_url_path="")

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
    return app.send_static_file("index.html")


app.run(debug=True)
