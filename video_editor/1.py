import requests
from random import choice
from string import digits

links = []


def generating_names():
    return ''.join(choice(digits) for i in range(6))


def parse_links(filename):
    f = open(filename)
    for link in f:
        links.append(link)

    
def download_video(url):
    response = requests.get(url, stream=True)
    with open(generating_names() + '.mp4', 'wb') as fd:
        for chunk in response.iter_content(chunk_size=128):
            fd.write(chunk)


def main():
    parse_links('download.txt')
    for i in links:
        download_video(i)
    
	
if __name__ == '__main__':
    main()