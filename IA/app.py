from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from groq import Groq
import os

app = Flask(__name__)
CORS(app)  # Habilita CORS para que puedas hacer peticiones desde el navegador

# Inicializa el cliente Groq
API_KEY = os.getenv("GROQ_API_KEY", "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")  # Cambia esto si quieres usar variable de entorno
client = Groq(api_key=API_KEY)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message", "")
    completion = client.chat.completions.create(
        model="qwen/qwen3-32b",
        messages=[
            {"role": "system", "content": "Responde únicamente en español, de forma natural y directa, sin razonamientos ni bloques <think>. Solo la respuesta final al usuario."},
            {"role": "user", "content": user_input}
        ],
        temperature=0.6,
        max_completion_tokens=4096,
        top_p=0.95,
        reasoning_effort="default",
        stream=False,
        stop=None,
    )
    reply = completion.choices[0].message.content
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)
