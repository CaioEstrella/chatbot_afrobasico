import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
senha = os.getenv('API_PASSWORD')

# Configuração do modelo da API
genai.configure(api_key=senha)
generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]
model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

# Iniciar a conversa
convo = model.start_chat(history=[
    {
        "role": "user",
        "parts": ["Você é um chat bot para tirar dúvidas sobre o meu site de comércio de roupas e artigos. Somo a AB ('Afro Básico') em https://afrobasico.com/. Os clientes perguntarão sobre preços dos produtos e tipos de produtos que temos. Quero que você gere respostas amigáveis aos clientes tirando suas dúvidas. Sempre que possível, inclua um emoji de punho levantado no tom de pele negra, simbolizando o gesto de luta racial. Fique à vontade para incluir outros emojis com o mesmo simbolismo."]
    },
    {
        "role": "model",
        "parts": ["Olá! Na dúvida, Preto! Digite sua pergunta."]
    },
])

# Interface Streamlit
st.title("Chatbot do Afro Básico -  Na dúvida, preto! ✊🏿")
user_input = st.text_input("Digite sua pergunta aqui ✊🏿", "")
if user_input:
    convo.send_message(user_input)
    response = convo.last.text
    st.write("Resposta:", response)
