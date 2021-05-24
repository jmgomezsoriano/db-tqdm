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

## Use db-tqdm

To use is very similar to tqdm. For example, if you are using the progress bar into normal console application or 
jupyter notebook, you only need to execute:

```python
from dbtqdm.mongo import tqdm

for i in tqdm(range(0, 10), desc='Normal bar'):
    sleep(1)
```

This code will show in the suitable output the following progress bar as usual:

```shell
Normal bar:  60%|██████    | 6/10 [00:06<00:04,  1.00s/it]
```

However, if you define the environment variables TQDM_MODE to 'auto' and TQDM_NAME with a bar name 
(or put the suitable extra arguments to tqdm), the prgress bar will not appear on the console output, 
but the state of the progress bar will be stored in a MongoDB and that progress bar can be presented as following:



