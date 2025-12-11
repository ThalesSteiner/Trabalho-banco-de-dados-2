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
    resultado VARCHAR(10),
    surrender VARCHAR(3)
);


CREATE TABLE dw.fato_Performance (
    id_fato SERIAL PRIMARY KEY,
    sk_campeao INT REFERENCES dw.dim_Campeao(sk_campeao),
    sk_jogador INT REFERENCES dw.dim_Jogador(sk_jogador),
    sk_detalhes INT REFERENCES dw.dim_DetalhesPartida(sk_detalhes),
    qtd_kills INT,
    qtd_deaths INT,
    qtd_assists INT,
    kda_ratio NUMERIC(10,2),
    ouro_ganho INT,
    ouro_gasto INT,
    minions_abatidos INT,
    dano_total_campeoes INT,
    dano_objetivos INT,
    dano_recebido INT,
    dano_mitigado INT,
    placar_visao INT,
    wards_colocadas INT,
    tempo_cc_aplicado INT
);