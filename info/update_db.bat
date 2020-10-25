psql -h localhost -d template1 -U postgres -p 5432 -a -f drop.sql
psql -h localhost -p 5432 -U postgres -d fyp-20s4-06p -f dump.out
