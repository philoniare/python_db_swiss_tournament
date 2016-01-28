#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")

def getConnCursor():
    """Connects to db and returns connection and cursor."""
    conn = connect()
    c = conn.cursor()
    return conn, c

def clearTable(table_name):
    """Deletes all entries inside a given table."""
    conn, c = getConnCursor()
    c.execute("DELETE FROM " + table_name + " *;")
    conn.commit()
    conn.close()
    
def deleteMatches():
    """Remove all the match records from the database."""
    clearTable('matches')
    

def deletePlayers():
    """Remove all the player records from the database."""
    clearTable('players')
    

def countPlayers():
    """Returns the number of players currently registered."""
    conn, c = getConnCursor()
    c.execute("SELECT COUNT(*) FROM players;")
    
    # save player count from cursor
    count_players = c.fetchone()[0]
    conn.close()
    return count_players

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (
    
    Args:
      name: the player's full name (need not be unique).
    """
    conn, c = getConnCursor()

    # Add the player providing the name
    c.execute("INSERT INTO players (name) VALUES (%s);", (name,))
    conn.commit()
    conn.close()
    
def createTournament(name)
    """Adds a tournament to the tournaments table to keep track of multiple tournaments.
        
        Args:
            name: the tournament name (need to be unique).
    """
    conn, c = getConnCursor()
    
    c.execute("INSERT INTO tournaments (name) VALUES (%s) RETURNING id;", (name,))
    tournament_id = c.fetchone()[0]
    conn.commit()
    conn.close()
    return tournament_id

def playerStandings(tournament_id):
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Args:
        tournament_id:  the id number of the tournament
        
    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn, c = getConnCursor()
    # Fetching players with sum of wins and total match count ordered by number of wins
    c.execute("SELECT * FROM standings;")
    players = c.fetchall()
    
    # Sort by number of wins
    conn.close()
    return players
    

def reportMatch(winner, loser, tournament_id):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
      tournament_id:  the id number of the tournament
    """
    conn, c = getConnCursor()
    
    # Create a match record with given ids
    c.execute("INSERT INTO matches (winner, loser, tournament_id) VALUES (%s, %s, %s);", (winner, loser, tournament_id))
    conn.commit()
    conn.close()
 
def swissPairings(tournament_id):
    """Returns a list of pairs of players for the next round of a match.
    
    Args:
        tournament_id:  the id number of the tournament
    
    Assuming that there are an even and odd number of players registered, each player
    appears exactly once in the pairings. If odd number of players, last player skips the round.
    Each player is paired with another player with an equal or nearly-equal win 
    record, that is, a player adjacent to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    # Fetch current_standings of players
    player_standings = playerStandings(tournament_id)
    
    # handle odd number of players
    if len(player_standings) % 2 == 1:
        skipped_round_player = player_standings.pop()  # skipped round for last player
    
    pairings = []
    for i in range(0, len(player_standings), 2):
        pairings.append((player_standings[i][0], player_standings[i][1], 
            player_standings[i+1][0], player_standings[i+1][1]))
    return pairings
    
    