import random, pandas as pd

def gerar():
    rows=[]
    for _ in range(5000):
        valor=random.uniform(300,8000)
        prazo=random.randint(7,60)
        desconto=random.randint(0,20)
        relacionamento=random.randint(1,5)
        historico=random.randint(0,20)
        score = (valor<3000)+(prazo>20)+(desconto<10)+(relacionamento>=3)+(historico>=5)
        aprovado=1 if score>=3 else 0
        rows.append([valor,prazo,desconto,relacionamento,historico,aprovado])

    df=pd.DataFrame(rows,columns=["valor","prazo","desconto","relacionamento","historico","aprovado"])
    df.sample(frac=0.8).to_csv("data/train.csv",index=False)
    df.drop(df.sample(frac=0.8).index).to_csv("data/test.csv",index=False)

gerar()
