-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--

-- connect to db tournament
\c tournament;

-- create initial Tables
CREATE TABLE players (
    id serial PRIMARY KEY,
    name varchar(50) NOT NULL
);

GRANT ALL PRIVILEGES ON TABLE players TO philoniare;
GRANT USAGE, SELECT ON SEQUENCE players_id_seq TO philoniare;

CREATE TABLE matches (
    id serial PRIMARY KEY,
    winner int references players(id),
    loser int references players(id),
);
