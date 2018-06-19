import vk
import datetime
from time import *
from config import *
import random
import requests

vkApi = ''

def main():
    getSession(authToken)
    sleep(1)
    while(True):
        #try:
            sendComment(groupId, postId, postText[random.randint(0, len(postText) - 1)], imgForComment)
            getFriend()
            print(datetime.datetime.now())
            sleep(1799)
        #except BaseException:
            #getSession(authToken)
            #print("Error")
            #continue
        

def getSession(authToken):
    global vkApi
    vkSession = vk.Session(authToken) 
    vkApi = vk.API(vkSession)
    return vkApi


#def getPosts(owner_id, count):
    #response = vkApi.wall.get(owner_id = owner_id, count = count)[1]['from_id']
    #return response


def getFriend():
    request = vkApi.friends.getRequests(out = 0)
    for i in request:
        vkApi.friends.add(user_id = i)
        sleep(1)


#def sendPost(owner_id, message):
    #vkApi.wall.post(owner_id = owner_id, message = message)


def sendComment(owner_id, post_id, message, attachments):
    vkApi.wall.createComment(owner_id = owner_id, post_id = post_id, message = message, attachments = attachments)


if __name__ == '__main__':
    main()
