from search import search_prompt, get_context
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

def main():
    
    question = input("Faça sua pergunta: \n\nPERGUNTA: ")

    if not question:
        print("Nenhuma pergunta fornecida. Encerrando.")
        return

    context = get_context(question)

    model = ChatOpenAI(model="gpt-5-mini", temperature=0.1)

    chain = search_prompt | model

    if not chain:
        print("Não foi possível iniciar o chat. Verifique os erros de inicialização.")
        return
    
    response = chain.invoke({"question": question, "context": context})
    
    print("RESPOSTA: ", response.content)
    

if __name__ == "__main__":
    main()