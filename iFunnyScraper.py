import urllib.request
from bs4 import BeautifulSoup as soup
import json
import csv


def removeEmojis(arg):
    return (str((arg).encode('utf-8', 'ignore')))[1:]
    
homePageMemeList = []
memeList = []
# Go to the ifunny homepage and download source
homePage = 'https://ifunny.co/'
response = urllib.request.urlopen(homePage)
homePageHTML = response.read()
response.close()
homePageSOUP = soup(homePageHTML, "lxml")
keyword = "/fun"

# Find all memes on homepage
memes = homePageSOUP.findAll("a", {"class":"button button_common button_expanding button_facebook js-goalcollector-action js-statistics-action js-dwhcollector-action"})
print("{} memes were found on the homepage".format(len(memes)))

#Find first meme
firstMeme = str(memes[0])
firstMemeIndex= firstMeme.find(keyword)
firstMemeID = firstMeme[firstMemeIndex+5: firstMemeIndex + 14]
print("First meme ID: {}".format(firstMemeID))

#Get list of memes on front page
for index, val in enumerate(memes):
    memesStr = str(memes[index])
    kwIndex = memesStr.find(keyword)
    memeList.append(memesStr[index+5: index + 14])

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

nextMeme = firstMemeID
with open('iFunnyArchive.csv', mode='w') as trackWriter:
        trackWriter = csv.writer(trackWriter, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        trackWriter.writerow(['memeID', 'pageTitle', 'user', 'likes', 'source', 'type'])
        while counter < 100:
            counter+=1
            response = urllib.request.urlopen('https://ifunny.co/fun/{}'.format(nextMeme))
            memeHTML = response.read()
            response.close()
            memeHTML = memeHTML.decode("utf-8")

            # Find the title of the page. Basically finds the hashtags if there are any
            start = (str(memeHTML).find(pageTitleStart)) + len(pageTitleStart)
            for x in range(start, start+500):
                if memeHTML[x] == '<':
                    end = x
                    break
            titleText = memeHTML[start:end]
            
            # Find the user who created the meme
            start = (str(memeHTML).find(userStart)) + len(userStart)
            for x in range(start, start+500):
                if memeHTML[x] == '>':
                    end = x
                    break
            userText = memeHTML[start:end-1]

            # Determined whether the meme is an image or video
            if str(memeHTML).find(videoStart) == -1:
                start = str(memeHTML).find(imageStart) + len(imageStart) + 6
                typeText = 'image'
                for x in range(start, start+500):
                    if memeHTML[x] == '\"':
                        end = x
                        break
            else:
                start = str(memeHTML).find(videoStart) + len(videoStart) + 14
                typeText = 'video'
                for x in range(start, start + 500):
                    if memeHTML[x] == '\"':
                        end = x
                        break
            sourceText = memeHTML[start:end]

            # Find the likes and comments
            start = (str(memeHTML).find(likesStart)) + len(likesStart)
            for x in range(start, start+50):
                if memeHTML[x] == '<':
                    end = x
                    break
            likesText = memeHTML[start:end]

            start = (str(memeHTML[start+20:]).find(likesStart)) + len(likesStart)
            for x in range(start, start+300):
                if memeHTML[x] == '<':
                    end = x
                    break
            commentsText = memeHTML[start:end]
            print(str(commentsText))
            print("MEME {}: {}, {}, {}, {}, {}".format(counter, removeEmojis(nextMeme), removeEmojis(titleText), removeEmojis(userText), removeEmojis(likesText), removeEmojis(typeText)))
            trackWriter.writerow([removeEmojis(nextMeme), removeEmojis(titleText), removeEmojis(userText), removeEmojis(likesText), removeEmojis(sourceText), removeEmojis(typeText)])
            # if sourceText[-3:] == 'jpg' or sourceText[-3:] == 'png':
            #     urllib.request.urlretrieve(sourceText, '/home/marek/Desktop/Meme Archive/content/img/{}.jpg'.format(nextMeme))
            # elif sourceText[-3:] == 'mp4':
            #     urllib.request.urlretrieve(sourceText, '/home/marek/Desktop/Meme Archive/content/vid/{}.mp4'.format(nextMeme))
            index = str(memeHTML).find(nextStart) + len(nextStart) + 7
            nextMeme = memeHTML[index: index+9]



# Hashtags 
# <title>spicy, shitposting, edgy, tagwhore, Video - iFunny :)</title>

# Likes Comments
# first two tags class="actionlink__text

# User
# first href="/user/testUser"

# Getting Type and sources
# if data-type="video" get source video
    # data-type="video" data-source="https://img.ifcdn.com/videos/758e27e38f8942cc9530c8a15ebf0df13946ef840e73d0e0b85b89f139c3b249_1.mp4" data-trackback-uri=""  data-autoplay >
# else <img class="media__image"
    # <img class="media__image" src="https://img.ifcdn.com/images/05d01044ab9ed88543ba6a0c3783bbfee155e76a3da9754729fbfcbab24a60d6_1.jpg" alt="LOL!!! :) - iFunny :)">
