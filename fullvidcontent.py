from moviepy.editor import *
import requests
import json
import vk

authToken = ''
vkApi = None


def main():
	video_url = input("Вставьте ссылку на видеоролик: ")
	print("Началось скачивание видеоролика...")
	download_file(video_url)
	print("Загрузка успешно завершена.")
	create_content()
	print("Обработка видеозаписи и создание GIF завершены.")
	create_session(authToken)
	print("Началась выгрузка во ВКонтакте!")
	upload_files()
	print("Выгрузка завершена. Готово!")


def download_file(video_url):
	file = requests.get(video_url, stream=True)
	with open("source.mp4", "wb") as fd:
		for chunk in file.iter_content(chunk_size=128):
			fd.write(chunk)


def create_content():
	start_t = input("Введите время начала GIF: ")
	end_t = input("Введите время конца GIF: ")
	video = VideoFileClip("source.mp4")
	gif = video.subclip(int(start_t), int(end_t)).resize(0.5)
	video = video.subclip(3, -3)
	textForVideo = TextClip("vk.com/fullvid", fontsize=70, color="white", font="Impact", interline=-25, stroke_width=3, stroke_color="black").set_opacity(0.5).set_pos((5, 2)).set_duration(video.duration).resize(height=35)
	textForGif = TextClip("vk.com/fullvid", fontsize=70, color="white", font="Impact", interline=-25, stroke_width=3, stroke_color="black").set_pos(("center", "bottom")).set_duration(gif.duration).resize(height=35)
	compositionVideo = CompositeVideoClip([video, textForVideo])
	compositionGif = CompositeVideoClip([gif, textForGif])
	compositionVideo.write_videofile("video.mp4")
	compositionGif.write_gif("gif.gif", fps = 10)


def create_session(authToken):
    global vkApi
    vkSession = vk.Session(authToken) 
    vkApi = vk.API(vkSession)
    return vkApi


def upload_files():
	response = vkApi.video.save(name="vk.com/fullvid", description="Фуллы от Деда (vk.com/fullvid)", wallpost=0, group_id=142936678)
	requests.post(response["upload_url"], files={"video_file": open("video.mp4", "rb")})
	response = vkApi.docs.getUploadServer(group_id=142936678)
	response = requests.post(response["upload_url"], files={"file": open("gif.gif", "rb")})
	response = vkApi.docs.save(file=response.json()["file"], title="vk.com/fullvid")


if __name__ == "__main__":
    main()
