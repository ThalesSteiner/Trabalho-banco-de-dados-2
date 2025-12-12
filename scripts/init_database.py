"""
Script de inicialização interativa do banco de dados.
Pergunta ao usuário se deseja criar e popular as tabelas.
Execute manualmente com: python scripts/init_database.py
"""
import os
import sys
from pathlib import Path

from loguru import logger
import scripts.create_table_main as create_main
import scripts.create_table_normalize as create_normalize
import scripts.create_table_dw as create_dw
import scripts.create_indices as create_indices
import scripts.create_views as create_views
import scripts.create_triggers as create_triggers
import scripts.create_procedures as create_procedures
import scripts.delete as delete_module
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


def ask_user_input() -> dict:
    """
    Pergunta ao usuário o que deseja fazer.
    Retorna um dicionário com as opções escolhidas.
    """
    print("\n" + "=" * 60)
    print("  GERENCIAMENTO DO BANCO DE DADOS")
    print("=" * 60)
    print("\nOpções disponíveis:")
    print("\n  CRIAÇÃO:")
    print("    1. Criar tabela original (o.Tabelona) e popular com CSV")
    print("    2. Criar tabelas normalizadas (schema n)")
    print("    3. Criar Data Warehouse (schema dw)")
    print("    4. Criar ambas (original + normalizadas)")
    print("    5. Fazer todas as etapas (original -> normalizadas -> DW -> índices -> objetos)")
    print("    6. Criar apenas índices")
    print("    7. Criar Views")
    print("    8. Criar Triggers")
    print("    9. Criar Procedures")
    print("   10. Criar todos os objetos (Views + Triggers + Procedures)")
    print("\n  MANUTENÇÃO:")
    print("   11. Deletar tudo (tabelas e schemas)")
    print("\n  OUTRAS:")
    print("   12. Sair")
    print()

    while True:
        try:
            choice = input("Escolha uma opção (1-12): ").strip()
            if choice in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]:
                break
            else:
                print("Opção inválida. Por favor, escolha 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11 ou 12.")
        except (EOFError, KeyboardInterrupt):
            print("\nOperação cancelada pelo usuário.")
            return {"create_main": False, "create_normalized": False, "create_dw": False, "create_indices": False, "create_views": False, "create_triggers": False, "create_procedures": False, "delete_all": False, "all_steps": False}

    options = {
        "1": {"create_main": True, "create_normalized": False, "create_dw": False, "create_indices": False, "create_views": False, "create_triggers": False, "create_procedures": False, "delete_all": False, "all_steps": False},
        "2": {"create_main": False, "create_normalized": True, "create_dw": False, "create_indices": False, "create_views": False, "create_triggers": False, "create_procedures": False, "delete_all": False, "all_steps": False},
        "3": {"create_main": False, "create_normalized": False, "create_dw": True, "create_indices": False, "create_views": False, "create_triggers": False, "create_procedures": False, "delete_all": False, "all_steps": False},
        "4": {"create_main": True, "create_normalized": True, "create_dw": False, "create_indices": False, "create_views": False, "create_triggers": False, "create_procedures": False, "delete_all": False, "all_steps": False},
        "5": {"create_main": True, "create_normalized": True, "create_dw": True, "create_indices": True, "create_views": True, "create_triggers": True, "create_procedures": True, "delete_all": False, "all_steps": True},
        "6": {"create_main": False, "create_normalized": False, "create_dw": False, "create_indices": True, "create_views": False, "create_triggers": False, "create_procedures": False, "delete_all": False, "all_steps": False},
        "7": {"create_main": False, "create_normalized": False, "create_dw": False, "create_indices": False, "create_views": True, "create_triggers": False, "create_procedures": False, "delete_all": False, "all_steps": False},
        "8": {"create_main": False, "create_normalized": False, "create_dw": False, "create_indices": False, "create_views": False, "create_triggers": True, "create_procedures": False, "delete_all": False, "all_steps": False},
        "9": {"create_main": False, "create_normalized": False, "create_dw": False, "create_indices": False, "create_views": False, "create_triggers": False, "create_procedures": True, "delete_all": False, "all_steps": False},
        "10": {"create_main": False, "create_normalized": False, "create_dw": False, "create_indices": False, "create_views": True, "create_triggers": True, "create_procedures": True, "delete_all": False, "all_steps": False},
        "11": {"create_main": False, "create_normalized": False, "create_dw": False, "create_indices": False, "create_views": False, "create_triggers": False, "create_procedures": False, "delete_all": True, "all_steps": False},
        "12": {"create_main": False, "create_normalized": False, "create_dw": False, "create_indices": False, "create_views": False, "create_triggers": False, "create_procedures": False, "delete_all": False, "all_steps": False},
    }

    return options[choice]


