-- Table definitions for the tournament project.
--
--

-- connect to db tournament
\c tournament;

-- create initial Tables
CREATE TABLE players (
    id serial PRIMARY KEY,
    name varchar(50) NOT NULL
);

-- needed for granting permission to the user, possibly optional
--GRANT ALL PRIVILEGES ON TABLE players TO philoniare;
--GRANT ALL PRIVILEGES ON TABLE matches TO philoniare;
--GRANT USAGE, SELECT ON SEQUENCE players_id_seq TO philoniare;
--GRANT USAGE, SELECT ON SEQUENCE matches_id_seq TO philoniare;

CREATE TABLE matches (
    id serial PRIMARY KEY,
    winner int references players(id),
    loser int references players(id)
);
