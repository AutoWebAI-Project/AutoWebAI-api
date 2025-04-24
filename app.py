from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app, origins=["https://autowebai.netlify.app"])

# Connexion client OpenAI avec la clé d'API
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route('/analyze-url', methods=['POST'])
def analyze_url():
    data = request.json
    url = data.get('url')
    cms = data.get('cms', 'auto')  # CMS envoyé depuis le frontend (ou "auto")

    if not url:
        return jsonify({'error': 'URL manquante'}), 400

    try:
        # 🎯 Ajoute une ligne d'intro selon le CMS choisi (MVP)
        if cms == "wordpress":
            content = "[WordPress détecté]\n"
        elif cms == "shopify":
            content = "[Shopify détecté]\n"
        elif cms == "wix":
            content = "[Wix détecté]\n"
        elif cms == "webflow":
            content = "[Webflow détecté]\n"
        else:
            content = ""

        # 🕷️ Scraping générique du contenu HTML
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

        texts = soup.find_all(['p', 'h1', 'h2', 'h3', 'h4'])
        extracted = '\n'.join([t.get_text(strip=True) for t in texts])

        content += extracted  # Combine CMS tag + contenu extrait

        # 🧠 Prompt pour améliorer le contenu avec OpenAI
        prompt = f"Voici le contenu d'un site web :\n{content}\n\nAméliore ce contenu pour le rendre plus engageant, plus clair, et optimisé pour le SEO. Propose une version modifiée mais conserve le sens."

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Tu es un expert en amélioration de contenu web."},
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
