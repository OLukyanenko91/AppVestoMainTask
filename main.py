import os
import cfscrape
import time
from bs4 import BeautifulSoup
from requests.exceptions import ConnectionError

DELAY = 2
URL = 'https://www.udemy.com/course/learn-flutter-dart-to-build-ios-android-apps'


def connect():
    time.sleep(DELAY)
    scraper = cfscrape.create_scraper()
    response = scraper.get(URL)

    return response


def getFreeVideoInfo(response):
    data = {}
    soup = BeautifulSoup(response.text, 'lxml')

    for div in soup.findAll('div', {'class': 'lecture-container'}):
        title = div.find('div', {'class': 'title'}).text.replace('\n', '')
        duration = div.find('span', {'class': 'content-summary'}).text.replace('\n', '')

        if div.find('a', {'data-purpose': 'preview-course'}):
            data[title] = duration

    data = {k: v for k, v in sorted(data.items(), key=lambda item: item[1])}

    return data


def main():
    try:
        response = connect()
        data = getFreeVideoInfo(response)
        videoTitles = data.keys()

        for title in videoTitles:
            print(title)
    except ConnectionError as error:
        print(error)


if __name__ == "__main__":
    main()
    os.system("pause")
