# db-tqdm
A web based tqdm process bars.

This TQDM based module is very useful for web, airflow, servers or similar environments which do not have console 
to show the typical tqdm process bars.
In these environments are not useful to use the standard TQDM module because the access to the console or log files are
not easy, and if it writes into logs, this one are fulfilled with the progress bar information instead of the
real information log data.

This module, by default, works the same way that the standard TQDM module. Only if the mode parameter is changed by
'mongo', or the environment variable 'TQDM_MODE' is defined with 'mongo', then the progress bar will store into a
database,instead of printing it in the standard error output.
This module also include the Uvicorn server in order to show this information with a browser like this:

![Example of DB-TQDM progress bar](https://github.com/jmgomezsoriano/db-tqdm/raw/master/img/example01.jpg)

## Content

* [db-tqdm module](#db-tqdm-module)
  * [Install db-tqdm](#install-db-tqdm)
  * [Execute the server](#execute-the-server)
  * [Use db-tqdm module](#use-db-tqdm-module)
* [db-tqdm environment variables](#db-tqdm-environment-variables)
* [db-tqdm docker](#db-tqdm-docker)
* [To do](#to-do)

# db-tqdm module<a id="db-tqdm-module" name="db-tqdm-module"></a>

You can use db-tqdm as a usual Python module and integrate it into your Python projects. This section explains how to
[install](#install-db-tqdm), execute the server and test the db-tqdm module.

## Install db-tqdm<a id="install-db-tqdm" name="install-db-tqdm"></a>
To install only need to do the following:

```shell
pip install db-tqdm
```

If you are using the pymongo database instead the standard TQDM module, you need to install:

```shell
pip install monutils~=0.1.3
```

In the case, this module will be not installed, then, db-tqdm are going to work as a normal tqdm progress bar.

If you are using also the web user interface, you need to install the following modules:

```shell
pip install fastapi~=0.70.0 Jinja2~=3.0.2 uvicorn~=0.15.0 importlib-resources~=5.1.3
```

## Execute the server<a id="execute-the-server" name="execute-the-server"></a>

You can execute the db-tqdm server in both, docker image or natively. If you choose the second option, 
you can use the following command:

```bash
usage: dbtqdm [-h] [-H HOST] [-P PORT] [-t TYPE] [--db_host HOST] [--db_port PORT]
              [-r NAME] [-d NAME] [-u USER] [-p PASS] [--cert_key_file FILE] 
              [--ca_file FILE] [--session_token SESSION] [-i SECONDS] [TITLE]

Start the server to serve the bar progress data.

positional arguments:
  TITLE                 The web page title. By default, "Process monitors".

optional arguments:
  -h, --help            show this help message and exit
  -H HOST, --host HOST  The server host. By default, localhost.
  -P PORT, --port PORT  The server port. By default, 5000.
  -t TYPE, --db_type TYPE
                        The database host. By default, mongo. Available databases: ['mongo'].
  --db_host HOST        The database host. By default, localhost.
  --db_port PORT        The database port. By default, 27017.
  -r NAME, --replicaset NAME
                        The replicaset. By default, none.
  -d NAME, --database NAME
                        The database name. By default, tqdm.
  -u USER, --user USER  The database user. By default, none.
  -p PASS, --password PASS
                        The user password. By default, none.
  --cert_key_file FILE  The cert key fle to connect to the database. By default, none.
  --ca_file FILE        The CA file to connect to the database. By default, none.
  --session_token SESSION
                        The session token to connect to the database. By default, none.
  -i SECONDS, --interval SECONDS
                        The default web refresh interval. By default, 5.
```

For example:

```bash
# Execute the server to connect with mongodb in localhost and port 27017 
# without authentication method and the database name "tqdm"
dbtqdm

# The same as above but defining database connection data
dbtqdm --db_host mymongoserver.com --db_port 18 -u mymongouser -p mymongopass

# Also, you can use environment variables instead command arguments
export TQDM_DB_HOST=mymongoserver.com
export TQDM_DB_PORT=18
export TQDM_DB_USER=mymongouser
export TQDM_DB_PASSWORD=mymongopass

dbtqdm
```

## Use db-tqdm module<a id="use-db-tqdm-module" name="use-db-tqdm-module"></a>

The use of db-tqdm is very similar to normal tqdm. For example, if you are using the progress bar into normal
console application or jupyter notebook, you only need to execute:

```python
from dbtqdm.mongo import tqdm
from time import sleep

for i in tqdm(range(0, 10), desc='Normal bar'):
    sleep(1)
```

This code will show in the suitable output the following progress bar as usual:

```shell
Normal bar:  60%|██████    | 6/10 [00:06<00:04,  1.00s/it]
```

You can change te normal tqdm progrsss bar by the database based one,
using the own db-tqdm parameters, specially mode and name, but not uniquely:

```python
from dbtqdm.mongo import tqdm
from time import sleep

# Create a tqdm based on MongoDB in localhost:27017 with the name "test1" and red colour
for _ in tqdm(range(0, 5000), desc=f'Description of the progress bar 1',
              mode='mongo', name='test1', colour='red'):
    sleep(1)

# The same as above but with the database connection
for _ in tqdm(range(0, 5000), desc=f'Description of the progress bar 1',
              mode='mongo', name='test1', colour='red',
              host='mymongoserver.com', port=18, user='mymongouser', password='mymongopassword'):
    sleep(1)
```

This code will generate the following web-based bar progress:

![Example of DBTQDM progress bar](https://github.com/jmgomezsoriano/db-tqdm/raw/master/img/example02.jpg)

However, we strongly recommend to use environment variables instead of the function parameters because, this way,
your code will be the same if you use the tqdm locally or web-based. For example. this code will generate a normal
tqdm bar progress:

```python
from dbtqdm.mongo import tqdm
from time import sleep

for _ in tqdm(range(0, 5000), desc=f'Description of the progress bar 1', colour='red'):
    sleep(1)
```
Nevertheless, if you define previously the follwoing environment variables, the same code will generate a web-based one:

```bash
export TQDM_MODE=mongo
export TQDM_NAME=test1
```

But this approach has a problem in the case you want to use several progress bars at the same time, 
because each progress bar is identified by its name. The solution is to change the previous code adding the suffix
parameter:

```python
from dbtqdm.mongo import tqdm
from time import sleep

for _ in tqdm(range(0, 10), desc=f'Description of the progress bar 1', colour='red', suffix='_main'):
    for _ in tqdm(range(0, 20), desc=f'Description of the progress bar 1', colour='yellow', suffix='_secondary'):
        sleep(1)
```

If you do not define the DB-TQDM environment variables, both progress bars will be normal ones,
ignoring the suffix parameter. However, if you define those variables, you will have two progress bars with
the name "<bar_name>_main" and "<bar_name>_secondary", respectively.

**Note:** At the moment, do not put spaces neither, the bar name nor bar suffix.

As we can see above, using environment variables instead the parameters allow you to use exactly the same code in 
different platforms (for example, local workstation or in remote airflow server), 
and depending on the defined environment variables can switch between different user interfaces.

**Note:** At the moment, the argument 'db_type' is not supported, and it will be ignored.

# db-tqdm environment variables<a id="db-tqdm-environment-variables" name="db-tqdm-environment-variables"></a>
You can define environment variables to change the way tqdm progress bar appears 
and the MondogDB connection data. All the environment variables you can define are:

|Variable             |Description                                                                                   |
|---------------------|----------------------------------------------------------------------------------------------|
|TQDM_MODE            |If you want a normal or mongo bar progress. By default, normal.                               |                                    |
|TQDM_NAME            |The bar progress name.                                                                        |
|TQDM_SUFFIX          |The suffix of the bar progress name. This value is better to set by function parameter.       |                                    |
|TQDM_HOST            |The Web server host address. By default, localhost.                                           |
|TQDM_PORT            |The Web server port. By default, 5000.                                                        |
|TQDM_TYPE            |The database type. In the current implementation only "mongo" is available. By default, mongo.|
|TQDM_DB_HOST         |The database host address. By default, localhost.                                             |
|TQDM_DB_PORT         |The database port. By default, 27017.                                                         |
|TQDM_DB_REPLICASET   |The mongo replicaset. By default, none.                                                       |
|TQDM_DB_NAME         |The database name. By default, tqdm.                                                          |
|TQDM_DB_USER         |The database username. By default, none.                                                      |
|TQDM_DB_PASSWORD     |The user password. By default, none.                                                          |
|TQDM_DB_CERT_KEY_FILE|The certificate key file. By default, none.                                                   |
|TQDM_DB_CA_FILE      |The CA file. By default, none.                                                                |
|TQDM_INTERVAL        |The web refresh interval in seconds. By default, 5s.                                          |
|TQDM_TITLE           |The web title. By default, 'Process monitors'.                                                |

The TQDM_HOST and TQDM_PORT if only for the Web server.

# db-tqdm docker<a id="db-tqdm-docker" name="db-tqdm-docker"></a>

You can install the db-tqdm server by means a docker image.

```bash
docker pull ialife/db-tqdm:1.1
```

Remember you can define the [environment variables] to set the database connection. 
For example, if you have the mongodb in your localhost, you can execute the following command to connect
the service in the db-tqdm docker with your mongodb:

```bash
docker run -e TQDM_DB_USER=myusename -e TQDM_DB_PASSWORD=mypassword -e TQDM_DB_HOST=localhost \
           -e ROOT_URL=http://localhost -e MONGO_URL=mongodb://localhost:27017 --network="host" ialife/db-tqdm
```

# To do<a id="to-do" name="to-do"></a>

## Message when there are any active process bar

Show a message when there are no active process bars.

## User and password for MongoDB connection

Add the possibility to set the user and password for the MongoDB connection.

## Create a historical view of finished processes

In the collection _&#95;stats&#95;_ are the historical information about the finished processes. 
It could be interesting to use them in a view with this information. The idea is to use the home page, below 
the progress bars in the main page, to add a section with a paged table with the finished processes ordered descending
by start time.

## Generalize to be able to use other database managers

The core of the module is ready to use another database managers creating classes inherited from _DatabaseTqdm_.
However, the server process is not prepared to use other database managers, only MongoDB. 
It could be interesting to refactor the code to add this functionality.

## Use Redis or Kafka

This can be adapted (but without historical information) to be used with [Redis](https://redis.io/) or 
[Kafka](https://kafka.apache.org/) platforms.

## Pass collections to registers 

I made the design decision to create each process bar in a MongoDB collection instead of create a register for each
process. I do not sure because I made that decision, and I think it would be better to replace the different collections
by registers of a unique MongoDB collection.

