-- Quais campeões possuem a maior taxa de vitória em partidas longas?
SELECT 
    c.championName AS Campeao,
    COUNT(f.id_fato) AS Total_Jogos,

    SUM(CASE WHEN d.resultado = 'Vitoria' THEN 1 ELSE 0 END) AS Vitorias,
    
    ROUND(
        (SUM(CASE WHEN d.resultado = 'Vitoria' THEN 1.0 ELSE 0.0 END) / COUNT(f.id_fato)) * 100, 
        2
    ) AS Win_Rate_Porcentagem

FROM dw.fato_Performance f
JOIN dw.dim_Campeao c ON f.sk_campeao = c.sk_campeao
JOIN dw.dim_DetalhesPartida d ON f.sk_detalhes = d.sk_detalhes
JOIN dw.dim_FaixaTempo t ON d.sk_tempo = t.sk_tempo
WHERE t.faixa_duracao IN ('Longa (30 - 40 min)', 'Muito Longa (> 40 min)')

GROUP BY c.championName
HAVING COUNT(f.id_fato) >= 10
ORDER BY Win_Rate_Porcentagem DESC
LIMIT 10;




--Existe uma vantagem estatística para o Time Azul?
SELECT 
    d.lado_time AS Lado_do_Mapa,
    COUNT(DISTINCT d.GameID) AS Total_Partidas,
    COUNT(DISTINCT CASE WHEN d.resultado = 'Vitoria' THEN d.GameID END) AS Partidas_Vencidas,
    ROUND(
        (COUNT(DISTINCT CASE WHEN d.resultado = 'Vitoria' THEN d.GameID END)::NUMERIC / 
         COUNT(DISTINCT d.GameID)) * 100, 
        2
    ) AS Taxa_Vitoria

FROM dw.fato_Performance f
JOIN dw.dim_DetalhesPartida d ON f.sk_detalhes = d.sk_detalhes

WHERE d.modo_jogo = 'CLASSIC'
GROUP BY d.lado_time
ORDER BY Taxa_Vitoria DESC;


--Qual a relação entre o ouro acumulado e a quantidade de wards colocadas?
SELECT 
    ROUND(f.ouro_ganho / 2000) * 2000 AS Faixa_de_Ouro,
    
    ROUND(AVG(f.wards_colocadas), 2) AS Media_Wards,
    COUNT(*) AS Qtd_Jogadores

FROM dw.fato_Performance f
JOIN dw.dim_DetalhesPartida d ON f.sk_detalhes = d.sk_detalhes

WHERE f.ouro_ganho > 0 
  AND d.modo_jogo = 'CLASSIC'
GROUP BY 1
ORDER BY 1;


