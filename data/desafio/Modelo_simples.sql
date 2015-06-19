CREATE TABLE Tournament (
 TournamentCode INT NOT NULL PRIMARY KEY,
 GameName CHAR(50),
 RefYear INT,
 Country CHAR(20)
);


CREATE TABLE Player (
 PlayerCode INT NOT NULL,
 TournamentCode INT NOT NULL,
 PlayerName CHAR(80),
 PlayerId CHAR(10),
 FU CHAR(15),

 PRIMARY KEY (PlayerCode,TournamentCode),

 FOREIGN KEY (TournamentCode) REFERENCES Tournament (TournamentCode)
);


CREATE TABLE Series (
 TournamentCode INT NOT NULL,
 SeriesCode INT NOT NULL,
 SeriesOrder INT,

 PRIMARY KEY (TournamentCode,SeriesCode),

 FOREIGN KEY (TournamentCode) REFERENCES Tournament (TournamentCode)
);


CREATE TABLE Game (
 TournamentCode INT NOT NULL,
 SeriesCode INT NOT NULL,
 GroupCode INT NOT NULL,

 PRIMARY KEY (TournamentCode,SeriesCode,GroupCode),

 FOREIGN KEY (TournamentCode,SeriesCode) REFERENCES Series (TournamentCode,SeriesCode),
 FOREIGN KEY (TournamentCode) REFERENCES Tournament (TournamentCode)
);


CREATE TABLE GameRound (
 RoundCode INT NOT NULL,
 TournamentCode INT NOT NULL,
 SeriesCode INT NOT NULL,
 GroupCode INT NOT NULL,
 RoundOrder INT,

 PRIMARY KEY (RoundCode,TournamentCode,SeriesCode,GroupCode),

 FOREIGN KEY (TournamentCode,SeriesCode,GroupCode) REFERENCES Game (TournamentCode,SeriesCode,GroupCode)
);


CREATE TABLE Enrollment (
 PlayerCode INT NOT NULL,
 TournamentCode INT NOT NULL,
 GroupCode INT NOT NULL,
 SeriesCode INT NOT NULL,
 FinalScore REAL,

 PRIMARY KEY (PlayerCode,TournamentCode,GroupCode,SeriesCode),

 FOREIGN KEY (PlayerCode,TournamentCode) REFERENCES Player (PlayerCode,TournamentCode),
 FOREIGN KEY (TournamentCode,SeriesCode,GroupCode) REFERENCES Game (TournamentCode,SeriesCode,GroupCode)
);


CREATE TABLE GameRoundResult (
 RoundCode INT NOT NULL,
 TournamentCode INT NOT NULL,
 SeriesCode INT NOT NULL,
 GroupCode INT NOT NULL,
 PlayerCode INT NOT NULL,
 RoundScore REAL,
 TotalScore REAL,
 PlayerRoundStatus INT,

 PRIMARY KEY (RoundCode,TournamentCode,SeriesCode,GroupCode,PlayerCode),

 FOREIGN KEY (RoundCode,TournamentCode,SeriesCode,GroupCode) REFERENCES GameRound (RoundCode,TournamentCode,SeriesCode,GroupCode),
 FOREIGN KEY (PlayerCode,TournamentCode,SeriesCode,GroupCode) REFERENCES Enrollment (PlayerCode,TournamentCode,SeriesCode,GroupCode)
);


