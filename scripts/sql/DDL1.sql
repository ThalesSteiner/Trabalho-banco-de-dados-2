CREATE SCHEMA IF NOT EXISTS n;

-- O summonerId existe independente da partida.
CREATE TABLE n.ContaJogador (
    summonerId VARCHAR(100) PRIMARY KEY
);


-- O Campeao (Personagem do jogo) existe independente de quem joga.
CREATE TABLE n.Campeao (
    championID SERIAL PRIMARY KEY,
    championName VARCHAR(50) NOT NULL UNIQUE 
);


CREATE TABLE n.Partida (
    GameID VARCHAR(50) PRIMARY KEY,
    GameMode VARCHAR(10) NOT NULL CHECK (GameMode IN ('ARAM','CLASSIC')),
    timePlayed INT NOT NULL 
);



CREATE TABLE n.Time (
    GameID VARCHAR(50) NOT NULL,
    teamId INT NOT NULL CHECK (teamId IN (100,200)),
    win BOOLEAN,
    teamEarlySurrendered BOOLEAN,
    gameEndedInSurrender BOOLEAN,
    nexusLost INT CHECK (nexusLost IN (0,1)),
    inhibitorsLost INT CHECK (inhibitorsLost BETWEEN 0 AND 10),
    turretsLost INT,
    PRIMARY KEY (GameID, teamId),
    FOREIGN KEY (GameID) REFERENCES n.Partida(GameID)
);


-- Liga a Partida + O Jogador (Summoner) + O Personagem (Campeao)
CREATE TABLE n.Participacao (
    GameID VARCHAR(50) NOT NULL,
    summonerId VARCHAR(100) NOT NULL,
    championID INT NOT NULL,    
    teamId INT NOT NULL,    
    individualPosition VARCHAR(7) CHECK (individualPosition IN ('TOP','MIDDLE','BOTTOM','JUNGLE','UTILITY','Invalid')),
    lane VARCHAR(6) CHECK (lane IN ('TOP','MIDDLE','BOTTOM','JUNGLE','NONE')),
    PRIMARY KEY (GameID, summonerId),

    FOREIGN KEY (GameID, teamId) REFERENCES n.Time(GameID, teamId),
    FOREIGN KEY (summonerId) REFERENCES n.ContaJogador(summonerId), 
    FOREIGN KEY (championId) REFERENCES n.Campeao(championID) 
);



-- Detalhes da Build (O "Setup" do campeão naquela partida)
CREATE TABLE n.JogadorItem (
    GameID VARCHAR(50) NOT NULL,
    summonerId VARCHAR(100) NOT NULL,
    champLevel INT CHECK (champLevel BETWEEN 1 AND 18),
    champExperience INT CHECK (champExperience BETWEEN 0 AND 43518),
    item0 INT, item1 INT, item2 INT, item3 INT, item4 INT, item5 INT, item6 INT,
    summoner1Id INT, summoner2Id INT,
    summoner1Casts INT, summoner2Casts INT,
    spell1Casts INT, spell2Casts INT, spell3Casts INT, spell4Casts INT,

    PRIMARY KEY (GameID, summonerId),
    FOREIGN KEY (GameID, summonerId) REFERENCES n.Participacao(GameID, summonerId)
);

-- Estátiscas do Jogador na partida.
CREATE TABLE n.Stats_Jogador (
    GameID VARCHAR(50) NOT NULL,
    summonerId VARCHAR(100) NOT NULL,
    kills INT, deaths INT, assists INT,
    largestKillingSpree INT, largestCriticalStrike INT,
    firstBloodKill BOOLEAN, firstBloodAssist BOOLEAN,
    bountyLevel INT,
    totalDamageDealtToChampions INT, physicalDamageDealtToChampions INT, 
    magicDamageDealtToChampions INT, trueDamageDealtToChampions INT,
    totalDamageTaken INT, damageSelfMitigated INT,
    visionScore INT, wardsPlaced INT, wardsKilled INT,
    turretTakedowns INT, inhibitorKills INT, dragonKills INT, baronKills INT,
    goldEarned INT, goldSpent INT, totalMinionsKilled INT,
    totalTimeSpentDead INT,

    longestTimeSpentLiving INT,
    magicDamageTaken INT,
    timeCCingOthers INT,
    totalDamageShieldedOnTeammates INT,
    physicalDamageTaken INT,
    magicDamageTaken INT,
    trueDamageTaken INT,
    totalHeal INT,
    totalHealsOnTeammates INT,
    damageDealtToObjectives INT,
    visionWardsBoughtInGame INT,
    objectivesStolen INT,
    totalTimeCCDealt INT,
    
    PRIMARY KEY (GameID, summonerId),
    FOREIGN KEY (GameID, summonerId) REFERENCES n.Participacao(GameID, summonerId)
);
