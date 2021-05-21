import os
from threading import Thread
from random import randint

from mongotqdm import tqdm
from time import sleep


def bar_progress(i):
    factor = randint(1, 20)
    print(f'Thread {i} launched with a factor of {factor} and {os.environ["TQDM_NAME"]}.')
    for _ in tqdm(range(0, 300), desc=f'Description of the bar progress {i}', initial=0, name=f'test{i}'):
        sleep(randint(1, 10) / factor)


for i in range(1, 9):
    os.environ['TQDM_NAME'] = f'test{i}'
    Thread(target=bar_progress, args=(i, )).start()


# for i in tqdm(range(0, 10), desc='Hello'):
#     sleep(0.2)
#     print('Goodbye')
