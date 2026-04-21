import pickle
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load():
    return pickle.load(open(os.path.join(BASE, "model", "model.pkl"), "rb"))
