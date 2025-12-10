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
