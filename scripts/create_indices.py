"""
Script para criar índices nas tabelas do banco de dados.
Melhora a performance de consultas e joins.
Execute: python scripts/create_indices.py
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
    else:
        logger.error("Não foi possível conectar ao banco de dados")
        return False


def create_original_table_indices() -> bool:
    """
    Cria índices para a tabela original o.Tabelona.
    """
    conn = db_config.get_connection()
    if not conn:
        logger.error("Erro ao conectar ao banco de dados")
        return False

    indices = [
        ("idx_tabelona_gameid", "CREATE INDEX IF NOT EXISTS idx_tabelona_gameid ON o.Tabelona(GameID);"),
        ("idx_tabelona_summonerid", "CREATE INDEX IF NOT EXISTS idx_tabelona_summonerid ON o.Tabelona(summonerId);"),
        ("idx_tabelona_championname", "CREATE INDEX IF NOT EXISTS idx_tabelona_championname ON o.Tabelona(championName);"),
        ("idx_tabelona_gamemode", "CREATE INDEX IF NOT EXISTS idx_tabelona_gamemode ON o.Tabelona(GameMode);"),
        ("idx_tabelona_win", "CREATE INDEX IF NOT EXISTS idx_tabelona_win ON o.Tabelona(win);"),
        ("idx_tabelona_teamid", "CREATE INDEX IF NOT EXISTS idx_tabelona_teamid ON o.Tabelona(teamId);"),
        ("idx_tabelona_position", "CREATE INDEX IF NOT EXISTS idx_tabelona_position ON o.Tabelona(individualPosition);"),
        ("idx_tabelona_lane", "CREATE INDEX IF NOT EXISTS idx_tabelona_lane ON o.Tabelona(lane);"),
    ]

    try:
        with conn.cursor() as cursor:
            for index_name, index_sql in indices:
                try:
                    cursor.execute(index_sql)
                    logger.info(f"Índice {index_name} criado")
                except Exception as e:
                    logger.warning(f"Erro ao criar índice {index_name}: {e}")

        conn.commit()
        logger.info("Índices da tabela o.Tabelona criados")
        return True
    except Exception as e:
        conn.rollback()
        logger.error(f"Erro ao criar índices da tabela original: {e}")
        return False
    finally:
        conn.close()


def create_normalized_table_indices() -> bool:
    """
    Cria índices para as tabelas normalizadas (schema n).
    """
    conn = db_config.get_connection()
    if not conn:
        logger.error("Erro ao conectar ao banco de dados")
        return False

    indices = [
        # n.Partida
        ("idx_partida_gamemode", "CREATE INDEX IF NOT EXISTS idx_partida_gamemode ON n.Partida(GameMode);"),
        
        # n.Time
        ("idx_time_gameid", "CREATE INDEX IF NOT EXISTS idx_time_gameid ON n.Time(GameID);"),
        ("idx_time_win", "CREATE INDEX IF NOT EXISTS idx_time_win ON n.Time(win);"),
        
        # n.Participacao
        ("idx_participacao_championid", "CREATE INDEX IF NOT EXISTS idx_participacao_championid ON n.Participacao(championID);"),
        ("idx_participacao_summonerid", "CREATE INDEX IF NOT EXISTS idx_participacao_summonerid ON n.Participacao(summonerId);"),
        ("idx_participacao_position", "CREATE INDEX IF NOT EXISTS idx_participacao_position ON n.Participacao(individualPosition);"),
        ("idx_participacao_lane", "CREATE INDEX IF NOT EXISTS idx_participacao_lane ON n.Participacao(lane);"),
        ("idx_participacao_teamid", "CREATE INDEX IF NOT EXISTS idx_participacao_teamid ON n.Participacao(teamId);"),
        
        # n.Stats_Jogador
        ("idx_stats_kills", "CREATE INDEX IF NOT EXISTS idx_stats_kills ON n.Stats_Jogador(kills);"),
        ("idx_stats_deaths", "CREATE INDEX IF NOT EXISTS idx_stats_deaths ON n.Stats_Jogador(deaths);"),
        ("idx_stats_goldearned", "CREATE INDEX IF NOT EXISTS idx_stats_goldearned ON n.Stats_Jogador(goldEarned);"),
        ("idx_stats_damage", "CREATE INDEX IF NOT EXISTS idx_stats_damage ON n.Stats_Jogador(totalDamageDealtToChampions);"),
        ("idx_stats_visionscore", "CREATE INDEX IF NOT EXISTS idx_stats_visionscore ON n.Stats_Jogador(visionScore);"),
    ]

    try:
        with conn.cursor() as cursor:
            for index_name, index_sql in indices:
                try:
                    cursor.execute(index_sql)
                    logger.info(f"Índice {index_name} criado")
                except Exception as e:
                    logger.warning(f"Erro ao criar índice {index_name}: {e}")

        conn.commit()
        logger.info("Índices das tabelas normalizadas criados")
        return True
    except Exception as e:
        conn.rollback()
        logger.error(f"Erro ao criar índices das tabelas normalizadas: {e}")
        return False
    finally:
        conn.close()


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

