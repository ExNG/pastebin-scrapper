#!/usr/bin/python
import os
import time
import urllib2
from bs4 import BeautifulSoup
import datetime


scriptDir = os.path.dirname(os.path.realpath(__file__))
config = {
    'path': os.path.join(scriptDir, 'data'),
    'pastebinarchive': 'https://pastebin.com/archive',
    'pastebin': 'https://pastebin.com',
    'timeout': 30
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

        # print('-> pasteIds', pasteIds)

        for pasteId in pasteIds:
            html = urllib2.urlopen(config['pastebin'] + pasteId).read()
            soup = BeautifulSoup(html, 'html.parser')

            content = str(soup.textarea.string.encode('utf-8'))
            hash = str.__hash__(content)

            title = soup.find("div", {"class": "paste_box_line1"}).get('title').encode('utf-8')

            if hash not in data:
                print('--> New Hash: ' + str(hash))
                addData(config, title, content, hash)
                data.append(hash)

        print('-> Done')
        print('-> Waiting: ' + str(config['timeout']) + ' seconds')
        time.sleep(config['timeout'])


def addData(config, title, content, hash):
    now = datetime.datetime.now()

    year = now.year
    month = '{:02d}'.format(now.month)
    day = '{:02d}'.format(now.day)

    hour = '{:02d}'.format(now.hour)
    minute = '{:02d}'.format(now.minute)
    second = '{:02d}'.format(now.second)

    date = str(year) + '-' + str(month) + '-' + str(day)
    time = str(hour) + ':' + str(minute) + ':' + str(second)

    filename = str(date) + '_' + str(time) + '_' + str(hash) + '_' + str(title) + '.txt'

    filePath = os.path.join(config['path'], filename)

    if os.path.isfile(filePath) is False:
        file = open(filePath, 'w')
        file.write(content)
        file.close()


if __name__ == '__main__':
    (data) = start(config)
    startJob(config, data)
