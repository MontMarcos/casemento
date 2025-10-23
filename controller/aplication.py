# controller/aplication.py

import json
from flask import render_template, request, redirect, url_for
from pathlib import Path 

# Define o caminho seguro do arquivo JSON a partir da localização do controller
GIFTS_DB_PATH = Path(__file__).parent.parent / 'db' / 'gifts.json'

class Aplication:
    """
    Classe de Lógica (Controller): Gerencia o conteúdo e a persistência dos dados.
    """
    def __init__(self):
        self.pages = {
            'casamento': self.render_casamento,
        }

    def render(self, page):
        # Despacho: Se não encontrar, usa render_casamento como fallback
        content_function = self.pages.get(page, self.render_casamento)
        return content_function()
    
    # -----------------------------------------------------
    # Lógica de Persistência (Métodos de acesso ao JSON)
    # -----------------------------------------------------
    
    def get_gift_list(self):
        """Lê a lista de presentes do arquivo JSON."""
        try:
            with open(GIFTS_DB_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"ERRO CRÍTICO: Arquivo DB não encontrado em: {GIFTS_DB_PATH}")
            return [] # Retorna lista vazia para evitar crash

    def save_gift_list(self, gifts):
        """Salva a lista atualizada de presentes no arquivo JSON."""
        with open(GIFTS_DB_PATH, 'w', encoding='utf-8') as f:
            json.dump(gifts, f, indent=4, ensure_ascii=False)

    def mark_gift_as_bought(self, gift_id):
        """Marca um presente como comprado e salva no JSON."""
        gifts = self.get_gift_list()
        
        try:
            gift_id = int(gift_id)
        except ValueError:
            return False 

        found = False
        for gift in gifts:
            if gift.get('id') == gift_id:
                gift['comprado'] = True
                found = True
                break
        
        if found:
            self.save_gift_list(gifts)
            return True
        return False
    
    # -----------------------------------------------------
    # Lógica de Renderização
    # -----------------------------------------------------

    def render_casamento(self):
        """Renderiza a página principal do Casamento."""
        
        presentes = self.get_gift_list()
        
        # O nome do template é 'casamento.tpl'
        return render_template('casamento.tpl', lista_itens=presentes)