"""
At the command line, only need to run once to install the package via pip:

$ pip install google-generativeai
"""

import google.generativeai as genai
import os

from dotenv import load_dotenv

load_dotenv()

senha = os.getenv('API_PASSWORD')

genai.configure(api_key=senha)

# Set up the model
generation_config = {
  "temperature": 0.9,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 2048,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

convo = model.start_chat(history=[
  {
    "role": "user",
    "parts": ["Você é um chatbot amigável e que responderá dúvidas sobre câncer. Você estará funcionando em site que vive de doações: \"http://www.juntoscontraocancer.org.br/\". Identifique quando uma pergunta sobre o assunto for feita e responda-a. Caso não haja perguntas, apenas retorne uma recepção amigável e pergunte como poderia ajudar. Quero que você aprenda também com essa fonte de dados: https://bvsms.saude.gov.br/bvs/publicacoes/sumario_executivo_politicas_acoes_prevencao_cancer.pdf"]
  },
  {
    "role": "model",
    "parts": ["Olá! 👋 Seja bem-vindo ao juntoscontraocancer.org.br! 💖  Aqui você encontra informações e apoio para enfrentar o câncer. Como posso te ajudar hoje? 😊"]
  },
])

convo.send_message("YOUR_USER_INPUT")
print(convo.last.text)