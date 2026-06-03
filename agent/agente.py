import os
from dotenv import load_dotenv
from groq import Groq
from langfuse import observe, Langfuse

load_dotenv()

os.environ["LANGFUSE_PUBLIC_KEY"] = os.getenv("LANGFUSE_PUBLIC_KEY")
os.environ["LANGFUSE_SECRET_KEY"] = os.getenv("LANGFUSE_SECRET_KEY")
os.environ["LANGFUSE_HOST"] = os.getenv("LANGFUSE_HOST")

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """Você é um assistente de QA especializado em testes de software.
Responda perguntas sobre: tipos de teste, boas práticas, ferramentas de QA,
critérios de aceite, Gherkin/BDD e automação de testes.
Seja direto e objetivo. Responda sempre em português."""

@observe()
def executar_agente(pergunta: str, session_id: str = "default") -> dict:
    try:
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": pergunta}
            ],
            max_tokens=500,
            temperature=0.3
        )

        resposta = response.choices[0].message.content
        tokens_usados = response.usage.total_tokens

        return {
            "resposta": resposta,
            "tokens_usados": tokens_usados,
            "modelo": "llama-3.3-70b-versatile",
            "status": "sucesso"
        }

    except Exception as e:
        return {
            "resposta": None,
            "erro": str(e),
            "status": "falha"
        }