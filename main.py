from data.gerar_dados import gerar
from model.train import train_and_save
from model.evaluate import evaluate

print("🔄 Gerando base sintética...")
gerar()

print("🧠 Treinando modelo...")
train_and_save()

print("📊 Avaliando modelo...")
evaluate()

print("✅ Pipeline finalizado com sucesso.")
