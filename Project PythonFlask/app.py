# importação
from pickle import GET 
from flask import Flask, request, jsonify #importação do Flask e outras funcionalidades
from flask_sqlalchemy import SQLAlchemy #importação para lidar com banco de dados
from flask_cors import CORS #importação para lidar com CORS
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user #importação para lidar com autenticação de usuários

# criação da aplicação
app = Flask(__name__)
CORS(app) #Habilitar CORS na aplicação


app.config['SECRET_KEY'] = "minha_chave_123" #Chave secreta para sessões
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db' # Conexão com o banco de dados
login_manager = LoginManager()
db = SQLAlchemy(app)
login_manager.init_app(app)
login_manager.login_view = 'login'  # Rota de login




#Modelagem de dados
#Criar as tabelas no banco de dados
#Para criar as tabelas, abra o terminal Python e execute os comandos abaixo:
#>>> flask shell
#>>> db.drop_all()
#>>> db.create_all()
#>>> db.session.commit()
#>>> exit()

#Criar um usuário admin para testes no terminal Python:
#>>> flask shell
#>>> user = User(username="admin" , password="123") 
#>>> db.session.add(user)
#>>> db.session.commit()

#Usuário (id, username, password)
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)


#Produto (id, name, price, description)
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)

#Função para carregar o usuário
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id)) #Retorna o usuário com o id fornecido

#Definir uma rota para login via API
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data.get("username")).first() 
    if user and data.get("password") == user.password: #Se o usuário existir e a senha estiver correta
        login_user(user)
        return jsonify({"message": "Login successful!"})
    return jsonify({"message": "Invalid credentials!"}), 401

#Definir uma rota para logout via API
@app.route('/logout', methods=["POST"])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logout successful!"})


#Definir uma rota para adicionar produtos via API
@app.route('/api/products/add', methods=["POST"])
@login_required
def add_product():
    data = request.json
    if 'name' in data and 'price' in data:
        product = Product(name=data["name"], price=data["price"], description=data.get("description", "")) #Na descrição, se não tiver, coloca vazio
        db.session.add(product)
        db.session.commit()
        return jsonify({"mesage": "Produto cadastrado com sucesso!"})
    return jsonify({"mesage": "Dados inválidos!"}), 400


#definir uma rota para deletar produtos via API
@app.route('/api/products/delete/<int:product_id>', methods=["DELETE"])
@login_required
def delete_product(product_id):
    product = Product.query.get(product_id)
    if product: #Se o produto existir (tem algum produto com esse id)
        db.session.delete(product)
        db.session.commit()
        return jsonify({"message": "Produto deletado com sucesso!"})
    return jsonify({"message": "Produto não encontrado!"}), 404

#definir uma rota para listar todos os produtos via API
@app.route('/api/products/<int:product_id>', methods=["GET"])
def get_products_details(product_id):
    product = Product.query.get(product_id)
    if product:
        return jsonify({
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "description": product.description
        })
    return jsonify({"message": "Produto não encontrado!"}), 404

#definir uma rota para atualizar produtos via API
@app.route('/api/products/update/<int:product_id>', methods=["PUT"])
@login_required
def update_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"message": "Produto não encontrado!"}), 404
    data = request.json
    if 'name' in data:
        product.name = data['name']
        if 'price' in data:
            product.price = data['price']
            if 'description' in data:
                product.description = data['description']
    db.session.commit()
    return jsonify({"message": "Produto atualizado com sucesso!"})

#definir uma rota para listar todos os produtos via API
@app.route('/api/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    product_list = [] #Lista vazia para armazenar os produtos
    for product in products:
        product_data = {
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "description": product.description
        }
        product_list.append(product_data) #Adiciona o dicionário na lista
    return jsonify(product_list)




#Definir uma rota raiz (página inicial) a função que será executada ao requisitar essa rota!
@app.route('/')
def hello_world():
    return 'Hello World!!'


if __name__ == "__main__":
    app.run(debug=True)
