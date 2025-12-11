INSERT INTO dw.dim_Campeao (championName)
SELECT DISTINCT championName 
FROM n.Campeao;



INSERT INTO dw.dim_Jogador (summonerId)
SELECT DISTINCT summonerId 
FROM n.ContaJogador;



INSERT INTO dw.dim_FaixaTempo (faixa_duracao, minutos_totais) VALUES
('Curta (< 20 min)', 20),
('Média (20 - 30 min)', 30),
('Longa (30 - 40 min)', 40),
('Muito Longa (> 40 min)', 999);



INSERT INTO dw.dim_DetalhesPartida (
    GameID, 
    sk_tempo, 
    modo_jogo, 
    lado_time, 
    resultado, 
    surrender
)
SELECT 
    t.GameID,
    dt.sk_tempo, 
    p.GameMode,
    CASE WHEN t.teamId = 100 THEN 'Azul' ELSE 'Vermelho' END,
    CASE WHEN t.win = TRUE THEN 'Vitoria' ELSE 'Derrota' END,
    CASE WHEN t.gameEndedInSurrender = TRUE THEN 'Sim' ELSE 'Nao' END
FROM n.Time t
JOIN n.Partida p ON t.GameID = p.GameID
JOIN dw.dim_FaixaTempo dt ON dt.sk_tempo = (
    SELECT sk_tempo 
    FROM dw.dim_FaixaTempo 
    WHERE (p.timePlayed / 60.0) <= minutos_totais 
    ORDER BY minutos_totais ASC 
    LIMIT 1
);



INSERT INTO dw.fato_Performance (
    sk_campeao, 
    sk_jogador, 
    sk_detalhes,
    qtd_kills, 
    qtd_deaths, 
    qtd_assists, 
    kda_ratio, 
    ouro_ganho, 
    ouro_gasto, 
    minions_abatidos, 
    dano_total_campeoes, 
    dano_objetivos, 
    dano_recebido, 
    dano_mitigado, 
    placar_visao, 
    wards_colocadas, 
    tempo_cc_aplicado
)
SELECT
    dc.sk_campeao,
    dj.sk_jogador,
    dd.sk_detalhes,
    s.kills,
    s.deaths,
    s.assists,
    CASE 
        WHEN s.deaths = 0 THEN (s.kills + s.assists)::NUMERIC 
        ELSE ROUND((s.kills + s.assists)::NUMERIC / s.deaths, 2) 
    END,
    s.goldEarned,
    s.goldSpent,
    s.totalMinionsKilled,
    s.totalDamageDealtToChampions,
    s.damageDealtToObjectives,
    s.totalDamageTaken,
    s.damageSelfMitigated,
    s.visionScore,
    s.wardsPlaced,
    s.totalTimeCCDealt

FROM n.Participacao p
JOIN n.Stats_Jogador s ON p.GameID = s.GameID AND p.summonerId = s.summonerId
JOIN n.Partida part ON p.GameID = part.GameID
JOIN n.Campeao camp ON p.championID = camp.championID
JOIN dw.dim_Campeao dc ON camp.championName = dc.championName
JOIN dw.dim_Jogador dj ON p.summonerId = dj.summonerId
JOIN dw.dim_DetalhesPartida dd ON p.GameID = dd.GameID 
    AND (CASE WHEN p.teamId = 100 THEN 'Azul' ELSE 'Vermelho' END) = dd.lado_time;  