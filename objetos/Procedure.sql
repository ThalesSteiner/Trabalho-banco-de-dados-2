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