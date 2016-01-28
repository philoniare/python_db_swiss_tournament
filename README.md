# Swiss-Style Tournament Simulation
### made with Postgres DB using psycopg2 interface in Python

## Project Dependencies:
- Postgres
- psycopg2 (postgres interface for Python)

## How to run:
- Run the sql commands to create the database, tables and custom views by running
`psql -f tournament.sql`
- Edit tournament.py to call the available methods
- Finally, run `python tournament.py` to run your script

## Directory Structure:
- tournament.py contains functions for abstracting out the database layer
- tournament_test.py contains tests for tournament.py

## Available methods:
    clearTable(table_name): Deletes all entries inside a given table.

    countPlayers(): Returns the number of players currently registered.

    registerPlayer(name): Adds a player to the tournament database.

    playerStandings(): Returns a list of the players and their win records, sorted by wins.

    reportMatch(winner, loser): Records the outcome of a single match between two players.

    swissPairings(): Returns a list of pairs of players for the next round of a match.
