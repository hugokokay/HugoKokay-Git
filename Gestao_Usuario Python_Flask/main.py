from flask import Flask, url_for, render_template

# inicialização do aplicativo Flask
app = Flask(__name__)

#rotas
@app.route('/') 
def ola_mundo():
    return render_template("index.html")

@app.route('/sobre')
def pagina_sobre():
    return """
          <b>Programador Python</b>: assita os videos no
          <a href="https://www.youtube.com/@programadorpython">Canal do YouTube</a>
          """

app.run(debug=True)