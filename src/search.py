import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import chain


load_dotenv()

PROMPT_TEMPLATE = """
CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""

@chain
def search_prompt(input_dict: dict):
    question = input_dict.get("question")

    if not question:
        return "Nenhuma pergunta fornecida."

    # Embeddings
    embeddings = OpenAIEmbeddings(model=os.getenv("OPENAI_MODEL","text-embedding-3-small"))

    # Buscar no banco de dados
    vector_store = PGVector(
        collection_name=os.getenv("PG_VECTOR_COLLECTION_NAME", "pdf_chunks"),
        connection=os.getenv("DATABASE_URL"),
        embeddings=embeddings,
        use_jsonb=True
    )

    # Get results
    results = vector_store.similarity_search_with_score(question, k=10)

    # Contexto
    contexto = ""
    for (result, score) in results:
        contexto += result.page_content.strip() + "\n\n"

    question_template = PromptTemplate(
        input_variables=["contexto", "pergunta"],
        template=PROMPT_TEMPLATE
    )

    prompt = question_template.invoke({"contexto": contexto, "pergunta": question})
    
    return prompt