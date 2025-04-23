from flask import Flask, request, jsonify

app = Flask(__name__)

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