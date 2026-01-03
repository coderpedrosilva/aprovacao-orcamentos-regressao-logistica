from flask import Flask,request,jsonify,send_from_directory
from model.save_load import load
import numpy as np

app=Flask(__name__,static_folder="static")
model=load()

@app.route("/predict",methods=["POST"])
def predict():
    d=request.json
    X=np.array([[d["valor"],d["prazo"],d["desconto"],d["relacionamento"],d["historico"]]])
    p=float(model.proba(X)[0])
    return jsonify({"probabilidade":round(p,3)})

@app.route("/")
def home():
    return send_from_directory("static","index.html")

app.run(debug=True)
