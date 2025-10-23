# db_connector.py

import psycopg2
import os
from typing import Dict, Any, List, Tuple
from dotenv import load_dotenv 
from contextlib import contextmanager

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

class GiftRepository:
    """
    Classe de Repositório (DAL). Gerencia o acesso ao PostgreSQL.
    """
    
    # -----------------------------------------------------
    # DADOS INICIAIS DO PROJETO (Estrutura: nome, comprado_boolean)
    # -----------------------------------------------------
    INITIAL_GIFTS = [
        ("Escorredor de Pratos", False),
        ("Cafeteira", False),
        ("Filtro de Barro", False),
        ("Garrafa de Café", False),
        ("Jarro de Vidro", False),
        ("Kit de Xícaras", False),
        ("Sanduicheira", False),
        ("Chaleira Elétrica", False),
        ("Jogo de Copos", False),
        ("Jogo de Colheres de Silicone", False),
        ("Jogo de Facas", False),
        ("Jogo de Formas", False),
        ("Jogo de Marinex", False),
        ("Jogo de Vasilhas", False),
        ("Jogo de Porta Temperos Multifuncional", False),
        ("Cesto Organizador de Cozinha", False),
        ("Cortador Multifuncional", False),
        ("Liquidificador", False),
        ("Jogo de Panelas", False),
        ("Panela de Pressão", False),
        ("Jogo de Pratos", False),
        ("Jogo de Talheres", False)
    ]
    
    def __init__(self):
        self.db_params = {
            "dbname": os.getenv("DB_NAME", "casamento_db"),
            "user": os.getenv("DB_USER", "postgres"),
            "password": os.getenv("DB_PASS", ""),
            "host": os.getenv("DB_HOST", "localhost"),
            "port": os.getenv("DB_PORT", "5432")
        }
        self.ensure_tables_exist()
        self.initialize_data()

    # ... (métodos de conexão e get_cursor permanecem iguais) ...
    def _get_connection(self):
        try:
            return psycopg2.connect(**self.db_params)
        except Exception as e:
            print(f"ERRO CRÍTICO: Falha de conexão com o Banco de Dados. Erro: {e}")
            raise 

    @contextmanager
    def get_cursor(self, commit: bool = False):
        conn = None
        try:
            conn = self._get_connection()
            cur = conn.cursor()
            yield cur
            if commit:
                conn.commit()
            cur.close()
        except Exception as e:
            if conn:
                conn.rollback()
            raise e
        finally:
            if conn:
                conn.close()

    def ensure_tables_exist(self):
        """Cria a tabela 'gifts' (AGORA SEM O LINK) e força o reset se o esquema mudar."""
        try:
            with self.get_cursor(commit=True) as cur:
                # 🚨 DROP TABLE NECESSÁRIO PARA GARANTIR O NOVO ESQUEMA SEM 'link'
                cur.execute("""
                    DROP TABLE IF EXISTS gifts;
                    
                    CREATE TABLE gifts (
                        id SERIAL PRIMARY KEY,
                        nome VARCHAR(100) NOT NULL UNIQUE, 
                        comprado BOOLEAN DEFAULT FALSE NOT NULL
                    );
                """)
        except Exception as e:
            print(f"Erro ao criar tabela 'gifts': {e}")

    def initialize_data(self):
        """Insere os dados iniciais SE a tabela estiver vazia."""
        query_check = "SELECT COUNT(*) FROM gifts;"
        
        try:
            with self.get_cursor(commit=False) as cur:
                cur.execute(query_check)
                count = cur.fetchone()[0]
                
                if count > 0:
                    print("INFO: Tabela 'gifts' já contém dados. Inicialização ignorada.")
                    return
                
            self.insert_initial_gifts(self.INITIAL_GIFTS)
            print("INFO: Dados iniciais da lista de presentes inseridos com sucesso!")
            
        except Exception as e:
            print(f"ERRO: Falha ao inicializar dados no DB: {e}")
    
    # -----------------------------------------------------
    # MÉTODOS DE OPERAÇÃO DO REPOSITÓRIO (DAL)
    # -----------------------------------------------------
    
    def get_all_gifts(self) -> List[Dict[str, Any]]:
        """Recupera todos os presentes (query sem 'link')."""
        query = "SELECT id, nome, comprado FROM gifts ORDER BY id;"
        
        try:
            with self.get_cursor(commit=False) as cur:
                cur.execute(query)
                col_names = [desc[0] for desc in cur.description]
                results = [dict(zip(col_names, row)) for row in cur.fetchall()]
                return results
        except Exception as e:
            print(f"Erro ao buscar presentes: {e}")
            return []

    def mark_gift_as_bought(self, gift_id: int) -> bool:
        """Atualiza o status 'comprado' de um presente."""
        query = "UPDATE gifts SET comprado = TRUE WHERE id = %s AND comprado = FALSE;"
        try:
            with self.get_cursor(commit=True) as cur:
                cur.execute(query, (gift_id,))
                return cur.rowcount > 0 
        except Exception as e:
            print(f"Erro ao marcar presente como comprado: {e}")
            return False

    def insert_initial_gifts(self, gifts_data: List[Tuple]) -> None:
        """Insere dados iniciais no banco de dados (SQL ajustado para 2 parâmetros)."""
        # 🚨 SQL AJUSTADO: Valores apenas para 'nome' e 'comprado'
        query = """
            INSERT INTO gifts (nome, comprado) 
            VALUES (%s, %s) 
            ON CONFLICT (nome) DO NOTHING;
        """
        try:
            with self.get_cursor(commit=True) as cur:
                cur.executemany(query, gifts_data)
        except Exception as e:
            print(f"Erro ao inserir dados iniciais: {e}")
            raise