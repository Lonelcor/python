import requests
import vk

authToken = '6f9be692be84c7d1df7e4bfddff816aaf8eb59c85808dab6cc4fb88b609fc4896429a9c04252ad1a805f5'
items = []


def parse_list(filename):
    f = open(filename)
    for item in f:
        items.append(item[:-1])


def create_session(authToken):
    global vkApi
    vkSession = vk.Session(authToken) 
    vkApi = vk.API(vkSession)
    return vkApi


def upload_files(i):
    response = vkApi.video.save(name="vk.com/fullvid", description="Фуллы от Деда (vk.com/fullvid)", wallpost=0, group_id=142936678, v=5.73)
    requests.post(response["upload_url"], files={"video_file": open(i + ".mp4", "rb")})
    response = vkApi.docs.getUploadServer(group_id=142936678, v=5.73)
    response = requests.post(response["upload_url"], files={"file": open(i + ".gif", "rb")})
    response = vkApi.docs.save(file=response.json()["file"], title="vk.com/fullvid", v=5.73)

        
def main():
    parse_list('upload.txt')
    create_session(authToken)
    for i in items:
        upload_files(i)
    
	
if __name__ == '__main__':
    main()