from flask import Flask, request, jsonify
from flask_cors import CORS

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

if __name__ == '__main__':
    app.run()
