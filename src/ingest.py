import os
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
#from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.documents import Document
from langchain_postgres import PGVector
from dotenv import load_dotenv
load_dotenv()

PDF_PATH = os.getenv("PDF_PATH")

def ingest_pdf():
    # Carregar PDF
    docs = PyPDFLoader(PDF_PATH).load()

    # Dividir PDF em pedaços
    splitted_text = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150, add_start_index=False).split_documents(docs)

    if not splitted_text:
        print("Não foi possível dividir o PDF em pedaços.")
        exit()

    # Enriquecer chunks (limpeza e sanitização)
    enriched = [
        Document(
            # Mantém o texto do seu PDF intacto
            page_content=d.page_content,
            # Crie um novo dicionário de metadados, mas só mantenha a chave e o valor se o valor (v) não for uma string vazia ("") e não for nulo (None).
            metadata={k: v for k, v in d.metadata.items() if v not in ("", None)}
        )
        for d in splitted_text
    ]

    ids = [f"doc-{i}" for i in range(len(enriched))]

    # Criar embeddings
    embeddings = OpenAIEmbeddings(model=os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"))
    #embeddings = GoogleGenerativeAIEmbeddings(model=os.getenv("GOOGLE_EMBEDDING_MODEL", "gemini-embedding-001"))

    # Inserir no banco de dados
    vector_store = PGVector(
        collection_name=os.getenv("PG_VECTOR_COLLECTION_NAME", "pdf_chunks"),
        connection=os.getenv("DATABASE_URL"),
        embeddings=embeddings,
        use_jsonb=True
    )

    vector_store.add_documents(documents=enriched, ids=ids)

    print("Ingestão concluída com sucesso!")


if __name__ == "__main__": 
    ingest_pdf()