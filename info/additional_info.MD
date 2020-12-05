# Quick References

# Database
#### Truncate User table
`TRUNCATE public."user" CASCADE;`

#### Reset User PK
`ALTER SEQUENCE user_user_id_seq RESTART;`

#### Query
`SELECT * FROM public."user";`</br>
`SELECT * FROM email_address;`

#### Export dump
`pg_dump -h localhost -U postgres fyp-20s4-06p > dump.out`

#### Import dump
`psql -h localhost -p 5432 -U postgres -d fyp-20s4-06p -f <dump.out>`

#### Drop db FORCE
`psql -h localhost -d template1 -U postgres -p 5432 -a -f <file.sql>`

#### To connect to Heroku DB using PgAdmin
>Create Server -> Connection </br>
Host Name: ec2 instance of HerokuPostgres</br>
Port: 5432</br>
Maintenance DB: instance on Heroku DB page</br>
Username: from Heroku DB page</br>
Password: from Heroku DB page</br>
Advanced -> Restriction
DB restriction: maintenance db // supposed to put quotes but it doesn't really work

#### To update Database Schema on Heroku if `flask db upgrade fails`
`psql -h <heroku-host> -U <postgres-user> <db-name> < <dump.file>`

## Environment
#### Mac
>If pip install fails because of psycopg2 error, brew install postgresql
* If you do not have homebrew, go to Homebrew website and install it</br>
* If you still get psycopg2 errors, brew install psycopg2-binary


# PyTest
<b><big>You will need to remove the added users / email address manually for now</big></b></br>
`DELETE FROM PUBLIC.EMAIL_ADDRESS WHERE EMAIL_ADDRESS = 'TESTMAIL456@MYMAIL.COM';`
`DELETE FROM PUBLIC.USER WHERE USERNAME = 'TESTUSER123';`</br>
## Unit Test
`py -m pytest tests/unit`
## API Test
`py -m pytest tests/api`
## Functional Test
`py -m pytest tests/functional`

<b><big>Run all suites in root directory</big></b></br>
It will look for all files in tests starting with test_*
