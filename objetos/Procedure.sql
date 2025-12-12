/*
Procedure que automatiza a exclusao de uma partida completa
Pedro Favato
*/

CREATE OR REPLACE PROCEDURE n.excluir_partida_completa(p_GameID VARCHAR)
LANGUAGE plpgsql
AS $$
BEGIN

    DELETE FROM n.Stats_Jogador WHERE GameID = p_GameID;    
    DELETE FROM n.JogadorItem WHERE GameID = p_GameID;
    DELETE FROM n.Participacao WHERE GameID = p_GameID;
    DELETE FROM n.Time WHERE GameID = p_GameID;
    DELETE FROM n.Partida WHERE GameID = p_GameID;
    
    RAISE NOTICE 'Partida % e todos os seus dados vinculados foram excluídos com sucesso.', p_GameID;

END;
$$;


/* procedure que muda o championLevel e o champExperience, baseado só nas pk
por Daniel da Costa */

create or replace procedure n.defchampExperienceELevel( p_GameID VARCHAR, p_summonerID VARCHAR)
as $$
declare 
p_champExperience int;
levelparaAlterar int;
begin
  
  select champExperience into p_champExperience 
  from n.JogadorItem
  where GameID = p_GameID and summonerId = p_summonerID;
  
  if p_champExperience >= 18360 then 
    levelparaAlterar := 18;
  elsif p_champExperience >= 16480 then 
    levelparaAlterar := 17;
  elsif p_champExperience >= 14700 then 
    levelparaAlterar := 16;
  elsif p_champExperience >= 13020 then 
    levelparaAlterar := 15;
  elsif p_champExperience >= 11440 then 
    levelparaAlterar := 14;
  elsif p_champExperience >= 9960 then 
    levelparaAlterar := 13;
  elsif p_champExperience >= 8580 then 
    levelparaAlterar := 12;
  elsif p_champExperience >= 7300 then 
    levelparaAlterar := 11;
  elsif p_champExperience >= 6120 then 
    levelparaAlterar := 10;
  elsif p_champExperience >= 5040 then 
    levelparaAlterar := 9;
  elsif p_champExperience >= 4060 then 
    levelparaAlterar := 8;
  elsif p_champExperience >= 3180 then 
    levelparaAlterar := 7;
  elsif p_champExperience >= 2400 then 
    levelparaAlterar := 6;
  elsif p_champExperience >= 1720 then 
    levelparaAlterar := 5;
  elsif p_champExperience >= 1140 then 
    levelparaAlterar := 4;
  elsif p_champExperience >= 660 then 
    levelparaAlterar := 3;
    elsif p_champExperience >= 280 then 
    levelparaAlterar := 2;
  else
    levelparaAlterar := 1;
  end if;
  
  update n.JogadorItem set champLevel = levelparaAlterar 
  where GameID = p_GameID and summonerId = p_summonerID;
end;
$$ LANGUAGE plpgsql;


/*Procedure para verificar se a partida foi balanceada ou não
por Iuri Sajnin */
CREATE OR REPLACE PROCEDURE n.sp_Verificar_Partida(p_GameID VARCHAR)
LANGUAGE plpgsql
AS $$
DECLARE
    v_gold_blue  INT;
    v_gold_red   INT;
    v_kills_blue INT;
    v_kills_red  INT;
    v_diff_gold_perc NUMERIC;
    v_total_kills INT;
    v_veredito VARCHAR(100);
BEGIN
    SELECT 
        SUM(CASE WHEN p.teamId = 100 THEN s.goldEarned ELSE 0 END),
        SUM(CASE WHEN p.teamId = 200 THEN s.goldEarned ELSE 0 END),
        SUM(CASE WHEN p.teamId = 100 THEN s.kills ELSE 0 END),
        SUM(CASE WHEN p.teamId = 200 THEN s.kills ELSE 0 END)
    INTO v_gold_blue, v_gold_red, v_kills_blue, v_kills_red
    FROM n.Stats_Jogador s
    JOIN n.Participacao p ON s.GameID = p.GameID AND s.summonerId = p.summonerId
    WHERE s.GameID = p_GameID;
    IF v_gold_blue IS NULL THEN
        RAISE NOTICE 'Partida % não encontrada', p_GameID;
        RETURN;
    END IF;
    v_diff_gold_perc := ABS(v_gold_blue - v_gold_red)::NUMERIC / NULLIF((v_gold_blue + v_gold_red), 0) * 100;
    v_total_kills := v_kills_blue + v_kills_red;
    IF v_diff_gold_perc < 5 THEN
        v_veredito := 'Partida Equilibrada (Diferença de ouro < 5%)';
    ELSIF v_diff_gold_perc > 20 THEN
        v_veredito := 'ATROPELO! (Um time stompou o outro)';
    ELSIF v_total_kills > 80 THEN
        v_veredito := 'Jogo de "bronze" (Muitas mortes)';
    ELSE
        v_veredito := 'Jogo Competitivo (Vantagem moderada)';
    END IF;
    RAISE NOTICE 'AUDITORIA DA PARTIDA: %', p_GameID;
    RAISE NOTICE 'Ouro Time Azul (100): % | Kills: %', v_gold_blue, v_kills_blue;
    RAISE NOTICE 'Ouro Time Vermelho (200): % | Kills: %', v_gold_red, v_kills_red;
    RAISE NOTICE 'VEREDITO FINAL: %', v_veredito;
