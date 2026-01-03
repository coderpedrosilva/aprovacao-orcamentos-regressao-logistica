import pandas as pd, pickle, os
from model.logistic import Logistic

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def train_and_save():
    df = pd.read_csv(os.path.join(BASE,"data","train.csv"))

    X = df.drop("aprovado",axis=1).values
    y = df["aprovado"].values

    # Z-score normalization
    mean = X.mean(axis=0)
    std  = X.std(axis=0)

    Xn = (X - mean) / std

    model = Logistic(lr=0.05, epochs=6000)
    model.fit(Xn, y)

    pickle.dump({"model":model,"mean":mean,"std":std},
                open(os.path.join(BASE,"model","model.pkl"),"wb"))
