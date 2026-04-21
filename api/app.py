import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, request, jsonify
import numpy as np
import pickle

app = Flask(__name__, static_folder="static", static_url_path="")

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_data = pickle.load(open(os.path.join(BASE, "model", "model.pkl"), "rb"))
model = _data["model"]
mean  = _data["mean"]
std   = _data["std"]

THRESHOLD_HIGH = 0.7
THRESHOLD_LOW  = 0.4

FEATURE_BOUNDS = {
    "valor":          (300,  8000),
    "prazo":          (7,    60),
    "desconto":       (0,    20),
    "relacionamento": (1,    5),
    "historico":      (0,    20),
}

def _validate(d):
    errors = []
    for field, (lo, hi) in FEATURE_BOUNDS.items():
        if field not in d:
            errors.append(f"Campo ausente: '{field}'")
            continue
        try:
            v = float(d[field])
        except (TypeError, ValueError):
            errors.append(f"'{field}' deve ser numérico")
            continue
        if not (lo <= v <= hi):
            errors.append(f"'{field}' deve estar entre {lo} e {hi} (recebido: {v})")
    return errors


@app.route("/predict", methods=["POST"])
def predict():
    d = request.get_json(silent=True)
    if d is None:
        return jsonify({"erro": "JSON inválido ou ausente"}), 400

    errors = _validate(d)
    if errors:
        return jsonify({"erro": errors}), 422

    X = np.array([[
        float(d["valor"]),
        float(d["prazo"]),
        float(d["desconto"]),
        float(d["relacionamento"]),
        float(d["historico"]),
    ]])
    X    = (X - mean) / std
    prob = float(model.proba(X)[0])

    if prob >= THRESHOLD_HIGH:
        status = "Alta chance"
    elif prob >= THRESHOLD_LOW:
        status = "Risco"
    else:
        status = "Baixa chance"

    return jsonify({"probabilidade": round(prob, 3), "status": status})


@app.route("/", methods=["GET"])
def index():
    return app.send_static_file("index.html")


if __name__ == "__main__":
    debug = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    app.run(debug=debug)
