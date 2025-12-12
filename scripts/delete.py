"""
Script de limpeza do banco de dados.
Deleta todas as tabelas e schemas criados (o e n).
Execute com cuidado: python scripts/delete.py
"""

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
    logger.error("Não foi possível conectar ao banco de dados")
    return False


def confirm_deletion() -> bool:
    """
    Confirma com o usuário antes de deletar.
    Retorna True se o usuário confirmar, False caso contrário.
    """
    logger.warning("=" * 60)
    logger.warning("LIMPEZA DO BANCO DE DADOS")
    logger.warning("ATENCAO: Esta operacao vai deletar TODAS as tabelas e schemas!")
    logger.warning("Schemas que serao deletados: 'o' (tabela o.Tabelona), 'n' (todas as tabelas normalizadas), 'dw' (Data Warehouse)")
    logger.warning("Esta operacao NAO pode ser desfeita!")

    while True:
        try:
            confirmation = input("Digite 'DELETAR' para confirmar ou 'cancelar' para abortar: ").strip()
            if confirmation.upper() == "DELETAR":
                logger.warning("Confirmação recebida. Apagando banco de dados.")
                return True
            elif confirmation.lower() == "cancelar":
                logger.info("Operação cancelada pelo usuário.")
                return False
            else:
                logger.warning("Resposta inválida. Digite 'DELETAR' ou 'cancelar'.")
        except (EOFError, KeyboardInterrupt):
            logger.info("Operação cancelada pelo usuário (interrupção de teclado).")
            return False


def delete_normalized_tables() -> bool:
    """
    Deleta todas as tabelas do schema n na ordem correta (respeitando foreign keys).
    """
    conn = db_config.get_connection()
    if not conn:
        logger.error("Erro ao conectar ao banco de dados")
        return False

    try:
        with conn.cursor() as cursor:
            tables_to_delete = [
                "n.Stats_Jogador",
                "n.JogadorItem",
                "n.Participacao",
                "n.Time",
                "n.Partida",
                "n.Campeao",
                "n.ContaJogador",
            ]
            for table in tables_to_delete:
                cursor.execute(f"DROP TABLE IF EXISTS {table} CASCADE;")
        conn.commit()
        logger.info("Tabelas do schema n deletadas")
        return True
    except Exception as e:
        conn.rollback()
        logger.error(f"Erro ao deletar tabelas normalizadas: {e}")
        return False
    finally:
        conn.close()


def delete_original_tables() -> bool:
    """Deleta todas as tabelas do schema o."""
    conn = db_config.get_connection()
    if not conn:
        logger.error("Erro ao conectar ao banco de dados")
        return False

    try:
        with conn.cursor() as cursor:
            cursor.execute("DROP TABLE IF EXISTS o.Tabelona CASCADE;")
        conn.commit()
        logger.info("Tabela o.Tabelona deletada")
        return True
    except Exception as e:
        conn.rollback()
        logger.error(f"Erro ao deletar tabelas originais: {e}")
        return False
    finally:
        conn.close()


def delete_dw_tables() -> bool:
    """
    Deleta todas as tabelas do schema dw na ordem correta (respeitando foreign keys).
    """
    conn = db_config.get_connection()
    if not conn:
        logger.error("Erro ao conectar ao banco de dados")
        return False

    try:
        with conn.cursor() as cursor:
            tables_to_delete = [
                "dw.fato_Performance",
                "dw.dim_DetalhesPartida",
                "dw.dim_FaixaTempo",
                "dw.dim_Jogador",
                "dw.dim_Campeao",
            ]
            for table in tables_to_delete:
                cursor.execute(f"DROP TABLE IF EXISTS {table} CASCADE;")
        conn.commit()
        logger.info("Tabelas do schema dw deletadas")
        return True
    except Exception as e:
        conn.rollback()
        logger.error(f"Erro ao deletar tabelas do Data Warehouse: {e}")
        return False
    finally:
        conn.close()


def delete_schemas() -> bool:
    """Deleta os schemas o, n e dw."""
    conn = db_config.get_connection()
    if not conn:
        logger.error("Erro ao conectar ao banco de dados")
        return False
    try:
        with conn.cursor() as cursor:
            for schema in ["dw", "n", "o"]:
                cursor.execute(f"DROP SCHEMA IF EXISTS {schema} CASCADE;")
        conn.commit()
        logger.info("Schemas deletados")
        return True
    except Exception as e:
        conn.rollback()
        logger.error(f"Erro ao deletar schemas: {e}")
        return False
    finally:
        conn.close()


def main():
    """Função principal do script de limpeza."""
    if not check_database_connection():
        logger.error("Erro: Não foi possível conectar ao banco de dados. Verifique se o container PostgreSQL está rodando.")
        sys.exit(1)

    if not confirm_deletion():
        logger.info("Operação cancelada. Nenhuma alteração foi feita.")
        return

    logger.info("Iniciando deleção...")

    success = True
    if not delete_dw_tables():
        success = False
    if not delete_normalized_tables():
        success = False
    if not delete_original_tables():
        success = False
    if not delete_schemas():
        success = False

    if success:
        logger.success("Limpeza do banco de dados concluída com sucesso!")
    else:
        logger.error("Limpeza concluída com alguns erros. Verifique os logs.")


if __name__ == "__main__":
    main()
