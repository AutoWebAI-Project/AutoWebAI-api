from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app, origins=["https://autowebai.netlify.app"])

# Configuration de l'API OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/analyze-url', methods=['POST'])
def analyze_url():
    data = request.json
    url = data.get('url')
    cms = data.get('cms', 'auto')
    goal = data.get('goal', 'vente')
    tone = data.get('tone', 'professionnel')

    if not url:
        return jsonify({'error': 'URL manquante'}), 400

    try:
        # Introduction personnalisée selon le CMS
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

        # Extraction du contenu HTML du site
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        texts = soup.find_all(['p', 'h1', 'h2', 'h3', 'h4'])
        extracted = '\n'.join([t.get_text(strip=True) for t in texts])
        content += extracted

        # Prompt personnalisé pour OpenAI
        prompt = (
            f"Voici le contenu d'un site web :\n{content}\n\n"
            f"Améliore ce contenu pour le rendre plus engageant, plus clair, et optimisé pour le SEO.\n"
            f"L'objectif du site est : {goal}.\n"
            f"Utilise un ton : {tone}.\n"
            f"Propose une version modifiée mais conserve le sens."
        )

        # Appel à OpenAI
        response = openai.ChatCompletion.create(
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
