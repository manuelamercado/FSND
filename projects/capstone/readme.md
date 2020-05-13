# How to set up:
* Create a database named 'capstone' using `createdb capstone`. You can pass the user if you want. Modify the database URI that is in `setup.sh`.
* Go to `starter` folder: `cd starter`.
* Run `source setup.sh` to get the environment variables available.

## Installing Requirements:
* Is recomendable to set up a virtual environment. You can do it with the following commands:
```
python3 -m venv env
source env/bin/activate
```
* Install dependencies running `pip3 install -r requirements.txt`
* Deactivate the virtual environment just running `deactivate`.
  
## Migrations:
* Create the initial migrations configuration: `flask db init`.
* Detects migrations to run `flask db migrate`
* Upgrade (apply) changes `flask db upgrade`
* Downgrade changes `flask db downgrade`