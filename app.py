from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import openai
import os

app = Flask(__name__)
CORS(app, origins=["https://autowebai.netlify.app"])

# Clé API OpenAI stockée dans l’environnement (via Render)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    title = data.get('title', '')
    content = data.get('content', '')

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Tu es un assistant expert en rédaction web et SEO."},
                {"role": "user", "content": f"Améliore ce contenu de page :\n\n{content}"}
            ]
        )

        improved = response["choices"][0]["message"]["content"]

        return jsonify({
            "original_title": title,
            "original_content": content,
            "suggested_update": improved
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/fetch-wp', methods=['POST'])
def fetch_wp():
    data = request.json
    url = data.get('siteURL')

    if not url:
        return jsonify({'error': 'URL manquante'}), 400

    try:
        if url.endswith("/"):
            url = url[:-1]

        api_url = f"{url}/wp-json/wp/v2/pages"
        response = requests.get(api_url)

        if response.status_code != 200:
            return jsonify({'error': 'Impossible de récupérer les pages'}), 500

        pages = response.json()
        pages_data = [{'title': p['title']['rendered'], 'content': p['content']['rendered']} for p in pages]

        return jsonify({'pages': pages_data})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run()
