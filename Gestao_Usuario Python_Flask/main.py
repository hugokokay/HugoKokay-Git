from flask import Flask

# inicialização do aplicativo Flask
app = Flask(__name__)

#rotas
@app.route('/') 
def ola_mundo():
    return "Olá, Mundo!"

# execução do aplicativo
app.run (debug=True) # modo de depuração ativado