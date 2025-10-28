from flask import Flask, request, redirect, url_for
from controller.aplication import Aplication 
from db.db_connector import GiftRepository 
import os
from dotenv import load_dotenv

load_dotenv()

repo = GiftRepository() 

app = Flask(__name__, template_folder='views')
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "chave-secreta-default")

aplication = Aplication()

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
    app.run(host='0.0.0.0', port=8083, debug=True)