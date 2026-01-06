from flask import Flask, render_template
import requests

app = Flask(__name__)

# My Github user
GITHUB_USER = "Tsundere-e"

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
    
@app.route('/category/<category_name>')
def category(category_name):
    return render_template('category.html', category=category_name)
    
@app.route('/run/<project_name>')
def run_project(project_name):
    return render_template('executor.html', project=project_name)

if __name__ == '__main__':

    app.run(debug=True)





