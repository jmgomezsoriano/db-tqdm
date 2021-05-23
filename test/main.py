import os
from threading import Thread
from random import randint

from dbtqdm.mongo import tqdm
from time import sleep


def bar_progress(i, colour):
    factor = randint(1, 20)
    print(f'Thread {i} launched with a factor of {factor} and {os.environ["TQDM_NAME"]}.')
    for _ in tqdm(range(0, 5000), desc=f'Description of the bar progress {i}', initial=0, name=f'test{i}',
                  colour=colour, mode='mongo'):
        sleep(randint(1, 10) / factor)


for i, colour in [(1, 'red'), (2, 'green'), (3, 'purple'), (4, None)]:
    os.environ['TQDM_NAME'] = f'test{i}'
    Thread(target=bar_progress, args=(i, colour)).start()


for i in tqdm(range(0, 20), desc='With suffix', mode='mongo', name='test1', suffix='_other'):
    sleep(1)

for i in tqdm(range(0, 20), desc='Normal bar'):
    sleep(1)

print('Goodbye')
