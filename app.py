from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

@app.route('/', methods=['POST'])
def traduzir_codigo():
    OPENAI_API_KEY = "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"
    link = "https://api.openai.com/v1/chat/completions"
    id_modelo = "gpt-3.5-turbo"

    body_mensagem = {
        "model": id_modelo,
        "messages": [{"role": "user", "content": request.form['codigo_original']}]
    }

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    body_mensagem = json.dumps(body_mensagem)

    requisicao = requests.post(link, headers=headers, data=body_mensagem)
    resposta = requisicao.json()
    mensagem = resposta["choices"][0]["message"]["content"]

    return jsonify({"traducao": mensagem})

if __name__ == '__main__':
    app.run()
