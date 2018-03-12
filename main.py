#!/usr/bin/python
import os
import time
import urllib2
from bs4 import BeautifulSoup


scriptDir = os.path.dirname(os.path.realpath(__file__))
config = {
    'path': os.path.join(scriptDir, 'data'),
    'pastebinarchive': 'https://pastebin.com/archive',
    'timeout': 60
}
data = []

"""
Setting up data directory

@param dict config

@return (data)
"""
def start(config):
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
    data = []
    for item in os.listdir(config['path']):
        itemPath = os.path.join(config['path'], item)
        if os.path.isfile(itemPath):
            hash = item.split('_')[2]
            data.append(str(hash))
    print('-> Done indexing')

    return (data)


"""
Start loading pastebin's archive

@param dict config
@param list data
"""
def startJob(config, data):
    while True:
        print('### Starting query')

        html = urllib2.urlopen(config['pastebinarchive']).read()
        soup = BeautifulSoup(html, 'html.parser')

        pasteIds = []

        for td in soup.table.find_all('td'):
            if td.a and td.get('class') == None:
                pasteIds.append(str(td.a.get('href')))

        print('-> pasteIds', pasteIds)
        print('-> Done')
        time.sleep(config['timeout'])


if __name__ == '__main__':
    (data) = start(config)
    startJob(config, data)
