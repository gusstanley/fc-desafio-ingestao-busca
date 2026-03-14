from search import search_prompt, get_context
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

def main():
    
    # Solicita ao usuario que faca uma pergunta.
    question = input("Faça sua pergunta: \n\nPERGUNTA: ")

    if not question:
        print("Nenhuma pergunta fornecida. Encerrando.")
        return

    # Recupera o contexto relevante a partir da busca por similaridade no banco vetorial.
    context = get_context(question)

    model = ChatOpenAI(model="gpt-5-mini", temperature=0.1)

    # Monta o chain combinando o prompt de busca e o modelo de linguagem.
    chain = search_prompt | model

    if not chain:
        print("Não foi possível iniciar o chat. Verifique os erros de inicialização.")
        return
    
    # Invoca o chain passando a pergunta e o contexto para impressao da resposta gerada.
    response = chain.invoke({"question": question, "context": context})
    
    print("RESPOSTA: ", response.content)


if __name__ == "__main__":
    main()