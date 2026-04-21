import pandas as pd
import pickle
import os
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
)

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

THRESHOLD = 0.5

def evaluate():
    data = pickle.load(open(os.path.join(BASE, "model", "model.pkl"), "rb"))
    model, mean, std = data["model"], data["mean"], data["std"]

    df = pd.read_csv(os.path.join(BASE, "data", "test.csv"))
    X  = (df.drop("aprovado", axis=1).values - mean) / std
    y  = df["aprovado"].values

    proba = model.proba(X)
    pred  = (proba >= THRESHOLD).astype(int)

    cm = confusion_matrix(y, pred)

    print(f"{'─' * 35}")
    print(f"  Threshold : {THRESHOLD}")
    print(f"  Accuracy  : {accuracy_score(y, pred):.4f}")
    print(f"  Precision : {precision_score(y, pred):.4f}")
    print(f"  Recall    : {recall_score(y, pred):.4f}")
    print(f"  F1-Score  : {f1_score(y, pred):.4f}")
    print(f"  ROC-AUC   : {roc_auc_score(y, proba):.4f}")
    print(f"{'─' * 35}")
    print(f"  Confusion Matrix:")
    print(f"              Pred 0   Pred 1")
    print(f"  Real 0      {cm[0,0]:<7}  {cm[0,1]:<7}")
    print(f"  Real 1      {cm[1,0]:<7}  {cm[1,1]:<7}")
    print(f"{'─' * 35}")
