import os
import requests as py_requests
import google.generativeai as genai
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

GITHUB_USER = "Tsundere-e"

@app.route('/')
def home():
    user_data = {}
    repos_data = []
    try:
        user_resp = py_requests.get(f"https://api.github.com/users/{GITHUB_USER}")
        repos_resp = py_requests.get(f"https://api.github.com/users/{GITHUB_USER}/repos?sort=updated")
        
        if user_resp.status_code == 200:
            user_data = user_resp.json()
        
        if repos_resp.status_code == 200:
            all_repos = repos_resp.json()
            if isinstance(all_repos, list):
                esconder = ["My-W.I.P", "Tsundere-e"]
                repos_data = [r for r in all_repos if r.get('name') not in esconder]
    except Exception:
        pass 

    return render_template('index.html', user=user_data, repos=repos_data)

@app.route('/my-portfolio')
def my_portfolio():
    return render_template('my-portfolio.html', title="My Portfolio")

@app.route('/portal/<card_name>')
def portal(card_name):
    if card_name == 'strawberry':
        return render_template('list_view.html', title="Strawberry Project")
    elif card_name == 'mymelody':
        return render_template('github_preview.html', title="My Melody API")
    elif card_name == 'engineering':
        return render_template('diary_view.html', title="Computer Engineering")
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    try:
        data = request.json
        user_msg = data.get('message')
        
        prompt = (
            f"Act as My Melody, a Senior Engineering Math tutor. Sweet personality (🍓🌸), but highly technical. "
            f"Step-by-step for Cubics (ax^3 + bx^2 + cx + d = 0): "
            f"1. Tschirnhaus (x = y - b/3a) to get y^3 + py + q = 0. "
            f"2. Identity 4cos^3(theta) - 3cos(theta) = cos(3theta). "
            f"3. Calculate theta and find the 3 roots. "
            f"Explain everything to the user: {user_msg}"
        )
        
        response = model.generate_content(prompt)
        return jsonify({'reply': response.text})
    except Exception:
        return jsonify({'reply': "My melody ears are hurting... 🍓"}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
