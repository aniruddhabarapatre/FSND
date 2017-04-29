-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

# Database for the project
CREATE database tournament;

# Players table to save player related information
CREATE TABLE players (
    pid serial PRIMARY KEY,
    name text NOT NULL
)
