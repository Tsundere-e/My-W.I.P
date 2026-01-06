from flask import Flask, render_template
import requests

app = Flask(__name__)

# My Github user
GITHUB_USER = "tsundere-e"

@app.route('/')
def home():
    try:
        # repository
        user_data = requests.get(f"https://api.github.com/users/{GITHUB_USER}").json()
        repos_data = requests.get(f"https://api.github.com/users/{GITHUB_USER}/repos?sort=updated").json()
        
        # api error
        if 'message' in user_data:
            return "Erro: O GitHub não deixou eu ver seu perfil agora. Tente em alguns minutos! 🍓"
            
    except Exception as e:
        return f"Houve um erro técnico: {e}"

    return render_template('index.html', user=user_data, repos=repos_data)

if __name__ == '__main__':

    app.run(debug=True)
