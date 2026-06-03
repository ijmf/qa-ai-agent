import pytest
from agent.agente import executar_agente

class TestQAAgent:

    def test_resposta_nao_vazia(self):
        resultado = executar_agente("O que é teste de regressão?")
        assert resultado["status"] == "sucesso"
        assert resultado["resposta"] is not None
        assert len(resultado["resposta"]) > 50

    def test_tokens_registrados(self):
        resultado = executar_agente("O que é BDD?")
        assert resultado["status"] == "sucesso"
        assert resultado["tokens_usados"] > 0

    def test_modelo_correto(self):
        resultado = executar_agente("O que é teste de carga?")
        assert resultado["modelo"] == "llama-3.3-70b-versatile"

    def test_resposta_em_portugues(self):
        resultado = executar_agente("O que é teste de unidade?")
        assert resultado["status"] == "sucesso"
        palavras_pt = ["teste", "software", "sistema", "código", "função"]
        resposta_lower = resultado["resposta"].lower()
        assert any(p in resposta_lower for p in palavras_pt)

    def test_pergunta_fora_do_escopo(self):
        resultado = executar_agente("Qual é a capital da França?")
        assert resultado["status"] == "sucesso"
        assert resultado["resposta"] is not None