def execute_deletion() -> bool:
    """Executa a deleção de todas as tabelas e schemas."""
    print("\n" + "=" * 60)
    print("  LIMPEZA DO BANCO DE DADOS")
    print("=" * 60)
    print("\nATENCAO: Esta operacao vai deletar TODAS as tabelas e schemas!")
    print("\nSchemas que serao deletados:")
    print("  - Schema 'o' (tabela o.Tabelona)")
    print("  - Schema 'n' (todas as tabelas normalizadas)")
    print("  - Schema 'dw' (Data Warehouse)")
    print("\nEsta operacao NAO pode ser desfeita!")
    print()

    while True:
        try:
            confirmation = input("Digite 'DELETAR' para confirmar ou 'cancelar' para abortar: ").strip()
            if confirmation.upper() == "DELETAR":
                break
            elif confirmation.lower() == "cancelar":
                print("\nOperacao cancelada. Nenhuma alteracao foi feita.")
                return False
            else:
                print("Resposta invalida. Digite 'DELETAR' para confirmar ou 'cancelar' para abortar.")
        except (EOFError, KeyboardInterrupt):
            print("\nOperacao cancelada pelo usuario.")
            return False

    print("\nIniciando delecao...")
    success = True

    if not delete_module.delete_normalized_tables():
        success = False
    if not delete_module.delete_original_tables():
        success = False
    if not delete_module.delete_schemas():
        success = False

    print("\n" + "=" * 60)
    if success:
        logger.info("Limpeza concluida com sucesso")
        print("Limpeza do banco de dados concluida com sucesso!")
        print("Todos os schemas e tabelas foram deletados.")
    else:
        logger.error("Limpeza concluida com erros")
        print("Limpeza concluida com alguns erros. Verifique os logs.")
    print("=" * 60 + "\n")

    return success


