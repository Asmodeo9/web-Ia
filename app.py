from flask import Flask, request, jsonify, send_file, render_template
from gtts import gTTS
import os
from groq import Groq
import io

app = Flask(__name__)

client = Groq(api_key="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")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_message', methods=['POST'])
def process_message():
    data = request.json
    user_message = data.get('message')

    if not user_message:
        return jsonify({'error': 'No message provided'}), 400

    # Generar respuesta con el modelo Groq
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "you are a helpful assistant."},
            {"role": "user", "content": user_message},
        ],
        model="llama3-70b-8192",
    )

    llm_response = chat_completion.choices[0].message.content

    # Configura el idioma a español
    language = "es"

    # Convierte el texto a voz usando gTTS
    speech = gTTS(text=str(llm_response), lang=language, slow=False)
    audio_output = io.BytesIO()
    speech.write_to_fp(audio_output)
    audio_output.seek(0)

    return send_file(audio_output, mimetype='audio/mp3', as_attachment=False, download_name='response.mp3')

if __name__ == '__main__':
    app.run(debug=True)