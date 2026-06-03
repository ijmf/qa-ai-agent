import os
from dotenv import load_dotenv
from langfuse import Langfuse
from agent.agente import executar_agente

load_dotenv()

langfuse = Langfuse(
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    host=os.getenv("LANGFUSE_HOST")
)

DATASET_NAME = "qa-agent-evaluation"
RUN_NAME = "run-v1"

dataset = langfuse.get_dataset(DATASET_NAME)

print(f"Rodando dataset '{DATASET_NAME}' com {len(dataset.items)} itens...\n")

resultados = []

for item in dataset.items:
    pergunta = item.input["pergunta"]
    esperado = item.expected_output["deve_conter"]

    resultado = executar_agente(pergunta, session_id=f"dataset-{item.id}")

    if resultado["status"] == "sucesso":
        resposta_lower = resultado["resposta"].lower()
        palavras_encontradas = [p for p in esperado if p in resposta_lower]
        score = len(palavras_encontradas) / len(esperado)
    else:
        palavras_encontradas = []
        score = 0.0

    resultados.append({
        "pergunta": pergunta,
        "score": score,
        "palavras_encontradas": palavras_encontradas,
        "total_esperado": len(esperado),
        "status": resultado["status"]
    })

    print(f"Pergunta: {pergunta}")
    print(f"Score: {score:.2f} ({len(palavras_encontradas)}/{len(esperado)} palavras-chave encontradas)")
    print("-" * 50)

langfuse.flush()

media = sum(r["score"] for r in resultados) / len(resultados)
print(f"\nScore médio do run '{RUN_NAME}': {media:.2f}")
print(f"Run concluída — {len(resultados)} itens avaliados.")