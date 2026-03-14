import os
from langchain_openai import OpenAIEmbeddings
#from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_postgres import PGVector
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import chain

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

# Realiza uma busca por similaridade no PGVector usando a pergunta fornecida,
# retornando os 10 trechos mais relevantes concatenados em uma única string de contexto.
def get_context(question: str) -> str:
    if not question:
        return "Nenhuma pergunta fornecida."

    # Embeddings
    embeddings = OpenAIEmbeddings(model=os.getenv("OPENAI_MODEL","text-embedding-3-small"))
    #embeddings = GoogleGenerativeAIEmbeddings(model=os.getenv("GOOGLE_EMBEDDING_MODEL", "gemini-embedding-001"))

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

    return contexto

# Monta o prompt final combinando o contexto recuperado e a pergunta do usuário,
# utilizando o template definido para garantir respostas baseadas apenas no contexto.
@chain
def search_prompt(input_dict: dict):
    question = input_dict.get("question")
    context = input_dict.get("context")

    if not question:
        return "Nenhuma pergunta fornecida."
    
    if not context:
        return "Nenhum contexto fornecido."

    prompt = PromptTemplate(
        input_variables=["contexto", "pergunta"],
        template=PROMPT_TEMPLATE
    )

    return prompt.invoke({"contexto": context, "pergunta": question})
