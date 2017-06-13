from PIL import Image
import glob

for i in glob.glob('image/*'):
    img = Image.open(i)
    img.resize((img.size[0] // 4, img.size[1] // 4))
    img.save(i)