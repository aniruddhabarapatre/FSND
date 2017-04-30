# Udacity FSND P4: Tournament Results

This project creates a Python module that uses a PostgreSQL database to keep track of players and matches in a game tournment using the [Swiss pairings system](https://en.wikipedia.org/wiki/Swiss-system_tournament). It is created as a part of project submission for **Full Stack Nanodegree** by **Udacity**.

## Technologies used:

* Python 3.5
* Vagrant
* PostgreSQL

## Usage

Boot up the vagrant machine and navigate to project directory as `/vagrant/tournament`, for e.g.
```
vagrant up
vagrant ssh
cd /vagrant/tournament/
```

### Setting up database

Run the `\i tournament.sql` in `psql` environment. This would create the required `tournament` database for this module.
```
ubuntu@ubuntu-xenial:/vagrant/tournament$ psql
psql (9.5.6)
Type "help" for help.

ubuntu=> \i tournament.sql
DROP DATABASE
CREATE DATABASE
You are now connected to database "tournament" as user "ubuntu".
CREATE TABLE
CREATE TABLE
CREATE VIEW
tournament=> \q
```

### Running Tests

Run `tournament_test.py` file to test all the functionality in the module. Output of test results should be -
```
ubuntu@ubuntu-xenial:/vagrant/tournament$ python3 tournament_test.py
1. countPlayers() returns 0 after initial deletePlayers() execution.
2. countPlayers() returns 1 after one player is registered.
3. countPlayers() returns 2 after two players are registered.
4. countPlayers() returns zero after registered players are deleted.
5. Player records successfully deleted.
6. Newly registered players appear in the standings with no matches.
7. After a match, players have updated standings.
8. After match deletion, player standings are properly reset.
9. Matches are properly deleted.
10. After one match, players with one win are properly paired.
Success!  All tests pass!
```
