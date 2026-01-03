import pandas as pd, pickle
from sklearn.metrics import accuracy_score

def evaluate():
    df=pd.read_csv("data/test.csv")
    X=df.drop("aprovado",axis=1).values
    y=df["aprovado"].values
    m=pickle.load(open("model/model.pkl","rb"))
    p=(m.proba(X)>=0.5).astype(int)
    print("Accuracy:",accuracy_score(y,p))
