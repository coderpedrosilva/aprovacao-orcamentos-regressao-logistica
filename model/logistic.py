import numpy as np

class Logistic:
    def __init__(self, lr=0.001, epochs=5000):
        self.lr=lr; self.epochs=epochs

    def sig(self,z): return 1/(1+np.exp(-z))

    def fit(self,X,y):
        self.w=np.zeros(X.shape[1]); self.b=0
        for _ in range(self.epochs):
            p=self.sig(X@self.w+self.b)
            self.w-=self.lr*(X.T@(p-y))/len(y)
            self.b-=self.lr*(p-y).mean()

    def proba(self,X): return self.sig(X@self.w+self.b)
