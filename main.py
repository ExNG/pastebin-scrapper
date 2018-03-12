#!/usr/bin/python
import os

scriptDir = os.path.dirname(os.path.realpath(__file__))
config = {
    'path': os.path.join(scriptDir, 'data')
}
data = []


def start():
    # Setting up data directory
    print('### Checking if data directory exists (' + config['path'] + ')' )
    if os.path.exists(config['path']):
        print('-> Data directory already exists. Skipping.')
    else:
        print('-> Data directory not found')
        try:
            os.mkdir(config['path'])
            print('-> Data directory created')
        except e:
            print('!! Error creating data directory')

    # Add existing entries to data list
    print('### Indexing pastes')
    for item in os.listdir(config['path']):
        itemPath = os.path.join(config['path'], item)
        if os.path.isdir(itemPath):
            data.append(str(item))
    print('-> Done indexing')


if __name__ == '__main__':
    start()
