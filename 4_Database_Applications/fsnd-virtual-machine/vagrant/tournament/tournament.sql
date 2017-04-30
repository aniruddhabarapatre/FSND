-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- Database for the project
DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament

-- Players table to save player related information
CREATE TABLE players (
    pid serial PRIMARY KEY,
    name text NOT NULL
);

-- Matches table to save player matches information
CREATE TABLE matches (
    mid serial PRIMARY KEY,
    winner int REFERENCES players(pid),
    loser int REFERENCES players(pid)
);

CREATE VIEW v_standings AS
    SELECT p.pid, p.name,
    (SELECT count(m.winner)
        FROM matches m
        WHERE p.pid = m.winner)
    AS wins,
    (SELECT count(m.mid)
        FROM matches m
        WHERE p.pid = m.winner
        OR p.pid = m.loser)
    AS matches
    FROM players p
    ORDER BY wins;
