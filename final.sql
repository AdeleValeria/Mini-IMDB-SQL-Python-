/**
CREATE TABLE name_basics
(
	nconst VARCHAR (10),
	primaryName VARCHAR (500),
	birthYear INT,
	deathYear INT,
	primaryProfession VARCHAR (80),
	knownFortitles VARCHAR (80),
	PRIMARY KEY (nconst)
);

COPY 
name_basics(nconst, primaryName, birthYear, deathYear, primaryProfession, knownFortitles)
FROM
'C:/Users/Public/name.basics.csv' DELIMITER ',' CSV HEADER NULL as '\N';


CREATE TABLE title_akas
(
	titleID CHAR (10) NOT NULL,
	ordering INT,
	title TEXT NOT NULL,
	region CHAR (10),
	language CHAR (10),
	types CHAR (100),
	attributes CHAR (500),
	isOriginalTitle INT
);

COPY 
title_akas(titleID, ordering, title, region, language, types, attributes, isOriginalTitle)
FROM
'C:/Users/HP/Documents/DSTProject/title.akas.csv' DELIMITER ',' CSV HEADER NULL as '\N';


CREATE TABLE title_basics
(
	tconst VARCHAR (10) NOT NULL,
	titleType VARCHAR (20),
	primaryTitle VARCHAR (500) NOT NULL,
	originalTitle VARCHAR (500),
	isAdult INT,
	startYear numeric (4),
	endYear INT,
	runtimeMinutes TEXT,
	genres VARCHAR (50),
	PRIMARY KEY (tconst)
);

COPY 
title_basics(tconst, titleType, primaryTitle, originalTitle, isAdult, startYear, endYear, runtimeMinutes, genres)
FROM
'C:/Users/HP/Documents/DSTProject/title.basics.csv' DELIMITER ',' CSV HEADER NULL as '\N';
**/


CREATE TABLE title_basics
(
	tconst VARCHAR (10) NOT NULL,
	titleType VARCHAR(20),
	primaryTitle VARChar(500) NOT NULL,
	originalTitle VARCHAR(500),
	isAdult INT,
	startYear numeric(4),
	endYear INT,
	runtimeMinutes TEXT,
	genres VARCHAR(50)
);

COPY title_basics(tconst,titleType,primaryTitle,originalTitle,isAdult,startYear,endYear,runtimeMinutes,genres)
FROM 'C:/Users/HP/Documents/DSTProject/title.basics.csv' DELIMITER ',' CSV HEADER NULL as '\N';

/**
CREATE TABLE title_crew
(
	tconst CHAR (10) NOT NULL,
	directors TEXT,
	writers TEXT,
	PRIMARY KEY (tconst)
);

COPY title_crew(tconst,directors,writers)
FROM 'C:/Users/HP/Documents/DSTProject/title.crew.csv' DELIMITER ',' CSV HEADER NULL as '\N';

CREATE TABLE title_episode
(
	tconst VARCHAR (10) NOT NULL,
	parentTconst VARCHAR(10),
	seasonNumber INT,
	episodeNumber INT,
	PRIMARY KEY tconst
);

COPY title_episode(tconst,parentTconst,seasonNumber,episodeNumber)
FROM 'C:/Users/HP/Documents/DSTProject/title.episode.csv' DELIMITER ',' CSV HEADER NULL as '\N';

CREATE TABLE title_principals
(
	tconst VARCHAR (10) NOT NULL,
	ordering INT,
	nconst VARCHAR(10),
	category VARCHAR(50),
	job TEXT,
	characters TEXT
);

COPY title_principals(tconst,ordering,nconst,category,job,characters)
FROM 'C:/Users/HP/Documents/DSTProject/title.principals.csv' DELIMITER ',' CSV HEADER NULL as '\N';

**/