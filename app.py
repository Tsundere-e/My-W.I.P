from flask import Flask, render_template
import requests

app = Flask(__name__)

# Seu usuário do GitHub
GITHUB_USER = "tsundere-e"

@app.route('/')
def home():
    try:
        # Pega seus dados e repositórios
        user_data = requests.get(f"https://api.github.com/users/{GITHUB_USER}").json()
        repos_data = requests.get(f"https://api.github.com/users/{GITHUB_USER}/repos?sort=updated").json()
        
        # Se der erro na API (limite de requisições)
        if 'message' in user_data:
            return "Erro: O GitHub não deixou eu ver seu perfil agora. Tente em alguns minutos! 🍓"
            
    except Exception as e:
        return f"Houve um erro técnico: {e}"

    return render_template('index.html', user=user_data, repos=repos_data)

if __name__ == '__main__':
    app.run(debug=True)