
import os

import streamlit as st
from groq import Groq
from dotenv import load_dotenv

# ==========================================
# 1. CONFIGURAÇÃO DO SITE
# ==========================================

st.set_page_config(
    page_title="Chatbot IA",
    page_icon="🤖",
    layout="centered"
)

# Carrega a chave da API
load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY")

# ==========================================
# 2. INTERFACE
# ==========================================

st.title("🤖 Chatbot IA")
st.caption("Seu assistente inteligente com tecnologia Groq")

st.divider()

# ==========================================
# 3. HISTÓRICO DA CONVERSA
# ==========================================

if "historico" not in st.session_state:
    st.session_state.historico = [
        {
            "role": "assistant",
            "content": "Olá! 👋 Sou seu assistente virtual. Como posso ajudar?"
        }
    ]

# Exibe as mensagens anteriores
for mensagem in st.session_state.historico:
    with st.chat_message(mensagem["role"]):
        st.markdown(mensagem["content"])

# ==========================================
# 4. CONEXÃO COM A GROQ
# ==========================================

if not API_KEY:
    st.error(
        "Chave da API não encontrada. "
        "Verifique se o arquivo .env existe "
        "e contém GROQ_API_KEY."
    )
    st.stop()

client = Groq(api_key=API_KEY)

# ==========================================
# 5. ENVIO E RESPOSTA DAS MENSAGENS
# ==========================================

pergunta = st.chat_input("Digite sua mensagem...")

if pergunta:
    # Guarda e exibe a mensagem do usuário
    st.session_state.historico.append(
        {
            "role": "user",
            "content": pergunta
        }
    )

    with st.chat_message("user"):
        st.markdown(pergunta)

    # Gera a resposta da inteligência artificial
    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            try:
                resposta = client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=st.session_state.historico,
                    temperature=0.7,
                    max_completion_tokens=2048
                )

                texto = resposta.choices[0].message.content

                if not texto:
                    texto = "Não consegui gerar uma resposta. Tente novamente."

                st.markdown(texto)

                # Salva a resposta no histórico
                st.session_state.historico.append(
                    {
                        "role": "assistant",
                        "content": texto
                    }
                )

            except Exception as erro:
                st.error(
                    "Não foi possível obter uma resposta da Groq. "
                    "Verifique sua conexão, sua chave de API "
                    "e a disponibilidade do modelo."
                )
                st.caption(f"Detalhes técnicos: {erro}")
