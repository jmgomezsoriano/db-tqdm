# db-tqdm
A tqdm bar progress that works with MongoDB instead of console.

This TQDM based module is very useful for web, airflow or similar environments. 
In these environments are not useful to use the standard TQDM module because the access to the console or log files are
not easy, and if it writes into logs, this one are fulfilled with the progress bar information instead of the
real information log data.

This module, by default, works the same way that the standard TQDM module. Only if the mode parameter is changed by
'mongo', or the environment variable 'TQDM_MODE' is defined with 'mongo', then the progress bar will store into a
database. This module also include the Flask server in order to show this information with a browser like this:

```shell

Normal bar:  60%|██████    | 6/10 [00:06<00:04,  1.00s/it]
```


