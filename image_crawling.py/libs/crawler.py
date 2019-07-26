import requests


def crawl(star_name):

    url = f'https://www.google.com/search?q={star_name}&tbm=isch'
    data = requests.get(url)
    print(data, url)
    return data.content
