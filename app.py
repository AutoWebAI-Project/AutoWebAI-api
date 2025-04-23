from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app, origins=["https://autowebai.netlify.app"])

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    title = data.get('title', '')
    content = data.get('content', '')

    improved = f"Voici une version améliorée du contenu de la page '{title}' :\n\n{content}\n\n[Version améliorée par IA]"

    return jsonify({
        "original_title": title,
        "original_content": content,
        "suggested_update": improved
    })

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
