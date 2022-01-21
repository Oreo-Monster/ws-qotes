'''
Web scrapre for colleting all works of William Shakepeare

Taking from this handy site:
http://shakespeare.mit.edu/index.html

Going to dump everything into a JSON

'''

import requests
import re
import json

# Get a list of all the plays somehow, maybe from home page
# put in a list of dictionaries

home = requests.get(url='http://shakespeare.mit.edu/index.html').text
playHTML = re.findall('<a href=\"[\w]*\/\w*.html\">[\w \n\',.]*<\/a>', home)
playURL = re.findall('href="\w*\/\w*.html', home)
playTitles = re.findall('>[\w \n\',.]*<\/a>', home)
plays = []


for i in range(len(playTitles)):
    playURL[i] = playURL[i][6:]
    playObj = {
        'id':i,
        'name':re.sub('\n', '', playTitles[i][1:-4])
    }
    plays.append(playObj)

nextSpeakerID = 0
charNames = {}
characters= []
lines=[]
lineID = 0

for playID in range(len(plays)):
    if 'Poetry' not in playURL[playID]:
        
        url = f'http://shakespeare.mit.edu/{playURL[playID][:-11]}/full.html'
        html = requests.get(url=url).text
        aTags = re.findall('<A NAME=[\w.]+>.+', html)

        for a in aTags:
            lineCode = re.search('\d+\.\d+\.\d+', a)
            if lineCode is None:
                name = re.search('<b>.+<\/b>', a).group()[3:-4]
                if name in charNames:
                    currentSpeakerID = charNames[name]
                else:
                    charNames[name] = nextSpeakerID
                    charObj = {
                        'id':nextSpeakerID,
                        'name':name
                    }
                    characters.append(charObj)
                    currentSpeakerID = nextSpeakerID
                    nextSpeakerID += 1
            else:
                lineNums = re.findall('\d+', lineCode.group())
                content = re.search('>.+<\/A>', a).group()[1:-4]
                lineObj = {
                    'id':lineID,
                    'play_id':playID,
                    'speaker_id':currentSpeakerID,
                    'act':lineNums[0],
                    'scene':lineNums[1],
                    'line':lineNums[2],
                    'content':content
                }
                lines.append(lineObj)
                lineID += 1
    else:
        # handle poetry
        pass

json.dump(characters, open('characters.json', 'w'))
json.dump(lines, open('lines.json', 'w'))
json.dump(plays, open('plays.json', 'w'))


    