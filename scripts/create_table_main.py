"""
Cria a tabela principal (o.Tabelona) e popula a partir de um CSV.
Use as variáveis de ambiente DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME.
"""
import argparse
import csv
import io
import os
from pathlib import Path

from loguru import logger

import utils.database_config as db_config


TABLE_COLUMNS = [
    "assists",
    "GameID",
    "GameMode",
    "baronKills",
    "bountyLevel",
    "champExperience",
    "champLevel",
    "championName",
    "damageDealtToObjectives",
    "damageSelfMitigated",
    "deaths",
    "dragonKills",
    "firstBloodAssist",
    "firstBloodKill",
    "gameEndedInSurrender",
    "goldEarned",
    "goldSpent",
    "individualPosition",
    "inhibitorKills",
    "inhibitorsLost",
    "item0",
    "item1",
    "item2",
    "item3",
    "item4",
    "item5",
    "item6",
    "kills",
    "lane",
    "largestCriticalStrike",
    "largestKillingSpree",
    "longestTimeSpentLiving",
    "magicDamageDealtToChampions",
    "magicDamageTaken",
    "nexusLost",
    "objectivesStolen",
    "physicalDamageDealtToChampions",
    "physicalDamageTaken",
    "spell1Casts",
    "spell2Casts",
    "spell3Casts",
    "spell4Casts",
    "summoner1Casts",
    "summoner2Casts",
    "summoner1Id",
    "summoner2Id",
    "summonerId",
    "teamEarlySurrendered",
    "teamId",
    "timeCCingOthers",
    "timePlayed",
    "totalDamageDealtToChampions",
    "totalDamageShieldedOnTeammates",
    "totalDamageTaken",
    "totalHeal",
    "totalHealsOnTeammates",
    "totalMinionsKilled",
    "totalTimeCCDealt",
    "totalTimeSpentDead",
    "trueDamageDealtToChampions",
    "trueDamageTaken",
    "turretTakedowns",
    "turretsLost",
    "visionScore",
    "visionWardsBoughtInGame",
    "wardsKilled",
    "wardsPlaced",
    "win",
]


def create_main_table(ddl_path: str) -> bool:
    """
    Cria o schema o e a tabela o.Tabelona conforme o arquivo SQL fornecido.
    """
    conn = db_config.get_connection()
    if not conn:
        logger.error("Erro ao conectar ao banco de dados")
        return False

    try:
        ddl_file_path = Path(ddl_path)
        if not ddl_file_path.exists():
            raise FileNotFoundError(f"DDL não encontrado em {ddl_file_path}")

        with open(ddl_file_path, "r", encoding="utf-8") as ddl_file:
            ddl_sql = ddl_file.read()

        with conn.cursor() as cursor:
            cursor.execute(ddl_sql)
        conn.commit()
        logger.info("Tabela o.Tabelona criada com sucesso")
        return True
    except Exception as e:
        conn.rollback()
        logger.error(f"Erro ao criar tabela: {e}")
        return False
    finally:
        conn.close()


def _prepare_csv(csv_path: str) -> tuple[io.StringIO, int]:
    """
    Remove a primeira coluna vazia do CSV e reordena para bater com o DDL.
    Retorna um buffer pronto para COPY e o total de linhas de dados.
    """
    with open(csv_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        try:
            raw_header = next(reader)
        except StopIteration as exc:
            raise ValueError("CSV vazio.") from exc

        header = raw_header[1:]
        if set(header) != set(TABLE_COLUMNS):
            raise ValueError("As colunas do CSV não batem com o DDL esperado.")

        col_index = {col: idx + 1 for idx, col in enumerate(header)}

        buffer = io.StringIO()
        writer = csv.writer(buffer)
        writer.writerow(TABLE_COLUMNS)

        row_count = 0
        for row in reader:
            if not row:
                continue
            ordered_row = [row[col_index[col]] for col in TABLE_COLUMNS]
            writer.writerow(ordered_row)
            row_count += 1

        buffer.seek(0)
        return buffer, row_count


def load_csv_into_table(csv_path: str, truncate: bool = False) -> bool:
    """
    Carrega um CSV em o.Tabelona usando COPY, corrigindo a primeira coluna vazia.
    """
    conn = db_config.get_connection()
    if not conn:
        logger.error("Erro ao conectar ao banco de dados")
        return False

    try:
        buffer, row_count = _prepare_csv(csv_path)
        with conn.cursor() as cursor:
            if truncate:
                cursor.execute("TRUNCATE TABLE o.Tabelona;")

            copy_sql = f"""
                COPY o.Tabelona ({', '.join(TABLE_COLUMNS)})
                FROM STDIN WITH CSV HEADER
            """
            cursor.copy_expert(copy_sql, buffer)

        conn.commit()
        logger.info(f"{row_count} linhas carregadas com sucesso")
        return True
    except Exception as e:
        conn.rollback()
        logger.error(f"Erro ao popular tabela: {e}")
        return False
    finally:
        conn.close()


def main():
    parser = argparse.ArgumentParser(
        description="Cria o schema o e carrega a Tabelona a partir de um CSV."
    )
    parser.add_argument(
        "--ddl-path",
        default=os.path.join("scripts", "sql", "ScriptTabelaOriginal.sql"),
        help="Caminho do DDL .sql da Tabelona (default: scripts/sql/ScriptTabelaOriginal.sql)",
    )
    parser.add_argument(
        "--csv",
        dest="csv_path",
        default=os.path.join("data", "Sep-29-2022_500matches.csv"),
        help="Caminho do CSV de origem (default: data/Sep-29-2022_500matches.csv)",
    )
    parser.add_argument(
        "--truncate",
        action="store_true",
        help="Limpa a tabela antes de inserir (TRUNCATE TABLE).",
    )
    parser.add_argument(
        "--create-only",
        action="store_true",
        help="Somente cria a tabela, sem carregar CSV.",
    )
    args = parser.parse_args()

    created = create_main_table(args.ddl_path)
    if not created or args.create_only:
        return

    load_csv_into_table(args.csv_path, truncate=args.truncate)


if __name__ == "__main__":
    main()