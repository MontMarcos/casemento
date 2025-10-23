# route.py

from flask import Flask, request, redirect, url_for
from controller.aplication import Aplication 
from db.db_connector import GiftRepository 
import os
from dotenv import load_dotenv

# -----------------------------------------------------
# CONFIGURAÇÃO E INICIALIZAÇÃO
# -----------------------------------------------------

load_dotenv()

# 🚨 ÚNICA INSTANCIAÇÃO DO REPOSITÓRIO (DAL) 🚨
# Esta linha executa o __init__ do GiftRepository, que faz o setup do DB
repo = GiftRepository() 

app = Flask(__name__, template_folder='views')
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "chave-secreta-default")

# Instancia a classe de Controller (POO)
aplication = Aplication()

# -----------------------------------------------------
# ROTEAMENTO HTTP (SOMENTE INFORMAÇÃO DE ROTAS)
# -----------------------------------------------------

@app.route('/', methods=['GET'])
def inicio():
    """Mapeia a URL '/' para a função de renderização do Controller."""
    return aplication.render('casamento')

@app.route('/comprar', methods=['POST'])
def comprar():
    """Mapeia a URL '/comprar' para a função de ação do Controller."""
    gift_id = request.form.get('gift_id')
    
    if gift_id:
        aplication.mark_gift_as_bought(gift_id)
    
    return redirect(url_for('inicio'))

if __name__ == '__main__':
    # Execute com 'python route.py'
    app.run(host='0.0.0.0', port=8080, debug=True)