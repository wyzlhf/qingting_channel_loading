import json

import requests
from browsermobproxy import Server
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from utils import create_folder, get_channel_name


class AudioLoader(object):
    def __init__(self, channel_id: str, program_id: str):
        self.channel_id: str = channel_id
        self.program_id: str = program_id
        self.program_url: str = f'https://m.qtfm.cn/vchannels/{self.channel_id}/programs/{self.program_id}/'

    def get_actual_audio_url(self) -> str:
        BMPserver = Server(r'C:\Program Files\browsermob-proxy-2.1.4\bin\browsermob-proxy.bat')
        BMPserver.start()
        BMPproxy = BMPserver.create_proxy()

        # 配置代理启动webdriver
        chrome_options = Options()
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--proxy-server={}'.format(BMPproxy.proxy))

        driver = webdriver.Chrome(options=chrome_options)
        BMPproxy.new_har("video", options={'captureContent': True, 'captureContent': True})
        driver.get(self.program_url)

        dict_data: dict = BMPproxy.har
        json_data: str = json.dumps(dict_data)
        python_dict_data: dict = json.loads(json_data)
        # entries:list=python_dict_data['log']['entries']
        entries: list = python_dict_data.get('log', '没有log数据').get('entries', '没有entries数据')
        actual_audio_url_list: list = []
        for item in entries:
            # url=item['request']['url']
            url = item.get('request', '没有request数据').get('url', '没有url数据')
            if 'https://hwod-sign.qtfm.cn/m4a/' in url:
                actual_audio_url_list.append(url)
        if len(actual_audio_url_list) == 0:
            print('好像出错了')
        else:
            return actual_audio_url_list[0]

        # for i in range(len(entries) - 1, -1, -1):
        #     # url=item.get('request','没有request数据').get('url','没有url数据')
        #     actual_audio_url = entries[i].get('request', '没有request数据').get('url', '没有url数据')
        #     if 'https://hwod-sign.qtfm.cn/m4a/' in actual_audio_url:
        #         break
        #     print(actual_audio_url)
        #     return entries[i-1]['request']['url']
        #         # break

        BMPserver.stop()
        driver.quit()

    def load_audio_and_write(self, audio_url: str,audio_name:str,write_path:str=None)->None:
        audio_response=requests.get(audio_url)
        if write_path:
            audio_path_and_name:str=write_path+'\\'+audio_name+'.m4a'
        else:
            audio_path_and_name: str = audio_name + '.m4a'
        with open(audio_path_and_name,'wb') as f:
            f.write(audio_response.content)


if __name__ == '__main__':
    audio_loader = AudioLoader(str(353596), str(14664144))
    # actual_audio_url = audio_loader.get_actual_audio_url()
    # print(actual_audio_url)

    audio_url='https://hwod-sign.qtfm.cn/m4a/5e8ca251d93ae56daab7b5ac_16198450_24.m4a?auth_key=64ba4728-143846-0-3447ead912a30b25dfe23afb120fcb85'
    audio_loader.load_audio_and_write(audio_url,'aaa','D:\CODE\PYTHON')
