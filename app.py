from flask import Flask, render_template, redirect
import requests
import os

app = Flask(__name__)

# github user
GITHUB_USER = "Tsundere-e"

@app.route('/')
def home():
    try:
        user_data = requests.get(f"https://api.github.com/users/{GITHUB_USER}").json()
        all_repos = requests.get(f"https://api.github.com/users/{GITHUB_USER}/repos?sort=updated").json()
        
        # hidden repos
        esconder = ["My-W.I.P", "Tsundere-e"]

        # filter
        repos_data = [repo for repo in all_repos if repo['name'] not in esconder]
            
        if 'message' in user_data:
            return "Erro: GitHub API limit or user not found. 🍓"
            
    except Exception as e:
        return f"Technical error: {e}"

    return render_template('index.html', user=user_data, repos=repos_data)
    
@app.route('/portal/<card_name>')
def portal(card_name):
    if card_name == 'strawberry':
        return render_template('list_view.html', title="Strawberry Project")
    
    elif card_name == 'mymelody':
        return render_template('github_preview.html', title="My Melody API")
    
    elif card_name == 'engineering':
        return render_template('diary_view.html', title="Computer Engineering")
    
    return redirect('/')

# production config
if __name__ == '__main__':
    # get port from environment for deploy
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
