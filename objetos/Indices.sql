/*
Script para criar índices nas tabelas do banco de dados.
Melhora a performance de consultas e joins.
*/

-- Índices para a tabela original o.Tabelona
CREATE INDEX IF NOT EXISTS idx_tabelona_gameid ON o.Tabelona(GameID);
CREATE INDEX IF NOT EXISTS idx_tabelona_summonerid ON o.Tabelona(summonerId);
CREATE INDEX IF NOT EXISTS idx_tabelona_championname ON o.Tabelona(championName);
CREATE INDEX IF NOT EXISTS idx_tabelona_gamemode ON o.Tabelona(GameMode);
CREATE INDEX IF NOT EXISTS idx_tabelona_win ON o.Tabelona(win);
CREATE INDEX IF NOT EXISTS idx_tabelona_teamid ON o.Tabelona(teamId);
CREATE INDEX IF NOT EXISTS idx_tabelona_position ON o.Tabelona(individualPosition);
CREATE INDEX IF NOT EXISTS idx_tabelona_lane ON o.Tabelona(lane);

-- Índices para as tabelas normalizadas (schema n)

-- n.Partida
CREATE INDEX IF NOT EXISTS idx_partida_gamemode ON n.Partida(GameMode);

-- n.Time
CREATE INDEX IF NOT EXISTS idx_time_gameid ON n.Time(GameID);
CREATE INDEX IF NOT EXISTS idx_time_win ON n.Time(win);

-- n.Participacao
CREATE INDEX IF NOT EXISTS idx_participacao_championid ON n.Participacao(championID);
CREATE INDEX IF NOT EXISTS idx_participacao_summonerid ON n.Participacao(summonerId);
CREATE INDEX IF NOT EXISTS idx_participacao_position ON n.Participacao(individualPosition);
CREATE INDEX IF NOT EXISTS idx_participacao_lane ON n.Participacao(lane);
CREATE INDEX IF NOT EXISTS idx_participacao_teamid ON n.Participacao(teamId);

-- n.Stats_Jogador
CREATE INDEX IF NOT EXISTS idx_stats_kills ON n.Stats_Jogador(kills);
CREATE INDEX IF NOT EXISTS idx_stats_deaths ON n.Stats_Jogador(deaths);
CREATE INDEX IF NOT EXISTS idx_stats_goldearned ON n.Stats_Jogador(goldEarned);
CREATE INDEX IF NOT EXISTS idx_stats_damage ON n.Stats_Jogador(totalDamageDealtToChampions);
CREATE INDEX IF NOT EXISTS idx_stats_visionscore ON n.Stats_Jogador(visionScore);

-- Índices específicos para otimização das Views

-- Índice para a view n.vw_Campeoes_winrate
CREATE INDEX IF NOT EXISTS idx_view_campeoes_winrate_time ON n.Time(GameID, teamId, win);

-- Índice para a view n.campeoeschatos
CREATE INDEX IF NOT EXISTS idx_view_campeoeschatos_time ON n.Time(GameID, gameEndedInSurrender, win);
CREATE INDEX IF NOT EXISTS idx_view_campeoeschatos_participacao ON n.Participacao(GameID, championID);

-- Índice para a view n.vw_Placar_Detalhado
CREATE INDEX IF NOT EXISTS idx_view_placar_stats ON n.Stats_Jogador(GameID, summonerId);
CREATE INDEX IF NOT EXISTS idx_view_placar_time ON n.Time(GameID, teamId, win);
CREATE INDEX IF NOT EXISTS idx_view_placar_campeao ON n.Participacao(championID, GameID, individualPosition);

-- Índice para a view n.vw_Estatisticas_Por_Rota
CREATE INDEX IF NOT EXISTS idx_view_estatisticas_rota_participacao ON n.Participacao(individualPosition, GameID, summonerId, teamId);
CREATE INDEX IF NOT EXISTS idx_view_estatisticas_rota_stats ON n.Stats_Jogador(GameID, summonerId);
CREATE INDEX IF NOT EXISTS idx_view_estatisticas_rota_time ON n.Time(GameID, teamId, win);