END;
$$;


/* Procedure para exibir estatísticas resumidas de um jogador
   Mostra total de partidas, vitórias, derrotas, KDA médio e outras métricas
   Feito por Thales Steiner */
CREATE OR REPLACE PROCEDURE n.sp_Estatisticas_Jogador(p_SummonerID VARCHAR)
LANGUAGE plpgsql
AS $$
DECLARE
    v_total_partidas INT;
    v_total_vitorias INT;
    v_total_derrotas INT;
    v_taxa_vitoria NUMERIC;
    v_kda_medio NUMERIC;
    v_kills_total INT;
    v_deaths_total INT;
    v_assists_total INT;
    v_ouro_medio NUMERIC;
    v_dano_medio NUMERIC;
    v_visao_media NUMERIC;
BEGIN
    IF NOT EXISTS (SELECT 1 FROM n.ContaJogador WHERE summonerId = p_SummonerID) THEN
        RAISE NOTICE 'Jogador % não encontrado no banco de dados.', p_SummonerID;
        RETURN;
    END IF;
    SELECT 
        COUNT(DISTINCT p.GameID),
        SUM(CASE WHEN t.win = TRUE THEN 1 ELSE 0 END),
        SUM(CASE WHEN t.win = FALSE THEN 1 ELSE 0 END)
    INTO v_total_partidas, v_total_vitorias, v_total_derrotas
    FROM n.Participacao p
    JOIN n.Time t ON p.GameID = t.GameID AND p.teamId = t.teamId
    WHERE p.summonerId = p_SummonerID;
    
    IF v_total_partidas = 0 THEN
        RAISE NOTICE 'Jogador % não possui partidas registradas.', p_SummonerID;
        RETURN;
    END IF;
    v_taxa_vitoria := ROUND((v_total_vitorias::NUMERIC / v_total_partidas) * 100, 2);
    SELECT 
        ROUND(AVG(CASE WHEN s.deaths = 0 THEN (s.kills + s.assists)::NUMERIC 
                       ELSE (s.kills + s.assists)::NUMERIC / NULLIF(s.deaths, 0) END), 2),
        SUM(s.kills),
        SUM(s.deaths),
        SUM(s.assists),
        ROUND(AVG(s.goldEarned), 0),
        ROUND(AVG(s.totalDamageDealtToChampions), 0),
        ROUND(AVG(s.visionScore), 2)
    INTO v_kda_medio, v_kills_total, v_deaths_total, v_assists_total, 
         v_ouro_medio, v_dano_medio, v_visao_media
    FROM n.Stats_Jogador s
    JOIN n.Participacao p ON s.GameID = p.GameID AND s.summonerId = p.summonerId
    WHERE s.summonerId = p_SummonerID;
    RAISE NOTICE '========================================';
    RAISE NOTICE 'ESTATÍSTICAS DO JOGADOR: %', p_SummonerID;
    RAISE NOTICE '========================================';
    RAISE NOTICE 'Total de Partidas: %', v_total_partidas;
    RAISE NOTICE 'Vitórias: % | Derrotas: %', v_total_vitorias, v_total_derrotas;
    RAISE NOTICE 'Taxa de Vitória: %', v_taxa_vitoria || '%';
    RAISE NOTICE '----------------------------------------';
    RAISE NOTICE 'KDA Médio: %', v_kda_medio;
    RAISE NOTICE 'Total de Kills: % | Deaths: % | Assists: %', v_kills_total, v_deaths_total, v_assists_total;
    RAISE NOTICE '----------------------------------------';
    RAISE NOTICE 'Ouro Médio por Partida: %', v_ouro_medio;
    RAISE NOTICE 'Dano Médio a Campeões: %', v_dano_medio;
    RAISE NOTICE 'Visão Média: %', v_visao_media;
    RAISE NOTICE '========================================';
END;
$$;
