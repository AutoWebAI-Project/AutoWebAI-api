from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app, origins=["https://autowebai.netlify.app"])

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    prompt = data.get('prompt')

    if not prompt:
        return jsonify({'error': 'Prompt manquant'}), 400

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Tu es un assistant expert en amélioration de contenu web et SEO."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        result = response.choices[0].message.content.strip()
        return jsonify({'response': result})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/analyze-url', methods=['POST'])
def analyze_url():
    data = request.json
    url = data.get('url')

    if not url:
        return jsonify({'error': 'URL manquante'}), 400

    try:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

        # Extraire le contenu texte principal
        texts = soup.find_all(['p', 'h1', 'h2', 'h3', 'h4'])
        content = '\n'.join([t.get_text(strip=True) for t in texts])

        prompt = f"Voici le contenu d'un site web :\n{content}\n\nAméliore ce contenu pour le rendre plus engageant, plus clair, et optimisé pour le SEO. Propose une version modifiée mais conserve le sens."

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Tu es un assistant expert en amélioration de site web."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=700
        )

        suggestion = response.choices[0].message.content.strip()

        return jsonify({
            'original': content,
            'suggestion': suggestion,
            'options': [
                "✅ Copier le contenu",
                "📧 Recevoir par email",
                "🔧 Appliquer automatiquement (nécessite connexion au CMS)"
            ]
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run()
