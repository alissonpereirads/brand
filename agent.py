from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from config import llm
from dados import get_excel


def create_agent(path: str = None):
    if path:
        data = get_excel(path)  # Usa o caminho personalizado
    else:
        data = get_excel()  # Usa o caminho padrão

    print(f"Total de entradas no DataFrame: {len(data)}")  # Verificação
    agent = create_pandas_dataframe_agent(
        llm,
        data,
        verbose=True,
        agent_type="tool-calling",
        allow_dangerous_code=True,
        handle_parsing_errors=True,
    )
    return agent


def ask_agent(agent, question):
    try:
        resposta = agent.invoke(question)
        return resposta
    except Exception as e:
        return f"Erro ao processar a pergunta: {e}"
