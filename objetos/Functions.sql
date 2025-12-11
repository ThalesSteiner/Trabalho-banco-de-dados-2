/* 
Function para calcular o KDA(kills, deaths, assists) do player na partida.
Pedro Favato 
*/

CREATE OR REPLACE FUNCTION n.fn_calcular_kda(kills INT, deaths INT, assists INT)
RETURNS NUMERIC(10, 2) AS $$
BEGIN
    IF deaths = 0 THEN
        RETURN (kills + assists)::NUMERIC;
    ELSE
        RETURN ROUND(((kills + assists)::NUMERIC / deaths), 2);
    END IF;
END;
$$ LANGUAGE plpgsql;



/* function que calcula a média de kills por minuto de um jogador em uma partida
por Daniel da Costa */

create or replace function n.abatespormin(kills int, tempodejogototalsegs int, tempogastomortosegs int)
returns numeric(10,2) as $$
declare 
mediafinal numeric(10,2);
tempovivo numeric(10,2);
begin
    tempovivo := tempodejogototalsegs - tempogastomortosegs;
    IF tempovivo <= 0 then
      RAISE EXCEPTION 'Jogador passou o jogo inteiro morto!';
      return 0;
    else
      mediafinal := (kills) / (tempovivo/60);
      return mediafinal;
    end if;
end;
$$ LANGUAGE plpgsql;


/*function que analisa o desempenho de um jogador em uma partida baseado no KDA e retorna uma classificação 
por Iuri Sajnin */

CREATE OR REPLACE FUNCTION n.fn_Classificar_Performance(p_GameID VARCHAR, p_SummonerID VARCHAR)
RETURNS VARCHAR AS $$
DECLARE
    v_kills INT;
    v_deaths INT;
    v_assists INT;
    v_kda NUMERIC;
    v_resultado VARCHAR(50);
BEGIN
    SELECT kills, deaths, assists 
    INTO v_kills, v_deaths, v_assists
    FROM n.Stats_Jogador
    WHERE GameID = p_GameID AND summonerId = p_SummonerID;
    IF v_kills IS NULL THEN
        RETURN 'Jogador ou Partida não encontrados';
    END IF;
    IF v_deaths = 0 THEN
        v_kda := (v_kills + v_assists); 
        v_resultado := 'PERFECT KDA (Imortal)';
    ELSE
        v_kda := (v_kills + v_assists)::NUMERIC / v_deaths;
        IF v_kda >= 10 THEN
            v_resultado := 'Rank S+ (Lendário)';
        ELSIF v_kda >= 5 THEN
            v_resultado := 'Rank A (Carregou a partida)';
        ELSIF v_kda >= 3 THEN
            v_resultado := 'Rank B (Bom)';
        ELSIF v_kda >= 1.5 THEN
            v_resultado := 'Rank C (Na Média)';
        ELSIF v_kda >= 0.5 THEN
             v_resultado := 'Rank D (Quase trollou...)';
        ELSE
             v_resultado := 'Rank F (Feedou?)';
        END IF;
    END IF;
    RETURN v_resultado;
END;
$$ LANGUAGE plpgsql;