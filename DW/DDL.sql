CREATE SCHEMA IF NOT EXISTS dw;


CREATE TABLE dw.dim_Campeao (
    sk_campeao SERIAL PRIMARY KEY,
    championName VARCHAR(50)
);

CREATE TABLE dw.dim_Jogador (
    sk_jogador SERIAL PRIMARY KEY,
    summonerId VARCHAR(100)
);

CREATE TABLE dw.dim_FaixaTempo (
    sk_tempo SERIAL PRIMARY KEY,
    faixa_duracao VARCHAR(50),
    minutos_totais INT
);

CREATE TABLE dw.dim_DetalhesPartida (
    sk_detalhes SERIAL PRIMARY KEY,
    sk_tempo INT REFERENCES dw.dim_FaixaTempo(sk_tempo),
    GameID VARCHAR(50),
    modo_jogo VARCHAR(20),
    lado_time VARCHAR(10),