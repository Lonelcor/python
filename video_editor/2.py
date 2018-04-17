import moviepy.video.fx.all as vfx
import moviepy
from moviepy.editor import *

items = []


def parse_list(filename):
    f = open(filename)
    for item in f:
        item = item.strip().split(' ')
        item[1] = int(item[1].split(':')[0]) * 60 + int(item[1].split(':')[1])
        items.append(item)


def creating_content(name, time):
    video = VideoFileClip(name + '.mp4')
    gif = video.subclip((time), (time + 5)).resize(0.5)
    video = video.subclip((10), (-10)).fx(vfx.mirror_x)
    width, height = video.size
    size = width / 20 / 100
    txt_video = TextClip('vk.com/fullvid', fontsize=72, stroke_width=2, 
                         color='white', stroke_color='black').resize(size).set_opacity(0.75)\
                         .set_pos((10, 5)).set_duration(video.duration)
    txt_gif = TextClip('vk.com/fullvid', fontsize=72, stroke_width=2, 
                       color='white', stroke_color='black').resize(size * 0.8).set_opacity(0.75)\
                       .set_pos((10, 5)).set_duration(gif.duration)
    final_video = CompositeVideoClip([video, txt_video])
    final_gif = CompositeVideoClip([gif, txt_gif])
    final_video.write_videofile('f_' + name + '.mp4', threads=3)
    final_gif.write_gif(name + '.gif', fps=10)
    video.audio.reader.__del__()
    video.audio.__del__()
    video.reader.__del__()
    video.__del__()
    
        
def main():
    parse_list('render.txt')
    for i in items:
        creating_content(i[0], i[1])
    

if __name__ == '__main__':
    main()