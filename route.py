# route.py

from flask import Flask, request, redirect, url_for
from controller.aplication import Aplication # Importa sua classe OO

# 🚨 Configura o Flask para procurar templates na pasta 'views'
app = Flask(__name__, template_folder='views') 

# Instancia a classe que gerencia a lógica
aplication = Aplication()

# -----------------------------------------------------
# ROTEAMENTO HTTP (GET e POST)
# -----------------------------------------------------

# 1. Rota Principal (GET): Exibe a Lista de Presentes
@app.route('/', methods=['GET'])
def inicio():
    # Chama o método render da sua classe, que retorna o template
    return aplication.render('casamento')

# 2. Rota de Ação (POST): Marca um presente como comprado
@app.route('/comprar', methods=['POST'])
def comprar():
    # Obtém o ID do presente enviado pelo formulário HTML
    gift_id = request.form.get('gift_id')
    
    if gift_id:
        # Chama o método OO para persistir a mudança
        aplication.mark_gift_as_bought(gift_id)
    
    # Redireciona o usuário de volta para a página inicial (evita reenvio do POST)
    return redirect(url_for('inicio'))

if __name__ == '__main__':
    # Roda o servidor no modo DEBUG (recarrega automático e mostra erros no navegador)
    app.run(host='0.0.0.0', port=5001, debug=True)