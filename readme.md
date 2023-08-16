# MyPass Daemon project

This package should be installed to run the daemon on your machine.
Plugins, and such will be communicating with your own, local service.

## PostgreSQL database initialization

> psql -U postgres

We will create a user for our db in the next section.

postgres-#

> **CREATE USER** mypass **WITH PASSWORD** '${your password goes here}';\
> **ALTER ROLE** mypass **SET** client_encoding **TO** 'utf8';\
> **ALTER ROLE** mypass **SET** default_transaction_isolation **TO** 'read committed';\
> **ALTER ROLE** mypass **SET** timezone **TO** 'UTC';

Next, execute the following db creation script:

```sql
CREATE DATABASE mypass
    WITH
    OWNER = mypass
    ENCODING = 'UTF8'
    LC_COLLATE = 'C'
    LC_CTYPE = 'C'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;

GRANT ALL ON DATABASE mypass TO mypass;
```

### Migrations

!!! TODO !!!

## MySQL and MariaDB initialization

```sql
-- Create a user with a password
CREATE USER 'mypass'@'localhost' IDENTIFIED BY '${your password goes here}';

-- Set user options
SET GLOBAL character_set_client = 'utf8';
SET GLOBAL transaction_isolation = 'READ-COMMITTED';
SET GLOBAL time_zone = '+00:00';

-- Create a database
CREATE DATABASE mypass CHARACTER SET utf8 COLLATE utf8_general_ci;

-- Grant privileges on the database to the user
GRANT ALL PRIVILEGES ON mypass.* TO 'mypass'@'localhost';

-- Flush privileges to apply changes
FLUSH PRIVILEGES;
```

## Environment setup

Database connection string should be configured using the environment variable `MYPASS_DB_CONNECTION_URI`.
Should be set to something like: `{protocol}://{dbuser}:{dbpass}@{host}:{port}/{dbname}`

### Setup in PostgreSQL
`postgresql+psycopg2://mypass:MyPassWord@localhost:5432/mypass`

### Setup in MySQL and MariaDB
`mysql://mypass:MyPassWord@localhost:3306/mypass`

## Run tests:

> pytest tests

## Run coverage:

> pytest --cov-report html --cov=mypass tests

Possible report options:
 - html
 - json
 - lcov
 - annotate

To report to a specified file, you could use the following command:

> pytest --cov-report html:.reports/coverage.html --cov=mypass tests

Run code style guide:

> flake8 mypass

## Cleanup

To clean local binaries, run:

> pyclean -v .

or clean only the package:

> pyclean -v mypass
