/*
Trigger para validar o tempo que o jogador vai inserir o momento em que matarm o Baron(Monstro no jogo)
Pedro Favato
*/
CREATE OR REPLACE FUNCTION n.fn_validar_tempo_baron()
RETURNS TRIGGER AS $$
DECLARE
    v_duracao_partida INT;
BEGIN
    SELECT timePlayed INTO v_duracao_partida
    FROM n.Partida
    WHERE GameID = NEW.GameID;
    IF v_duracao_partida < 1200 AND NEW.baronKills > 0 THEN
        RAISE EXCEPTION 'Erro: Jogador % registrou morte de Barão em partida de % segundos (Barão nasce apenas aos 1200s).', NEW.summonerId, v_duracao_partida;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_impedir_baron_prematuro
BEFORE INSERT OR UPDATE ON n.Stats_Jogador
FOR EACH ROW
EXECUTE FUNCTION n.fn_validar_tempo_baron();