[!logo](./pictures/piscator_logo.png)
# Project Piscator

## Introduction
Project Piscator is a final-year project by a group of 6 University of
Wollongong (SIMGE) students pursuing their Bachelor's of Computer Science.
The assigned topic for the project is an email phishing detection system.

## Goals
The end product of this project will be a subscription-based service that provides
automatic email phishing detection in users' mailboxes that will detect possibly
malicious emails and execute a soft delete.

## Technologies Used (WIP)
The project will be built primarily on the following tech
- Backend: Python Flask
- Web Server: Gunicorn
- Frontend: HTML (for now)
- Database: PostgreSQL
- Deployment: Heroku
- Version Control: Git

## Developer's Instructions (Windows)
1. Clone the repository with `git clone`
  - `git clone https://github.com/jonzxz/project-piscator.git`
2. Install PostgreSQL from https://www.enterprisedb.com/downloads/postgres-postgresql-downloads
  - Database version used during development will be version 13
  - Optionally to include pgAdmin for UI
  - Use "pa$$w0rd" for default admin password (for now)
3. Setup Python virtual environment for project
  - Create virtual environment with command line
    - `python -m venv <any_name>` eg. `python -m venv piscator-venv`
    - Ensure you have Python home set in your %PATH% variable
  - Install dependencies with command line
    - `cd Scripts`
    - `activate`
    - `cd ..`
    - `pip install -r requirements.txt`
4. Initialize & Update Database instance
  - Manually
    - `createdb -host localhost -p 5432 -U postgres fyp-20s4-06p`
    - `psql -h localhost -p 5432 -U postgres -d fyp-20s4-06p -f <dump_file>`
  - or with `update_db.bat`
  - Both creates / reinitializes the database and imports all existing data in

5. Exporting Database dump
  - Manually
    - `pg_dump -h localhost -p 5432 -U postgres fyp-20s4-06p > <dump_file>`
  - or with `export_db.bat`


## Usage
- `py -m projectpiscator`
- Default port is localhost:4000

- If there are changes in database schema, do a `flask db upgrade` <b>before importing dumps</b>
