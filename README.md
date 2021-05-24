# db-tqdm
A tqdm bar progress that works with MongoDB instead of console.

This TQDM based module is very useful for web, airflow or similar environments. 
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