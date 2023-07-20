import re
import json
from typing import List, Dict

import bs4
import requests
from bs4 import BeautifulSoup
from requests import Response

'''
最后获取的channel && programs的字典格式如下：

all_program_in_a_channel: Dict = {
    'channel_id': 12345,
    'all_programs_url': [
        {'program_id': 45678,'program_name': '音频标题'},
        {'program_id': 45679,'program_name': '音频标题'},
    ]
}

'''


class ChannelItemLoader(object):
    def __init__(self, channel_id:str):
        self.channel_fist_page_url: str = 'https://www.qtfm.cn/channels/' + str(channel_id)
        self.channel_id: str = channel_id
        self.page_number: int = self.get_channel_page_num()
        self.version: str = self.get_channel_version_field()

    # 每个页面获取一个soup，方便使用
    def get_page_soup(self, page_url) -> BeautifulSoup:
        response_text: str = requests.get(page_url).text
        soup: BeautifulSoup = BeautifulSoup(response_text, 'lxml')
        return soup

    # 获取一个channel中容纳所有节目的页码，就是最底下那个翻页组件
    def get_channel_page_num(self) -> int:
        soup: BeautifulSoup = self.get_page_soup(self.channel_fist_page_url)
        pagination_div: bs4.element.Tag = soup.find_all('ul', class_='pagination')[0]
        get_last_page_li: bs4.element.Tag = pagination_div.find_all("li")[-2]
        page_num: int = int(get_last_page_li.text)
        return page_num

    # 每个channel有一个version字段，根据这个字段可以拼出获取所有program json信息的URL
    def get_channel_version_field(self) -> str:
        version_url: str = f'https://i.qtfm.cn/capi/v3/channel/{self.channel_id}?user_id=null'
        version_response: Response = requests.get(version_url)
        json_version_response: str = version_response.text
        dict_version_response: dict = json.loads(json_version_response)
        version: str = dict_version_response['data']['v']
        return version

    # 获取一个单一页面中，比如第一页所包含的page的URL，但是是主要想获取program的ID
    def get_programs_json_in_onepage(self, page_num:int) -> List:
        program_info_json_url: str = f'https://i.qtfm.cn/capi/channel/{self.channel_id}/programs/{self.version}?curpage={page_num}&pagesize=30&order=asc'
        program_info_json_response: Response = requests.get(program_info_json_url)
        program_info_json_text: str = program_info_json_response.text
        program_info_json_dict: Dict = json.loads(program_info_json_text)
        # programs_json:List=program_info_json_dict['data']['programs']
        programs_json: List = program_info_json_dict.get('data', '没有data数据').get('programs', '没有programs数据')
        # return programs_json
        return programs_json

    # 获取一个channel中所有program的ID，并组成all_program_in_a_channel的字典
    def get_all_programs(self) -> Dict:
        all_program_in_a_channel: Dict = {}
        all_program_in_a_channel['channel_id'] = self.channel_id
        all_programs_url: List = []
        for page_num in range(self.page_number):
            programs_json = self.get_programs_json_in_onepage(page_num+1)
            all_programs_url.extend(programs_json)
        all_program_in_a_channel['all_programs_url'] = all_programs_url
        return all_program_in_a_channel


if __name__ == '__main__':
    # channel_url = 'https://www.qtfm.cn/channels/353596'#
    # channel_url='https://www.qtfm.cn/channels/353596/2'
    # get_all_audio_page_urls(channel_url)
    # get_channel_page_num(channel_url)

    chanel_item_loader = ChannelItemLoader(str(353596))
    # programs_json=chanel_item_loader.get_programs_json_in_onepage(1)
    # for i in programs_json:
    #     print(i)

    all_program_in_a_channel = chanel_item_loader.get_all_programs()
    for item in all_program_in_a_channel['all_programs_url']:
        print(item)
