"""
Script para criar índices nas tabelas do banco de dados.
Lê e executa o arquivo SQL de índices da pasta objetos.
Melhora a performance de consultas e joins.
Execute: python scripts/create_indices.py
"""
import os
import sys
from pathlib import Path

from loguru import logger

import utils.database_config as db_config


def check_database_connection() -> bool:
    """Verifica se a conexão com o banco de dados está disponível."""
    conn = db_config.get_connection()
    if conn:
        conn.close()
        return True
    else:
        logger.error("Não foi possível conectar ao banco de dados")
        return False


def create_indices_from_file(indices_path: str) -> bool:
    """
    Cria índices a partir de um arquivo SQL.
    """
    conn = db_config.get_connection()
    if not conn:
        logger.error("Erro ao conectar ao banco de dados")
        return False

    try:
        indices_file_path = Path(indices_path)
        if not indices_file_path.exists():
            raise FileNotFoundError(f"Arquivo de índices não encontrado em {indices_file_path}")

        with open(indices_file_path, "r", encoding="utf-8") as indices_file:
            indices_sql = indices_file.read()

        with conn.cursor() as cursor:
            db_config.execute_multiple_statements(indices_sql, cursor)
        conn.commit()
        logger.info("Índices criados com sucesso")
        return True
    except Exception as e:
        conn.rollback()
        logger.error(f"Erro ao criar índices: {e}")
        return False
    finally:
        conn.close()


def create_original_table_indices() -> bool:
    """
    Cria índices para a tabela original o.Tabelona.
    Mantido para compatibilidade com código existente.
    """
    indices_path = os.path.join("objetos", "Indices.sql")
    return create_indices_from_file(indices_path)


def create_normalized_table_indices() -> bool:
    """
    Cria índices para as tabelas normalizadas (schema n).
    Mantido para compatibilidade com código existente.
    """
    indices_path = os.path.join("objetos", "Indices.sql")
    return create_indices_from_file(indices_path)


def main():
    """Função principal do script de criação de índices."""
    if not check_database_connection():
        print("\nErro: Não foi possível conectar ao banco de dados.")
        print("Verifique se o container PostgreSQL está rodando.")
        sys.exit(1)

    print("\n" + "=" * 60)
    print("  CRIAÇÃO DE ÍNDICES")
    print("=" * 60)

    success = True

    print("\nCriando índices para tabela original (o.Tabelona)...")
    if not create_original_table_indices():
        success = False

    print("\nCriando índices para tabelas normalizadas (schema n)...")
    if not create_normalized_table_indices():
        success = False

    print("\n" + "=" * 60)
    if success:
        logger.info("Criação de índices concluída com sucesso")
        print("Criação de índices concluída com sucesso!")
    else:
        logger.error("Criação de índices concluída com erros")
        print("Criação de índices concluída com alguns erros. Verifique os logs.")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()

