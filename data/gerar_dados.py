import numpy as np
import pandas as pd
import os

SEED = 42
BASE = os.path.dirname(os.path.abspath(__file__))

def gerar():
    rng = np.random.default_rng(SEED)
    n = 5000

    valor          = rng.uniform(300, 8000, n)
    prazo          = rng.integers(7,  61,   n)
    desconto       = rng.integers(0,  21,   n)
    relacionamento = rng.integers(1,  6,    n)
    historico      = rng.integers(0,  21,   n)

    score = (
        (valor < 3000).astype(int)         +
        (prazo > 20).astype(int)           +
        (desconto < 10).astype(int)        +
        (relacionamento >= 3).astype(int)  +
        (historico >= 5).astype(int)
    )
    aprovado = (score >= 3).astype(int)

    # ~10% de ruído para simular incerteza do mundo real
    noise_mask = rng.random(n) < 0.10
    aprovado[noise_mask] = 1 - aprovado[noise_mask]

    df = pd.DataFrame({
        "valor":          valor,
        "prazo":          prazo,
        "desconto":       desconto,
        "relacionamento": relacionamento,
        "historico":      historico,
        "aprovado":       aprovado,
    })

    train = df.sample(frac=0.8, random_state=SEED)
    test  = df.drop(train.index)

    train.to_csv(os.path.join(BASE, "train.csv"), index=False)
    test.to_csv(os.path.join(BASE, "test.csv"),  index=False)
