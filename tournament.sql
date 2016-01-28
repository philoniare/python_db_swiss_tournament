-- Table definitions for the tournament project.
--
--

DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
-- connect to db tournament
\c tournament;


/* Players table
    +---------+-------------+
    |   Id    |    name     |
    +---------+-------------+
    | Serial  | varchar(50) |
    | Primary | NOT NULL    |
    +---------+-------------+
*/

-- create initial Tables
CREATE TABLE players (
    id serial PRIMARY KEY,
    name varchar(50) NOT NULL
);


/* Tournaments table
    +---------+-------------+
    |   Id    |    name     |
    +---------+-------------+
    | Serial  | varchar(50) |
    | Primary | NOT NULL    |
    +---------+-------------+
*/


CREATE TABLE tournaments (
    id serial PRIMARY KEY,
    name varchar(50) NOT NULL
);


/* Matches TABLE
    +---------+-----------------+-----------------+---------------------+
    |   Id    |     winner      |      loser      |     tournament      |
    +---------+-----------------+-----------------+---------------------+
    | Serial  | int             | int             | int                 |
    | Primary | ref players(id) | ref players(id) | ref tournaments(id) |
    +---------+-----------------+-----------------+---------------------+
*/

CREATE TABLE matches (
    id serial PRIMARY KEY,
    winner int references players(id),
    loser int references players(id), 
    tournament int references tournaments(id)
);


-- needed for granting permission to the user, possibly optional
--GRANT ALL PRIVILEGES ON TABLE players TO philoniare;
--GRANT ALL PRIVILEGES ON TABLE matches TO philoniare;
--GRANT USAGE, SELECT ON SEQUENCE players_id_seq TO philoniare;
--GRANT USAGE, SELECT ON SEQUENCE matches_id_seq TO philoniare;
--GRANT ALL PRIVILEGES ON TABLE standings TO philoniare;



-- View: return players ordered by their win record
--      format: id, name, wins, total_matches
CREATE VIEW standings AS SELECT players.id, players.name, 
    SUM(CASE WHEN matches.winner=players.id THEN 1 else 0 END) as wins, 
    SUM(CASE WHEN matches.loser=players.id or matches.winner=players.id 
    THEN 1 else 0 END) as matches, matches.tournament FROM players 
    left join matches on players.id=matches.winner or 
    players.id=matches.loser group by players.id, matches.tournament ORDER BY wins DESC;