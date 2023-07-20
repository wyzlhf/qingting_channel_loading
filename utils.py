import os

import bs4
import requests
from bs4 import ResultSet


def get_channel_name(channel_id: str) -> str:
    channel_url: str = f'https://www.qtfm.cn/channels/{channel_id}'
    channel_page_response: requests.api = requests.get(channel_url)
    soup: bs4.BeautifulSoup = bs4.BeautifulSoup(channel_page_response.text, 'lxml')
    titles: ResultSet = soup.find_all('h1', class_='title')
    title: str = titles[0].text
    title = title.split('-')[0]
    return title


def create_folder(folder_name: str, base_path: str = None) -> str:
    if base_path:
        folder_path: str = base_path + '/' + folder_name
        try:
            os.mkdir(folder_path)
            return folder_path
        except Exception as e:
            print('創建文件時發生錯誤，請檢查是否存在同名文件，錯誤原因為：',e)
    else:
        try:
            os.mkdir(folder_name)
            return folder_name
        except Exception as e:
            print('創建文件時發生錯誤，請檢查是否存在同名文件，錯誤原因為：',e)


if __name__ == '__main__':
    # title=get_channel_name(str(353596))
    # print(title)
    create_folder('全書','D:\CODE\PYTHON\\')