def execute_creation(options: dict) -> bool:
    """Executa a criação de tabelas, índices e objetos."""
    if not options["create_main"] and not options["create_normalized"] and not options["create_dw"] and not options["create_indices"] and not options["create_views"] and not options["create_triggers"] and not options["create_procedures"]:
        return True

    success = True

    if options["all_steps"]:
        print("\n" + "=" * 60)
        print("  EXECUTANDO TODAS AS ETAPAS")
        print("=" * 60)

    if options["create_main"]:
        if options["all_steps"]:
            print("\n[ETAPA 1/7] Criando tabela original (o.Tabelona)...")
        else:
            print("\nCriando tabela original (o.Tabelona)...")
        
        ddl_path = os.path.join("scripts", "CSV 1 - 1000 partidas", "ScriptTabelaOriginal.sql")
        csv_path = os.path.join("data", "Sep-29-2022_500matches.csv")
        
        if not Path(csv_path).exists():
            logger.warning(f"Arquivo CSV não encontrado: {csv_path}")
            print(f"Aviso: Arquivo CSV não encontrado. Criando apenas a estrutura da tabela...")
            csv_path = None

        created = create_main.create_main_table(ddl_path)
        if created and csv_path and Path(csv_path).exists():
            print("Carregando dados do CSV...")
            loaded = create_main.load_csv_into_table(csv_path, truncate=False)
            if not loaded:
                success = False
                if options["all_steps"]:
                    print("\nErro ao carregar CSV. Abortando próximas etapas.")
                    print("=" * 60 + "\n")
                    return False
        elif not created:
            success = False
            if options["all_steps"]:
                print("\nErro ao criar tabela original. Abortando próximas etapas.")
                print("=" * 60 + "\n")
                return False

    if options["create_normalized"]:
        if options["all_steps"]:
            print("\n[ETAPA 2/7] Criando tabelas normalizadas (schema n)...")
        else:
            print("\nCriando tabelas normalizadas (schema n)...")
        
        ddl_path = os.path.join("scripts", "CSV 1 - 1000 partidas", "DDL1.sql")
        dml_path = os.path.join("scripts", "CSV 1 - 1000 partidas", "DML1.sql")
        
        created = create_normalize.create_normalized_tables(ddl_path)
        if created:
            print("Populando tabelas normalizadas...")
            populated = create_normalize.populate_normalized_tables(dml_path)
            if not populated:
                success = False
                if options["all_steps"]:
                    print("\nErro ao popular tabelas normalizadas. Abortando próximas etapas.")
                    print("=" * 60 + "\n")
                    return False
        else:
            success = False
            if options["all_steps"]:
                print("\nErro ao criar tabelas normalizadas. Abortando próximas etapas.")
                print("=" * 60 + "\n")
                return False

    if options["create_dw"]:
        if options["all_steps"]:
            print("\n[ETAPA 3/7] Criando Data Warehouse (schema dw)...")
        else:
            print("\nCriando Data Warehouse (schema dw)...")
        
        ddl_path = os.path.join("DW", "DDL.sql")
        dml_path = os.path.join("DW", "DML.sql")
        
        created = create_dw.create_dw_tables(ddl_path)
        if created:
            print("Populando Data Warehouse...")
            populated = create_dw.populate_dw_tables(dml_path)
            if not populated:
                success = False
                if options["all_steps"]:
                    print("\nErro ao popular Data Warehouse. Abortando próximas etapas.")
                    print("=" * 60 + "\n")
                    return False
        else:
            success = False
            if options["all_steps"]:
                print("\nErro ao criar Data Warehouse. Abortando próximas etapas.")
                print("=" * 60 + "\n")
                return False

    if options["create_indices"]:
        if options["all_steps"]:
            print("\n[ETAPA 4/7] Criando índices...")
        else:
            print("\nCriando índices...")
        
        indices_original = create_indices.create_original_table_indices()
        indices_normalized = create_indices.create_normalized_table_indices()
        
        if not indices_original or not indices_normalized:
            success = False
            if options["all_steps"]:
                print("\nErro ao criar índices. Continuando com próximas etapas...")

    if options["create_views"]:
        if options["all_steps"]:
            print("\n[ETAPA 5/7] Criando Views...")
        else:
            print("\nCriando Views...")
        
        views_path = os.path.join("objetos", "Views.sql")
        created = create_views.create_views(views_path)
        if not created:
            success = False
            if options["all_steps"]:
                print("\nErro ao criar Views. Continuando com próximas etapas...")

    if options["create_triggers"]:
        if options["all_steps"]:
            print("\n[ETAPA 6/7] Criando Triggers...")
        else:
            print("\nCriando Triggers...")
        
        triggers_path = os.path.join("objetos", "Triggers.sql")
        created = create_triggers.create_triggers(triggers_path)
        if not created:
            success = False
            if options["all_steps"]:
                print("\nErro ao criar Triggers. Continuando com próximas etapas...")

    if options["create_procedures"]:
        if options["all_steps"]:
            print("\n[ETAPA 7/7] Criando Procedures...")
        else:
            print("\nCriando Procedures...")
        
        procedures_path = os.path.join("objetos", "Procedure.sql")
        created = create_procedures.create_procedures(procedures_path)
        if not created:
            success = False
            if options["all_steps"]:
                print("\nErro ao criar Procedures. Continuando com próximas etapas...")

    return success


def main():
    """Função principal do script de inicialização."""
    if not check_database_connection():
        print("\nErro: Não foi possível conectar ao banco de dados.")
        print("Verifique se o container PostgreSQL está rodando.")
        sys.exit(1)

    options = ask_user_input()

    if options["delete_all"]:
        execute_deletion()
        return

    if not options["create_main"] and not options["create_normalized"] and not options["create_dw"] and not options["create_indices"] and not options["create_views"] and not options["create_triggers"] and not options["create_procedures"]:
        print("\nNenhuma operação selecionada. Saindo...")
        return

    success = execute_creation(options)

    print("\n" + "=" * 60)
    if success:
        logger.info("Operação concluída com sucesso")
        print("Operação concluída com sucesso!")
    else:
        logger.error("Operação concluída com erros")
        print("Operação concluída com alguns erros. Verifique os logs.")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()

