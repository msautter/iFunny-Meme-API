import urllib.request
from bs4 import BeautifulSoup as soup
import json
import csv


def removeEmojis(arg):
    return (str((arg).encode('utf-8', 'ignore')))[1:]

counter = 0
start = 0
end = 0

pageTitleStart = '<title>'
likesStart = 'class="actionlink__text'
userStart = 'href="/user/'
videoStart = 'data-type="video"'
imageStart = '<img class="media__image"'
likesStart = 'class="actionlink__text">'
nextStart = 'data-next-post'

# https://ifunny.co/fun/y5Cr6aT36
nextMeme = 'y5Cr6aT36'
with open('iFunnyArchive.csv', mode='w') as trackWriter:
    trackWriter = csv.writer(trackWriter, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    trackWriter.writerow(['memeID', 'pageTitle', 'user', 'likes', 'source', 'type'])
    while counter < 100:
        counter+=1
        response = urllib.request.urlopen('https://ifunny.co/fun/{}'.format(nextMeme))
        memeHTML = response.read()
        response.close()
        memeHTML = memeHTML.decode("utf-8")
        start = (str(memeHTML).find(pageTitleStart)) + len(pageTitleStart)
        for x in range(start, start+500):
            if memeHTML[x] == '<':
                end = x
                break
        titleText = memeHTML[start:end - 14]
        
        start = (str(memeHTML).find(userStart)) + len(userStart)
        for x in range(start, start+500):
            if memeHTML[x] == '>':
                end = x
                break
        userText = memeHTML[start:end-1]

        if str(memeHTML).find(videoStart) == -1:
            start = str(memeHTML).find(imageStart) + len(imageStart) + 6
            typeText = 'image'
            for x in range(start, start+500):
                if memeHTML[x] == '\"':
                    end = x
                    sourceText = memeHTML[start:end]
                    break
        else:
            start = str(memeHTML).find(videoStart) + len(videoStart) + 14
            typeText = 'video'
            for x in range(start, start + 500):
                if memeHTML[x] == '"':
                    end = x

                    break
        sourceText = memeHTML[start:end]

        start = (str(memeHTML).find(likesStart)) + len(likesStart)
        for x in range(start, start+50):
            if memeHTML[x] == '<':
                end = x
                break
        likesText = memeHTML[start:end]
        print("MEME {}: {}, {}, {}, {}, {}, {}".format(counter, removeEmojis(nextMeme), removeEmojis(titleText), removeEmojis(userText), removeEmojis(likesText), removeEmojis(sourceText), removeEmojis(typeText)))
        trackWriter.writerow([removeEmojis(nextMeme), removeEmojis(titleText), removeEmojis(userText), removeEmojis(likesText), removeEmojis(sourceText), removeEmojis(typeText)])
        print("HELLOOOOo")
        print(str(sourceText[-3:]))
        # if sourceText[-3:] == 'jpg' or sourceText[-3:] == 'png':
        #     print("I DID IT IMAGE")
        #     urllib.request.urlretrieve(sourceText, '/content/img/{}.jpg'.format(nextMeme))
        # elif sourceText[-3:] == 'mp4':
        #     print("I DID IT VIDEO")
        #     urllib.request.urlretrieve(sourceText, '/content/vid/{}.mp4'.format(nextMeme))
        index = str(memeHTML).find(nextStart) + len(nextStart) + 7
        nextMeme = memeHTML[index: index+9]
