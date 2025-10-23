# controller/aplication.py

from flask import render_template, request, redirect, url_for
from db.db_connector import GiftRepository 

# Instancia o Repositório, que já carrega o DB no construtor
repo = GiftRepository() 

class Aplication:
    """
    Classe de Lógica de Negócio (Controller).
    Gerencia a interação entre a View e o Repositório de Dados.
    """
    def __init__(self):
        self.pages = {
            'casamento': self.render_casamento,
        }

    def render(self, page):
        content_function = self.pages.get(page, self.render_casamento)
        return content_function()

    # -----------------------------------------------------
    # MÉTODOS DE NEGÓCIO (Usando o Repositório)
    # -----------------------------------------------------

    def get_gift_list(self):
        """Busca todos os presentes usando a camada de repositório."""
        return repo.get_all_gifts()

    def mark_gift_as_bought(self, gift_id):
        """Marca um presente como comprado usando a camada de repositório."""
        try:
            return repo.mark_gift_as_bought(int(gift_id))
        except ValueError:
            return False
    
    # -----------------------------------------------------
    # MÉTODOS DE RENDERIZAÇÃO
    # -----------------------------------------------------

    def render_casamento(self):
        """Renderiza a página principal do Casamento."""
        
        presentes = self.get_gift_list()
        
        # O nome do template é 'casamento.tpl'
        return render_template('casamento.tpl', lista_itens=presentes)