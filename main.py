import streamlit as st
from agent import create_agent, ask_agent
import os

# Configuração da página
st.set_page_config(page_title="Analisador de Dados em Excel", page_icon="📊")

# Título da aplicação
st.title("Brand Analisador de Dados em Excel 📊")

# Descrição
st.write(
    """
Esta aplicação permite que você faça perguntas sobre seus dados em Excel e obtenha respostas instantâneas.
Carregue seu arquivo Excel e comece a explorar!
"""
)


# Função para excluir o arquivo temporário, se existir
def limpar_arquivo_temporario():
    if os.path.exists("temp_file.xlsx"):
        os.remove("temp_file.xlsx")
        print("Arquivo temporário excluído.")


# Limpa o arquivo temporário ao iniciar a aplicação
limpar_arquivo_temporario()

# Upload do arquivo Excel
uploaded_file = st.file_uploader("Carregue seu arquivo Excel", type=["xlsx"])
st.markdown("---")

# Inicializa a lista de perguntas e respostas na sessão do Streamlit
if "historico" not in st.session_state:
    st.session_state.historico = []

if uploaded_file is not None:
    # Exclui o arquivo temporário anterior, se existir
    limpar_arquivo_temporario()

    # Salva o arquivo carregado temporariamente
    with open("temp_file.xlsx", "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Cria ou recria o agente com o novo arquivo carregado
    st.session_state.agent = create_agent(path="temp_file.xlsx")

    # Exibe o histórico de perguntas e respostas usando st.chat_message
    if len(st.session_state.historico) > 0:
        st.write("### Histórico de Perguntas e Respostas")
        for i, item in enumerate(st.session_state.historico):
            # Exibe o número da pergunta
            st.markdown(f"**{i+1}ª Pergunta**")

            # Exibe a pergunta do usuário
            with st.chat_message("user"):
                st.markdown(f"**Pergunta:** {item['pergunta']}")

            # Exibe a resposta do agente
            with st.chat_message("assistant"):
                st.markdown(f"**Resposta:** {item['resposta']}")

            st.markdown("---")  # Linha divisória entre itens

        # Botão para limpar o histórico (só aparece se houver histórico)
        if st.button("Limpar Histórico"):
            st.session_state.historico = []
            st.rerun()

    # Campo de entrada para perguntas usando st.chat_input
    if prompt := st.chat_input("Faça uma pergunta sobre os dados:"):
        # Obtém a resposta do agente
        resposta = ask_agent(st.session_state.agent, prompt)

        # Verifica se a resposta é um dicionário e extrai o valor correto
        if isinstance(resposta, dict) and "output" in resposta:
            resposta_formatada = resposta["output"]
        else:
            resposta_formatada = str(resposta)  # Converte a resposta para string

        # Adiciona a pergunta e a resposta ao histórico
        st.session_state.historico.append(
            {"pergunta": prompt, "resposta": resposta_formatada}
        )

        # Força a atualização da interface com a função correta
        st.rerun()
else:
    st.warning("Por favor, carregue um arquivo Excel para começar.")
