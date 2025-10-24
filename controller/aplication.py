
from flask import render_template, request, redirect, url_for
from db.db_connector import GiftRepository 

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

    

    def get_gift_list(self):
        """Busca todos os presentes usando a camada de repositório."""
        return repo.get_all_gifts()

    def mark_gift_as_bought(self, gift_id):
        """Marca um presente como comprado usando a camada de repositório."""
        try:
            return repo.mark_gift_as_bought(int(gift_id))
        except ValueError:
            return False
    
    def render_casamento(self):
        """Renderiza a página principal do Casamento."""
        
        presentes = self.get_gift_list()
        return render_template('casamento.tpl', lista_itens=presentes)