import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path("DBScore.sqlite3")

class DBProxy:
    """Gerencia o banco de dados de scores."""

    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        """Cria a tabela de scores se não existir."""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS scores (
                play INTEGER PRIMARY KEY,
                score INTEGER NOT NULL,
                date TEXT NOT NULL
            )
        """)
        self.conn.commit()

    def save(self, score: int):
        """Salva um novo score no banco."""
        self.cursor.execute("SELECT MAX(play) FROM scores")
        last_play = self.cursor.fetchone()[0]
        next_play = 1 if last_play is None else last_play + 1

        date_str = datetime.now().strftime("%H:%M - %d/%m/%y")
        self.cursor.execute(
            "INSERT INTO scores (play, score, date) VALUES (?, ?, ?)",
            (next_play, score, date_str)
        )
        self.conn.commit()

    def retrieve_top10(self):
        """Retorna os 10 maiores scores."""
        self.cursor.execute(
            "SELECT play, score, date FROM scores ORDER BY score DESC, play ASC LIMIT 10"
        )
        return self.cursor.fetchall()

    def get_high_score(self) -> int:
        """Retorna o maior score ou 0 se não houver nenhum."""
        self.cursor.execute("SELECT MAX(score) FROM scores")
        result = self.cursor.fetchone()[0]
        return result if result is not None else 0

    def close(self):
        """Fecha a conexão com o banco."""
        self.conn.close()
