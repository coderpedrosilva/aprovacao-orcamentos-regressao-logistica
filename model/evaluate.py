import pandas as pd, pickle, os
from sklearn.metrics import accuracy_score, confusion_matrix

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def evaluate():
    data = pickle.load(open(os.path.join(BASE,"model","model.pkl"),"rb"))
    model,mean,std = data["model"],data["mean"],data["std"]

    df = pd.read_csv(os.path.join(BASE,"data","test.csv"))
    X = (df.drop("aprovado",axis=1).values - mean) / std
    y = df["aprovado"].values

    pred = (model.proba(X)>=0.5).astype(int)

    print("Accuracy:", accuracy_score(y,pred))
    print("Confusion matrix:\n", confusion_matrix(y,pred))
