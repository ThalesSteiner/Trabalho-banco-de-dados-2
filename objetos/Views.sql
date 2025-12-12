/* 
View que demonstra quais campeões(personagens) tem a maior % de vitória
Pedro Favato 
*/
CREATE OR REPLACE VIEW n.vw_Campeoes_winrate AS
SELECT 
    c.championName AS Campeao,
    COUNT(p.GameID) AS Total_Partidas,
    SUM(CASE WHEN t.win = TRUE THEN 1 ELSE 0 END) AS Total_Vitorias,
    ROUND((SUM(CASE WHEN t.win = TRUE THEN 1 ELSE 0 END)::NUMERIC / COUNT(p.GameID)) * 100, 2) AS Win_Rate_Porcentagem
FROM 
    n.Participacao p
    JOIN n.Campeao c ON p.championID = c.championID
    JOIN n.Time t ON p.GameID = t.GameID AND p.teamId = t.teamId
GROUP BY 
    c.championName
HAVING 
    COUNT(p.GameID) > 5
ORDER BY 
    Win_Rate_Porcentagem DESC; 


/* View que demonstra os campeões mais dificeis/chatos de se jogar contra (vitorias por desistência)
por Daniel da Costa */

create or replace view n.campeoeschatos as 
select championName as "Campeão", count (championName) as "vitórias por desistência" from n.Time
INNER join n.Participacao on n.Participacao.GameID = n.Time.GameID 
INNER join n.Campeao on n.Participacao.championId = n.Campeao.championId 
WHERE gameEndedInSurrender = TRUE and win = TRUE
group by championName
order by count(championName) desc;

/* View para facilitar a consulta mostrando um placar detalhado dos jogadores
por Iuri Sajnin */

CREATE OR REPLACE VIEW n.vw_Placar_Detalhado AS
SELECT 
    p.GameID,
    t.win AS Vitoria,
    c.championName AS Campeao,
    p.individualPosition AS Rota,
    s.kills,
    s.deaths,
    s.assists,
    s.totalDamageDealtToChampions AS Dano_Em_Campeoes 
FROM n.Participacao p
JOIN n.Stats_Jogador s ON p.GameID = s.GameID AND p.summonerId = s.summonerId
JOIN n.Campeao c ON p.championID = c.championID
JOIN n.Time t ON p.GameID = t.GameID AND p.teamId = t.teamId;

/* View que demonstra estatísticas consolidadas de performance por rota/posição
   Inclui métricas de combate, economia, visão e eficiência
   Feito por Thales Steiner */
CREATE OR REPLACE VIEW n.vw_Estatisticas_Por_Rota AS
SELECT 
    p.individualPosition AS Rota,
    COUNT(DISTINCT p.GameID) AS Total_Partidas,
    COUNT(DISTINCT p.summonerId) AS Total_Jogadores_Unicos,
    ROUND(AVG(CASE WHEN s.deaths = 0 THEN (s.kills + s.assists)::NUMERIC 
                   ELSE (s.kills + s.assists)::NUMERIC / NULLIF(s.deaths, 0) END), 2) AS KDA_Medio,
    ROUND(AVG(s.kills), 2) AS Kills_Medio,
    ROUND(AVG(s.deaths), 2) AS Deaths_Medio,
    ROUND(AVG(s.assists), 2) AS Assists_Medio,
    ROUND(AVG(s.goldEarned), 0) AS Ouro_Ganho_Medio,
    ROUND(AVG(s.goldSpent), 0) AS Ouro_Gasto_Medio,
    ROUND(AVG(s.totalDamageDealtToChampions), 0) AS Dano_Medio_Campeoes,
    ROUND(AVG(s.totalDamageTaken), 0) AS Dano_Recebido_Medio,
    ROUND(AVG(s.visionScore), 2) AS Visao_Media,
    ROUND(AVG(s.wardsPlaced), 2) AS Wards_Colocadas_Media,
    ROUND(AVG(s.totalMinionsKilled), 2) AS CS_Medio,
    ROUND(SUM(CASE WHEN t.win = TRUE THEN 1 ELSE 0 END)::NUMERIC / COUNT(*) * 100, 2) AS Taxa_Vitoria_Porcentagem
FROM n.Participacao p
JOIN n.Stats_Jogador s ON p.GameID = s.GameID AND p.summonerId = s.summonerId
JOIN n.Time t ON p.GameID = t.GameID AND p.teamId = t.teamId
GROUP BY p.individualPosition
ORDER BY KDA_Medio DESC;