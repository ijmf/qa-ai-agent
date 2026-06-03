# qa-ai-agent

Agente de IA especializado em QA, com observabilidade via LangFuse, testes automatizados com pytest e pipeline CI/CD via GitHub Actions.

## O que é

Um agente que responde perguntas sobre testes de software usando um LLM (Llama 3.3 via Groq), com cada interação rastreada no LangFuse — input, output, tokens e latência. Os testes automatizados validam o comportamento do agente, incluindo mocks para falha de API, validação de conteúdo e tempo de resposta. Um dataset de avaliação fixo permite medir a qualidade do agente a cada atualização.

## Stack

- Python 3.13
- Groq API — inferência com Llama 3.3 70B
- LangFuse — observabilidade, rastreamento de traces e LLM-as-a-Judge
- pytest + pytest-mock — testes automatizados do agente
- GitHub Actions — pipeline CI/CD

## Estrutura

```
qa-ai-agent/
├── .github/
│   └── workflows/
│       └── tests.yml       # Pipeline CI/CD com GitHub Actions
├── agent/
│   └── agente.py           # Lógica do agente + integração LangFuse
├── tests/
│   └── test_agent.py       # 12 casos de teste com pytest
├── app.py                  # Execução das perguntas
├── dataset_setup.py        # Cria o dataset de avaliação no LangFuse
├── dataset_run.py          # Roda o agente contra o dataset e calcula scores
├── .env.example            # Variáveis de ambiente necessárias
└── requirements.txt        # Dependências do projeto
```

## Como executar

```bash
# Criar ambiente virtual
python -m venv venv
venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt

# Configurar variáveis de ambiente
cp .env.example .env
# Preencher .env com suas chaves

# Rodar o agente
python app.py

# Rodar os testes
pytest tests/test_agent.py -v

# Criar dataset de avaliação no LangFuse
python dataset_setup.py

# Rodar avaliação contra o dataset
python dataset_run.py
```

## Variáveis de ambiente

```
GROQ_API_KEY=sua_chave_groq
LANGFUSE_PUBLIC_KEY=sua_chave_publica
LANGFUSE_SECRET_KEY=sua_chave_secreta
LANGFUSE_HOST=http://localhost:3000
```

## Casos de teste

| Teste | O que valida |
|---|---|
| test_resposta_nao_vazia | Agente retorna resposta com mais de 50 caracteres |
| test_tokens_registrados | Tokens são contabilizados corretamente |
| test_modelo_correto | Modelo correto está sendo usado |
| test_resposta_em_portugues | Resposta contém palavras em português |
| test_pergunta_fora_do_escopo | Agente responde mesmo fora do domínio |
| test_resposta_regressao_menciona_conceito | Valida conteúdo da resposta sobre regressão |
| test_resposta_gherkin_menciona_estrutura | Valida que Given/When/Then aparecem na resposta |
| test_resposta_nao_muito_curta | Resposta tem mais de 100 caracteres |
| test_tempo_de_resposta | Resposta chega em menos de 15 segundos |
| test_falha_api_retorna_status_falha | Falha da API retorna status correto sem exception |
| test_falha_api_nao_levanta_excecao | Agente não quebra quando API falha |
| test_mock_resposta_controlada | Valida comportamento com resposta mockada |

## Observabilidade

Cada chamada ao agente gera um trace no LangFuse com input, output, tokens usados e latência. O evaluator **LLM-as-a-Judge Hallucination** avalia automaticamente cada resposta com score de 0 a 1. O LangFuse roda localmente via Docker.

## Dataset de avaliação

O dataset `qa-agent-evaluation` contém 5 perguntas fixas com palavras-chave esperadas. A cada run, o agente é avaliado contra esse dataset e um score médio é calculado — equivalente a um suite de regressão para sistemas de IA.

**Resultado da run-v1:** score médio de 0.78