from agent.agente import executar_agente

perguntas = [
    "O que é teste de regressão?",
    "Qual a diferença entre teste funcional e não funcional?",
    "Como escrever um cenário BDD em Gherkin?",
    "O que é um teste de carga e quando usar?",
    "Quais são os níveis de teste de software?"
]

if __name__ == "__main__":
    print("=" * 60)
    print("QA AI AGENT — Powered by Groq + LangFuse")
    print("=" * 60)

    for i, pergunta in enumerate(perguntas, 1):
        print(f"\n[{i}] Pergunta: {pergunta}")
        resultado = executar_agente(pergunta, session_id=f"session-{i}")

        if resultado["status"] == "sucesso":
            print(f"Resposta: {resultado['resposta'][:200]}...")
            print(f"Tokens usados: {resultado['tokens_usados']}")
            print(f"Modelo: {resultado['modelo']}")
        else:
            print(f"Erro: {resultado['erro']}")

        print("-" * 60)