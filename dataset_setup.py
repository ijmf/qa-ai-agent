import os
from dotenv import load_dotenv
from langfuse import Langfuse

load_dotenv()

langfuse = Langfuse(
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    host=os.getenv("LANGFUSE_HOST")
)

DATASET_NAME = "qa-agent-evaluation"

itens = [
    {
        "input": {"pergunta": "O que é teste de regressão?"},
        "expected_output": {"deve_conter": ["regressão", "funcionalidade", "alteração"]}
    },
    {
        "input": {"pergunta": "Como escrever um cenário BDD em Gherkin?"},
        "expected_output": {"deve_conter": ["given", "when", "then", "dado", "quando", "então"]}
    },
    {
        "input": {"pergunta": "Qual a diferença entre teste funcional e não funcional?"},
        "expected_output": {"deve_conter": ["funcional", "performance", "usabilidade", "requisito"]}
    },
    {
        "input": {"pergunta": "O que é teste de carga e quando usar?"},
        "expected_output": {"deve_conter": ["carga", "usuários", "performance", "simultâneos"]}
    },
    {
        "input": {"pergunta": "Quais são os níveis de teste de software?"},
        "expected_output": {"deve_conter": ["unidade", "integração", "sistema", "aceitação"]}
    },
]

for item in itens:
    langfuse.create_dataset_item(
        dataset_name=DATASET_NAME,
        input=item["input"],
        expected_output=item["expected_output"]
    )
    print(f"Adicionado: {item['input']['pergunta']}")

print(f"\n{len(itens)} itens adicionados ao dataset '{DATASET_NAME}'")
langfuse.flush()