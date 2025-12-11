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


/* TRIGGER que verifica se o insert em jogadoritem em experiencia é maior que o máximo,
se for, o usuário está trapaceado
por Daniel da Costa */
CREATE OR REPLACE FUNCTION n.verfexperiencia()
RETURNS TRIGGER AS $$
begin
    if new.champExperience > 43518 then
      raise exception 'Jogador possui mais experiencia que o limite, ele está trapaceado';
      return old;
    else
      return new;
    end if;

end;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER verificarsepodeExperiencia
BEFORE INSERT ON n.JogadorItem
FOR EACH ROW
EXECUTE FUNCTION n.verfexperiencia();


/* TRIGGER para validar se aconteceu remake na partida ou não (partidas com menos de 230 segundos não são válidas)
por Iuri Sajnin */
CREATE OR REPLACE FUNCTION n.trg_Validar_Tempo_Jogo()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.timePlayed < 230 THEN
        RAISE EXCEPTION 'Erro de Inserção: Partidas que aconteceu o remake não são permitidas para análise.';
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_Check_Remake
BEFORE INSERT ON n.Partida
FOR EACH ROW
EXECUTE FUNCTION n.trg_Validar_Tempo_Jogo();
