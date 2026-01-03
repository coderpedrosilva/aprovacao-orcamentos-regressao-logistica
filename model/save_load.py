import pickle

def load():
    return pickle.load(open("model/model.pkl","rb"))
