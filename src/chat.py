from search import search_prompt
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

def main():
    
    question = input("Faça sua pergunta: \n\nPERGUNTA: ")

    prompt = search_prompt.invoke({"question": question})

    model = ChatOpenAI(model="gpt-5-mini", temperature=0.1)

    response = model.invoke(prompt)

    print("RESPOSTA: ", response.content)

    # if not chain:
    #     print("Não foi possível iniciar o chat. Verifique os erros de inicialização.")
    #     return
    
    pass

if __name__ == "__main__":
    main()