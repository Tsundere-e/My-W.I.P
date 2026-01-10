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
    try:
        user_resp = py_requests.get(f"https://api.github.com/users/{GITHUB_USER}")
        repos_resp = py_requests.get(f"https://api.github.com/users/{GITHUB_USER}/repos?sort=updated")
        
        user_data = user_resp.json()
        all_repos = repos_resp.json()
        
        # Check if the response is actually a list
        if not isinstance(all_repos, list):
            return render_template('index.html', user=user_data, repos=[], error="GitHub API limit reached. 🍓")

        esconder = ["My-W.I.P", "Tsundere-e"]
        repos_data = [repo for repo in all_repos if isinstance(repo, dict) and repo.get('name') not in esconder]
            
    except Exception as e:
        return f"Technical error: {e}"

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

@app.route('/get_response', methods=['POST'])
def get_response():
    try:
        data = request.json
        user_message = data.get('message')
        prompt = (
            f"Act as My Melody, a Senior Engineering Math tutor. Sweet personality "
            f"using 🍓 and 🌸, but highly technical. Focus on Viète's formulas, "
            f"irrational roots, and complex Math 2 problems. Help with: {user_message}"
        )
        response = model.generate_content(prompt)
        return jsonify({'reply': response.text})
    except Exception:
        return jsonify({'reply': "My melody ears are hurting... error! 🍓"}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
