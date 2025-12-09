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