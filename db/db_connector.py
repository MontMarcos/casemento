
import psycopg2
import os
from typing import Dict, Any, List, Tuple
from dotenv import load_dotenv 
from contextlib import contextmanager

load_dotenv()

class GiftRepository:
    """
    CLASSE DE REPOSITÓRIO (DAL): Gerencia o acesso ao PostgreSQL.
    """
    
  
    INITIAL_GIFTS = [
        ("Escorredor de Pratos", False), ("Cafeteira", False), ("Aparelho de jantar")
        ("Garrafa de Café", False), ("Jarro de Vidro", False), ("Kit de Caneca", False),
        ("Sanduicheira", False), ("Chaleira Elétrica", False), ("Jogo de Copos", False),
        ("Jogo de Colheres de Silicone", False), ("Jogo de Facas", False), ("Jogo de Formas", False),
        ("Jogo de Marinex", False), ("Jogo de Vasilhas", False), ("Jogo de Porta Temperos Multifuncional", False),
        ("Cesto Organizador de Cozinha", False), ("Cortador Multifuncional", False), ("Liquidificador", False),
        ("Jogo de Panelas", False), ("Panela de Pressão", False), ("Jogo de Pratos", False),
        ("Jogo de Talheres", False),
        ("Kit de Bowls", False), ("Sanduicheira com Grill", False), ("Kit Organizador de Geladeira", False),
        ("Mixer", False), ("Kit de Utensílios de Cozinha", False), ("Kit de Mantimentos Hermético", False),
        ("Kit de Vasilha de Vidro", False)
    ]

    
    def __init__(self):
        self.DATABASE_URL = os.getenv("DATABASE_URL")
        
        if self.DATABASE_URL:
            self.db_params = {'dsn': self.DATABASE_URL}
        else:
            self.db_params = {
                "dbname": os.getenv("DB_NAME", "postgres"), 
                "user": os.getenv("DB_USER", "postgres"),
                "password": os.getenv("DB_PASS", None),
                "host": os.getenv("DB_HOST", "localhost"),
                "port": os.getenv("DB_PORT", "5432")
            }

        self.ensure_tables_exist()
        self.initialize_data()

    def _get_connection(self):
        """Estabelece e retorna uma conexão bruta."""
        try:
            return psycopg2.connect(**self.db_params)
        except Exception as e:
            print(f"ERRO CRÍTICO: Falha de conexão com o Banco de Dados.")
            print(f"Parâmetros usados: {self.db_params}")
            raise 

    @contextmanager
    def get_cursor(self, commit: bool = False):
        """Gerencia a conexão e o cursor usando um contexto."""
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
        """Cria a tabela 'gifts' (DROP table é obrigatório para resetar o esquema)"""
        try:
            with self.get_cursor(commit=True) as cur:
                cur.execute("""
                    -- Isso garante que a tabela seja criada com o esquema correto
                    DROP TABLE IF EXISTS gifts;
                    
                    CREATE TABLE gifts (
                        id SERIAL PRIMARY KEY,
                        nome VARCHAR(100) NOT NULL UNIQUE, 
                        comprado BOOLEAN DEFAULT FALSE NOT NULL
                    );
                """)
        except Exception as e:
            print(f"Erro ao criar tabela 'gifts': {e}")
            raise 

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
            raise
    
    def get_all_gifts(self) -> List[Dict[str, Any]]:
        """Recupera todos os presentes."""
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
        """Insere dados iniciais no banco de dados."""
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