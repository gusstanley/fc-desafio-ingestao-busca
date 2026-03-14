# Desafio MBA Engenharia de Software com IA - Full Cycle

Aplicação RAG (Retrieval-Augmented Generation) que ingere documentos PDF no PGVector e permite fazer perguntas sobre o conteúdo via chat.

## Pré-requisitos

- Python 3.13
- Docker e Docker Compose

## Setup

1. Suba o banco de dados PostgreSQL com PGVector:

```bash
docker compose up -d
```

2. Configure as variáveis de ambiente:

```bash
cp .env.example .env
```

Preencha as chaves de API no arquivo `.env` (`OPENAI_API_KEY`).

3. Crie o ambiente virtual e instale as dependências:

```bash
make setup
```

## Ingestão de dados

Coloque o arquivo PDF na raiz do projeto (ou ajuste o `PDF_PATH` no `.env`) e execute:

```bash
make ingest
```

Isso irá processar o PDF, gerar embeddings e armazená-los no PGVector.

## Chat

Para fazer perguntas sobre o conteúdo do documento:

```bash
make chat
```

Digite sua pergunta e a aplicação retornará uma resposta baseada no contexto do documento.
