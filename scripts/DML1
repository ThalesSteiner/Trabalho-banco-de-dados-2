INSERT INTO n.ContaJogador (summonerId)
SELECT DISTINCT summonerId 
FROM o.Tabelona;


INSERT INTO n.Campeao (championName)
SELECT DISTINCT championName 
FROM o.Tabelona;


INSERT INTO n.Partida (GameID, GameMode, timePlayed)
SELECT DISTINCT GameID, GameMode, timePlayed
FROM o.Tabelona;


INSERT INTO n.Time (GameID, teamId, win, teamEarlySurrendered, gameEndedInSurrender, nexusLost, inhibitorsLost, turretsLost)
SELECT DISTINCT 
    GameID, teamId, win, teamEarlySurrendered, gameEndedInSurrender, nexusLost, inhibitorsLost, turretsLost
FROM o.Tabelona;


INSERT INTO n.Participacao (GameID, summonerId, championID, teamId, individualPosition, lane)
SELECT 
    t.GameID, 
    t.summonerId, 
    c.championID, 
    t.teamId, 
    t.individualPosition, 
    t.lane
FROM o.Tabelona t
JOIN n.Campeao c ON t.championName = c.championName;


INSERT INTO n.JogadorItem (
    GameID, summonerId, champLevel, champExperience, 
    item0, item1, item2, item3, item4, item5, item6, 
    summoner1Id, summoner2Id, summoner1Casts, summoner2Casts, 
    spell1Casts, spell2Casts, spell3Casts, spell4Casts
)
SELECT 
    GameID, summonerId, champLevel, champExperience, 
    item0, item1, item2, item3, item4, item5, item6, 
    summoner1Id, summoner2Id, summoner1Casts, summoner2Casts, 
    spell1Casts, spell2Casts, spell3Casts, spell4Casts
FROM o.Tabelona;


INSERT INTO n.Stats_Jogador (
    GameID, summonerId, kills, deaths, assists, 
    largestKillingSpree, largestCriticalStrike, firstBloodKill, firstBloodAssist, bountyLevel, 
    totalDamageDealtToChampions, physicalDamageDealtToChampions, magicDamageDealtToChampions, trueDamageDealtToChampions, 
    totalDamageTaken, damageSelfMitigated, visionScore, wardsPlaced, wardsKilled, 
    turretTakedowns, inhibitorKills, dragonKills, baronKills, 
    goldEarned, goldSpent, totalMinionsKilled, totalTimeSpentDead
)
SELECT 
    GameID, summonerId, kills, deaths, assists, 
    largestKillingSpree, largestCriticalStrike, firstBloodKill, firstBloodAssist, bountyLevel, 
    totalDamageDealtToChampions, physicalDamageDealtToChampions, magicDamageDealtToChampions, trueDamageDealtToChampions, 
    totalDamageTaken, damageSelfMitigated, visionScore, wardsPlaced, wardsKilled, 
    turretTakedowns, inhibitorKills, dragonKills, baronKills, 
    goldEarned, goldSpent, totalMinionsKilled, totalTimeSpentDead
FROM o.Tabelona;