import pytest
import os
from unittest.mock import patch, MagicMock
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

    def test_resposta_regressao_menciona_conceito(self):
        resultado = executar_agente("O que é teste de regressão?")
        assert resultado["status"] == "sucesso"
        palavras_chave = ["regressão", "regress", "alteração", "funcionalidade", "existente"]
        resposta_lower = resultado["resposta"].lower()
        assert any(p in resposta_lower for p in palavras_chave)

    def test_resposta_gherkin_menciona_estrutura(self):
        resultado = executar_agente("Como escrever um cenário BDD em Gherkin?")
        assert resultado["status"] == "sucesso"
        palavras_chave = ["given", "when", "then", "dado", "quando", "então", "cenário"]
        resposta_lower = resultado["resposta"].lower()
        assert any(p in resposta_lower for p in palavras_chave)

    def test_resposta_nao_muito_curta(self):
        resultado = executar_agente("O que é teste de carga?")
        assert resultado["status"] == "sucesso"
        assert len(resultado["resposta"]) > 100

    def test_tempo_de_resposta(self):
        import time
        inicio = time.time()
        resultado = executar_agente("O que é teste de unidade?")
        duracao = time.time() - inicio
        assert resultado["status"] == "sucesso"
        assert duracao < 15

    def test_falha_api_retorna_status_falha(self):
        with patch("agent.agente.groq_client") as mock_client:
            mock_client.chat.completions.create.side_effect = Exception("API indisponível")
            resultado = executar_agente("O que é teste de regressão?")
            assert resultado["status"] == "falha"
            assert resultado["resposta"] is None
            assert "API indisponível" in resultado["erro"]

    def test_falha_api_nao_levanta_excecao(self):
        with patch("agent.agente.groq_client") as mock_client:
            mock_client.chat.completions.create.side_effect = Exception("Timeout")
            try:
                resultado = executar_agente("O que é BDD?")
                assert resultado["status"] == "falha"
            except Exception:
                pytest.fail("O agente não deveria levantar exceção")

    def test_mock_resposta_controlada(self):
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "Teste de regressão valida funcionalidades existentes."
        mock_response.usage.total_tokens = 42

        with patch("agent.agente.groq_client") as mock_client:
            mock_client.chat.completions.create.return_value = mock_response
            resultado = executar_agente("O que é teste de regressão?")
            assert resultado["status"] == "sucesso"
            assert resultado["tokens_usados"] == 42
            assert "regressão" in resultado["resposta"].lower()