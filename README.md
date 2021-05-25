# db-tqdm
A web based tqdm process bars.

This TQDM based module is very useful for web, airflow, servers or similar environments which do not have console 
to show the typical tqdm process bars.
In these environments are not useful to use the standard TQDM module because the access to the console or log files are
not easy, and if it writes into logs, this one are fulfilled with the progress bar information instead of the
real information log data.

This module, by default, works the same way that the standard TQDM module. Only if the mode parameter is changed by
'mongo', or the environment variable 'TQDM_MODE' is defined with 'mongo', then the progress bar will store into a
database. This module also include the Flask server in order to show this information with a browser like this:

![Example of DBTQDM progress bar](https://github.com/jmgomezsoriano/db-tqdm/raw/master/img/example01.jpg)

## Install db-tqdm
To install only need to do the following:

```shell
pip install db-tqdm
```

If you are using the pymongo database instead the standard TQDM module, you need to install:

```shell
pip install pymongo
```

If you are using also the web user interface, you need to install the following modules:

```shell
pip install flask flask-cors
```

## Use tqdm based on db-tqdm module

To use is very similar to tqdm. For example, if you are using the progress bar into normal console application or 
jupyter notebook, you only need to execute:

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

However, if you define the environment variables TQDM_MODE to 'auto' and TQDM_NAME with a bar name 
(or put the suitable extra arguments to tqdm), the progress bar will not appear on the console output, 
but the state of the progress bar will be stored in a MongoDB. For instance, the following code:

```python
from dbtqdm.mongo import tqdm
from time import sleep

for _ in tqdm(range(0, 5000), desc=f'Description of the progress bar 1', mode='mongo', name='test1', colour='red'):
    sleep(1)
```

![Example of DBTQDM progress bar](https://github.com/jmgomezsoriano/db-tqdm/raw/master/img/example02.jpg)

The previous result can be also obtained using environment variables. For example:

```python
from dbtqdm.mongo import tqdm
from time import sleep
from os import environ
environ['TQDM_MODE'] = 'mongo'
environ['TQDM_NAME'] = 'test1'


for _ in tqdm(range(0, 5000), desc=f'Description of the progress bar 1', colour='red'):
    sleep(1)
```

Using environment variables instead the parameters allow you to use exactly the same code in different platforms
(for example, local workstation or in remote airflow server), and depending on the defined environment variables
can switch between different user interfaces.

The previous code assumes that the MongoDB is in local host and in the default port (27017). 
However, if you want to change this default values, you can use the 'TQDM_DB_HOST', 'TQDM_DB_PORT' environment variables,
or the 'host' or 'port' parameters in tqdm(). Also, you can define the 'TQDM_REPLICASET' environment variable, or
the 'replicaset' parameter.

By default, it will create a database called 'tqdm'. If you want to change the database name, you can use the
environment variable 'TQDM_DB_NAME', or the parameter 'db' in tqdm(). For example:

```python
from dbtqdm.mongo import tqdm
from time import sleep

for _ in tqdm(range(0, 5000), desc=f'Description of the progress bar 1', colour='red', mode='mongo',
              host='localhost', port=27017, replicaset=None, db='tqdm', name='test1'):
    sleep(1)
```

Finally, there is another parameter called 'suffix'. This parameter is useful to create several bars 
for the same process with the same bar name but with different suffix. This way, if you define the environment variable
'TQDM_NAME' for a process that contain different progress bars, it can be differentiate using the suffix.
For instance:

I have the following environment variables defined outside my program:
```shell
# Environment variable
export TQDM_MODE='mongo'
export TQDM_HOST='localhost'
export TQDM_PORT=27017
export TQDM_NAME='test1'
```

However, my program create two long process monitored by tqdm as following:

```python
from dbtqdm.mongo import tqdm
from time import sleep

for _ in tqdm(range(0, 5000), desc=f'Description of the first progress bar', colour='red', suffix='_main'):
    sleep(1)
    
for _ in tqdm(range(0, 5000), desc=f'Description of the second progress bar', colour='red', suffix='_secondary'):
    sleep(1)
```

If you execute the Python program without the environment variables, it will work as usual, ignoring the suffix 
parameter. Nevertheless, if you define the environment variables, the first one will have the title 'test1_main', 
and the second one will have the title 'test1_secondary'. It would help to differentiate between both processes.

## Start the start

If you want to see the information of the process bars, db-tqdm module includes a Flask server to give you a web 
representation. This server is executed with the following command:

```shell
usage: dbtqdm [-h] [-H HOST] [-p PORT] [-t TYPE] [--db_host HOST]
              [--db_port PORT] [-r NAME] [-d NAME] [-i SECONDS]
              [TITLE]

Start the server to serve the bar progress data.

positional arguments:
  TITLE                 The web page title. By default, "Process monitors".

optional arguments:
  -h, --help            show this help message and exit
  -H HOST, --host HOST  The server host. By default, localhost.
  -p PORT, --port PORT  The server port. By default, 5000.
  -t TYPE, --db_type TYPE
                        The database host. By default, mongo. Available
                        databases: ['mongo'].
  --db_host HOST        The database host. By default, localhost.
  --db_port PORT        The database port. By default, 5000.
  -r NAME, --replicaset NAME
                        The replicaset. By default, none.
  -d NAME, --database NAME
                        The database name. By default, tqdm.
  -i SECONDS, --interval SECONDS
                        The database name. By default, tqdm.
```

If you have the default values, only need to run the following to start the server:

```shell
dbtqdm
```

**Note:** At the moment, the argument 'db_type' is not supported, and it will be ignored.

## Table of variables and parameters

All these variables and parameters only work with the mode **mongo**. With mode **auto** they are ignored.

### Environment variables

| Variable        | Description                                                                         |
|-----------------|-------------------------------------------------------------------------------------|
| TQDM_MODE       | The working mode of tqdm process bar:<br/><ul><li>'**auto**': Normal mode (by default).</li><li>'**mongo**': The MongoDB mode.</li></ul> |
| TQDM_NAME       | The progress bar name. It will use to identify the progress bar among others.       |
| TQDM_HOST       | The database host. By default, localhost.                                           |
| TQDM_PORT       | The database port. By default, 27017.                                               |
| TQDM_REPLICASET | The replicaset for MongoDB. By default, it is not used.                             |
| TQDM_DB_NAME    | The database name where the progress bar states are stored. By default, '**tqdm**'. |

### Parameters
| Parameter  | Description                                                                                                   |
|------------|-------------------------------------------------------------------------------------------|
| mode       | The working mode of tqdm process bar:<br/><ul><li>'**auto**': Normal mode (by default).</li><li>'**mongo**': The MongoDB mode.</li></ul> |
| name       | The progress bar name. It will use to identify the progress bar among others.             |
| suffix     | The suffix to add to the bar name. Together the name, it will use to identify the progress bar among others in the case that there are multiple progress bars with the same name. |
| host       | The database host. By default, localhost.                                                 |
| port       | The database port. By default, 27017.                                                     |
| replicaset | The replicaset for MongoDB. By default, it is not used.                                   |
| db         | The database name where the progress bar states are stored. By default, '**tqdm**'.       |


## To do

### Message when there are any active process bar

Show a message when there are no active process bars.

### User and password for MongoDB connection

Add the possibility to set the user and password for the MongoDB connection.

### Create a historical view of finished processes

In the collection _&#95;stats&#95;_ are the historical information about the finished processes. 
It could be interesting to use them in a view with this information. The idea is to use the home page, below 
the progress bars in the main page, to add a section with a paged table with the finished processes ordered descending
by start time.

### Generalize to be able to use other database managers

The core of the module is ready to use another database managers creating classes inherited from _DatabaseTqdm_.
However, the server process is not prepared to use other database managers, only MongoDB. 
It could be interesting to refactor the code to add this functionality.

### Use Redis or Kafka

This can be adapted (but without historical information) to be used with [Redis](https://redis.io/) or 
[Kafka](https://kafka.apache.org/) platforms.

### Pass collections to registers 

I made the design decision to create each process bar in a MongoDB collection instead of create a register for each
process. I do not sure because I made that decision, and I think it would be better to replace the different collections
by registers of a unique MongoDB collection.

