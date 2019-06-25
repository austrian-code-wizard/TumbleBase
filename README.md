# Python
## Setting up virtual environment

Go into folder where you want to generate virtual environment.

```console
python3 -m venv ./venv/
```

Set venv as used python environment to run your code.

```console
source /venv/bin/activate
```

After setting venv as used environment install all packages from requirements.txt.

```console
python3 -m pip install -r requirements.txt
```

If you get an error package requirements.txt doesn't exist you only have to add the -r flag, which you forgot before.

## Install python package and generate requirements.txt

Install any new python package with the following command:

```console
(venv) user-pc:franglomat user$ python3 -m pip install flask-restful
```

Generate a requirements.txt file after installing all needed pyhton packages. Don't forget to generate always a new
requirements.txt file after installing new python packages. Otherwise it is not possible for every developer to set up a
correct venv!

```console
(venv) user-pc:franglomat user$ python3 -m pip freeze > requirements.txt
```

## Flask

##### Important links

[basic knowledge about flask_restulf](https://flask-restful.readthedocs.io/en/latest/)\
[json web tokens](https://www.youtube.com/watch?v=WxGBoY5iNXY)

## SqlAlchemy

##### Important links

[basic relationships in sqlalchemy](https://docs.sqlalchemy.org/en/latest/orm/basic_relationships.html)

# Database

## PostgreSQL Linux

[install PostgreSQL on Ubuntu](https://tecadmin.net/install-postgresql-server-on-ubuntu/)

After installing PostgreSQL on Ubuntu you have to follow these steps [create postgres user](#postgresql-create-new-user)


## PostgreSQL MacOS

##### Uninstall old PostgreSQL

```console
brew uninstall --force postgresql
```

##### Remove old PostgreSQL files

```console
rm -rf /usr/local/var/postgres
```

##### Install PostgreSQL

```console
brew install postgres
```

##### Install PostGIS

Postgis increases Postgres management capabilities by adding geospatial types and functions to enhance spatial data 
handled within a relational database structure.

```console
brew install postgis
```

##### Remove old database file

```console
rm -r /usr/local/var/postgres
```

##### Run the init command again

```console
initdb /usr/local/var/postgres
```

##### Start PostgreSQL server

````console
pg_ctl -D /usr/local/var/postgres/ -l logfile start
````

##### Create a new database

```console
createdb <database>
```

##### Enable PostGIS

````console
psql <database>
````

##### Creating extension for PostGIS

````console
CREATE EXTENSION postgis;
````

## PostgreSQL Create new user

##### Create user and grant rights to him

````console
sudo -u postgres psql
postgres=# create database <database>;
postgres=# create user <user> with encrypted password '<password>';
postgres=# grant all privileges on database <database> to <user>;
````

##### Create vocabulary_user and grant rights to him (MacOS)

````console
psql vocabulary
vocabulary=# create user vocabulary_user with encrypted password 'password';
vocabulary=# grant all privileges on database vocabulary to vocabulary_user;
````

Checking if new user has the right rights for the database.

````console
psql -h localhost -d vocabulary -U vocabulary_user
````

If database opens all worked correctly, hardly always you have to enter a password for user vocabulary_user which is 
password in our case.