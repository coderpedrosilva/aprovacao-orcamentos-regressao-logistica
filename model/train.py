import pandas as pd, pickle
from model.logistic import Logistic

def train_and_save():
    df=pd.read_csv("data/train.csv")
    X=df.drop("aprovado",axis=1).values
    y=df["aprovado"].values
    m=Logistic(); m.fit(X,y)
    pickle.dump(m,open("model/model.pkl","wb"))
