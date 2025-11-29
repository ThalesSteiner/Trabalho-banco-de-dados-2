-- Script de inicialização do banco de dados PostgreSQL

\c banco_dados

-- Criar extensões úteis
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

CREATE SCHEMA IF NOT EXISTS public;

-- Definir permissões padrão no schema public
GRANT ALL PRIVILEGES ON SCHEMA public TO postgres;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO postgres;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO postgres;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON FUNCTIONS TO postgres;

-- Mensagem de confirmação
DO $$
BEGIN
    RAISE NOTICE '========================================';
    RAISE NOTICE 'Banco de dados inicializado com sucesso!';
    RAISE NOTICE '========================================';
END $$;

