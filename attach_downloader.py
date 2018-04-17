import vk
import requests

from time import *
from random import choice
from string import digits


auth_token = ''
vk_api = ''
links = []


def main():
    create_session(auth_token)
    sleep(1)
    get_dialogs()
	
	
def generating_names():
    return ''.join(choice(digits) for i in range(12))
	
	
def download_images(url):
    img = requests.get(url)
    out = open(generating_names() + ".jpg", "wb")
    out.write(img.content)
    out.close()
	

def create_session(auth_token):
    global vk_api
    vk_session = vk.Session(auth_token)
    vk_api = vk.API(vk_session)
	
	
def get_dialogs():
    result = vk_api.messages.getHistoryAttachments(peer_id=138378862, media_type="photo", start_from="344850", count=200, v=5.69)
    for i in range(len(result['items'])):
        if('photo_2560' in result['items'][i]['attachment']['photo']):
            links.append(result['items'][i]['attachment']['photo']['photo_2560'])
        elif('photo_1280' in result['items'][i]['attachment']['photo']):
            links.append(result['items'][i]['attachment']['photo']['photo_1280'])
        elif('photo_807' in result['items'][i]['attachment']['photo']):
            links.append(result['items'][i]['attachment']['photo']['photo_807'])
        elif('photo_604' in result['items'][i]['attachment']['photo']):
            links.append(result['items'][i]['attachment']['photo']['photo_604'])
        if(i > (len(result['items']) - 5)):
            print(result['items'][i]['message_id'])
    for i in links:
        download_images(i)
    print("Загрузка завершена.")


if __name__ == "__main__":
    main()
