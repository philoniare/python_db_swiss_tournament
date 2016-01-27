#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach

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
    count_players = c.fetchall()[0][0]
    conn.close()
    return count_players

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    conn, c = getConnCursor()
    # sanitize input
    name = bleach.clean(name)
    
    # Add the player providing the name
    c.execute("INSERT INTO players (name) VALUES (%s);", (name,))
    conn.commit()
    conn.close()
    


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn, c = getConnCursor()
    # Fecching players with sum of wins and total match count in tournament
    c.execute("SELECT players.id, players.name, "
    "sum(CASE WHEN matches.winner=players.id THEN 1 else 0 END) as wins,"
    " sum(CASE WHEN matches.loser=players.id or matches.winner=players.id "
    "THEN 1 else 0 END) as matches FROM players left join matches on "
    "players.id=matches.winner or players.id=matches.loser group by players.id;")
    players = c.fetchall()
    
    # Sort by number of wins
    players = sorted(players, key=lambda x: x[2])
    conn.close()
    return players
    

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn, c = getConnCursor()
    
    # Create a match record with given ids
    c.execute("INSERT INTO matches (winner, loser) VALUES (%s, %s);", (winner, loser))
    conn.commit()
    conn.close()
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    # Fetch current_standings of players
    player_stadings = playerStandings()
    
    pairings = []
    for i in range(0, len(player_stadings), 2):
        pairings.append((player_stadings[i][0], player_stadings[i][1], 
            player_stadings[i+1][0], player_stadings[i+1][1]))
    return pairings
    
    