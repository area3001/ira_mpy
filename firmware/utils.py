import os

def rmdir(dir):
    for i in os.listdir(dir):
        os.remove('{}/{}'.format(dir,i))
    os.rmdir(dir)