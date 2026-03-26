import os
import requests as py_requests
import google.generativeai as genai
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# --- Configure Gemini safely ---
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not set in environment variables")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

GITHUB_USER = "Tsundere-e"


@app.route('/')
def home():
    user_data = {}
    repos_data = []

    try:
        user_resp = py_requests.get(
            f"https://api.github.com/users/{GITHUB_USER}", timeout=5
        )
        repos_resp = py_requests.get(
            f"https://api.github.com/users/{GITHUB_USER}/repos?sort=updated",
            timeout=5
        )

        if user_resp.ok:
            user_data = user_resp.json() or {}

        if repos_resp.ok:
            all_repos = repos_resp.json() or []

            if isinstance(all_repos, list):
                esconder = {"My-W.I.P", "Tsundere-e"}  # set = faster lookup
                repos_data = [
                    r for r in all_repos
                    if r.get('name') and r.get('name') not in esconder
                ]

    except py_requests.exceptions.RequestException as e:
        print(f"[GitHub API Error]: {e}")

    return render_template('index.html', user=user_data, repos=repos_data)


@app.route('/my-portfolio')
def my_portfolio():
    return render_template('my-portfolio.html', title="My Portfolio")


@app.route('/portal/<card_name>')
def portal(card_name):
    routes = {
        'strawberry': ('list_view.html', "Strawberry Project"),
        'mymelody': ('github_preview.html', "My Melody API"),
        'engineering': ('diary_view.html', "Computer Engineering"),
    }

    template, title = routes.get(card_name, ('index.html', None))
    return render_template(template, title=title)


@app.route('/get_response', methods=['POST'])
def get_response():
    try:
        data = request.get_json(silent=True) or {}
        user_msg = data.get('message')

        if not user_msg:
            return jsonify({'reply': "Please send a message 🍓"}), 400

        prompt = (
            "Act as My Melody, a Senior Engineering Math tutor. "
            "Sweet personality (🍓🌸), but highly technical. "
            "Step-by-step for Cubics (ax^3 + bx^2 + cx + d = 0): "
            "1. Tschirnhaus (x = y - b/3a) to get y^3 + py + q = 0. "
            "2. Identity 4cos^3(theta) - 3cos(theta) = cos(3theta). "
            "3. Calculate theta and find the 3 roots. "
            f"Explain everything to the user: {user_msg}"
        )

        response = model.generate_content(prompt)

        reply_text = getattr(response, "text", None)
        if not reply_text:
            reply_text = "I couldn't generate a response right now 🍓"

        return jsonify({'reply': reply_text})

    except Exception as e:
        print(f"[Gemini Error]: {e}")
        return jsonify({'reply': "My melody ears are hurting... 🍓"}), 500


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
