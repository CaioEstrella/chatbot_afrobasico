from flask import Flask, request, render_template_string
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
senha = os.getenv('API_PASSWORD')

app = Flask(__name__)

# Configure o modelo da API
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

# Iniciar conversa
convo = model.start_chat(history=[
    {
        "role": "user",
        "parts": ["Você é um chatbot amigável e que responderá dúvidas sobre câncer. Você estará funcionando em site que vive de doações: \"http://www.juntoscontraocancer.org.br/\". Identifique quando uma pergunta sobre o assunto for feita e responda-a. Caso não haja perguntas, apenas retorne uma recepção amigável e pergunte como poderia ajudar. Quero que você aprenda também com o pdf localizado em'https://bvsms.saude.gov.br/bvs/publicacoes/sumario_executivo_politicas_acoes_prevencao_cancer.pdf' e que gere respostas mais elaboradas a partir dele."]
    },
    {
        "role": "model",
        "parts": ["Olá! 👋 Seja bem-vindo ao juntoscontraocancer.org.br! 💖 Aqui você encontra informações e apoio para enfrentar o câncer. Como posso te ajudar hoje? 😊"]
    },
])

# Definição da rota da página principal
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        user_input = request.form['user_input']
        convo.send_message(user_input)
        response = convo.last.text
        return render_template_string(HOME_HTML, user_input=user_input, response=response)
    return render_template_string(HOME_HTML)

HOME_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Chatbot de Apoio</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background-color: #f9f9f9;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .container {
            width: 100%;
            max-width: 600px;
            background-color: white;
            padding: 20px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            border-radius: 8px;
            text-align: center;
        }
        h1 {
            color: #4A90E2;
        }
        input[type="text"] {
            width: 80%;
            padding: 10px;
            margin-top: 20px;
            border: 2px solid #ccc;
            border-radius: 4px;
        }
        button {
            padding: 10px 20px;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            margin-top: 10px;
        }
        button:hover {
            background-color: #45a049;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Chatbot para Apoio sobre Câncer 💖</h1>
        <form method="post">
            <input type="text" name="user_input" placeholder="Digite sua pergunta aqui 🤔" autocomplete="off">
            <button type="submit">Enviar</button>
        </form>
        {% if user_input %}
            <h2>Sua Pergunta:</h2>
            <p>{{ user_input }}</p>
            <h2>Resposta:</h2>
            <p>{{ response }}</p>
        {% endif %}
    </div>
</body>
</html>
"""

if __name__ == '__main__':
    app.run(debug=True)
