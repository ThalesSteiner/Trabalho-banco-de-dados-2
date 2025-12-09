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
