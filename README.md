# qa-ai-agent

Agente de IA especializado em QA, com observabilidade via LangFuse e testes automatizados com pytest.

## O que é

Um agente que responde perguntas sobre testes de software usando um LLM (Llama 3.3 via Groq), com cada interação rastreada no LangFuse — input, output, tokens e latência. Os testes automatizados validam o comportamento do agente com pytest.

## Stack

- Python 3.13
- Groq API — inferência com Llama 3.3 70B
- LangFuse — observabilidade e rastreamento de traces
- pytest — testes automatizados do agente

## Estrutura

qa-ai-agent/
├── agent/
│   └── agente.py       # Lógica do agente + integração LangFuse
├── tests/
│   └── test_agent.py   # Casos de teste com pytest
├── app.py              # Execução das perguntas
├── .env.example        # Variáveis de ambiente necessárias
└── requirements.txt    # Dependências do projeto

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
```

## Variáveis de ambiente

GROQ_API_KEY=sua_chave_groq
LANGFUSE_PUBLIC_KEY=sua_chave_publica
LANGFUSE_SECRET_KEY=sua_chave_secreta
LANGFUSE_HOST=http://localhost:3000

## Casos de teste

| Teste | O que valida |
|---|---|
| test_resposta_nao_vazia | Agente retorna resposta com mais de 50 caracteres |
| test_tokens_registrados | Tokens são contabilizados corretamente |
| test_modelo_correto | Modelo correto está sendo usado |
| test_resposta_em_portugues | Resposta contém palavras em português |
| test_pergunta_fora_do_escopo | Agente responde mesmo fora do domínio |

## Observabilidade

Cada chamada ao agente gera um trace no LangFuse com input, output, tokens usados e latência. O LangFuse roda localmente via Docker.

Depois cria o .env.example e o requirements.txt:

New-Item .env.example
pip freeze > requirements.txt

Abre o .env.example e cola:

GROQ_API_KEY=
LANGFUSE_PUBLIC_KEY=
LANGFUSE_SECRET_KEY=
LANGFUSE_HOST=http://localhost:3000
