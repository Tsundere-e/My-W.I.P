from flask import Flask, render_template
import requests

app = Flask(__name__)

# My Github user
GITHUB_USER = "tsundere-e"

@app.route('/')
def home():
    try:
        user_data = requests.get(f"https://api.github.com/users/{GITHUB_USER}").json()
        all_repos = requests.get(f"https://api.github.com/users/{GITHUB_USER}/repos?sort=updated").json()
        
        # hidden 🤫
        esconder = ["My-W.I.P", "Tsundere-e"]

        # Filter
        repos_data = [repo for repo in all_repos if repo['name'] not in esconder]
            
        if 'message' in user_data:
            return "Erro: O GitHub não deixou eu ver seu perfil agora. 🍓"
            
    except Exception as e:
        return f"Houve um erro técnico: {e}"

    return render_template('index.html', user=user_data, repos=repos_data)
    
@app.route('/projeto/<nome_do_projeto>')
def detalhe_projeto(nome_do_projeto):
    # lista de sub-itens
    return render_template('projeto_detalhes.html', titulo=nome_do_projeto)

if __name__ == '__main__':

    app.run(debug=True)



