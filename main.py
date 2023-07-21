import copy
import json
import random
import time
from typing import List
import os

from get_all_pages_url_in_channel import ChannelItemLoader
from get_audio import AudioLoader


# def get_all_audios_in_channel(channel_id:str)->None:
# channel_item_loader:ChannelItemLoader = ChannelItemLoader(channel_id)

# all_program_in_a_channel:dict = channel_item_loader.get_all_programs()
# complete_program_list:list=[]

# all_programs_url:List=all_program_in_a_channel['all_programs_url']
# for item in all_programs_url:
#     program_id=item['id']
#     program_name:str=item['title']
#     AudioLoader(channel_id,program_id,program_name)
#     sleep_time=random.randint(2,6)
#     print(f'完成{program_name}下载，当前进度为{all_programs_url.index(item)+1}/{len(all_programs_url)}')
#     time.sleep(sleep_time)

# with open('all_program_in_a_channel.json', 'w') as f:
#     f.write(json.dumps(all_program_in_a_channel))
#
# with open('all_program_in_a_channel.json', 'w')as f:
#     all_program_in_a_channel_json=f.read()
# all_program_in_a_channel_dict=json.loads(all_program_in_a_channel_json)
# all_programs_url=all_program_in_a_channel_dict['all_programs_url']
# for item in all_programs_url:
#     # if os.path.exists('')
#     program_id=item['id']
#     program_name:str=item['title']
#     AudioLoader(channel_id,program_id,program_name)
#     sleep_time=random.randint(2,6)
#     print(f'完成{program_name}下载，当前进度为{all_programs_url.index(item)+1}/{len(all_programs_url)}')
#     with open('completed.txt','a')as f:
#         f.write(program_id)
#     time.sleep(sleep_time)
def get_all_programs_info_write_to_json(channel_id: str) -> None:
    channel_item_loader: ChannelItemLoader = ChannelItemLoader(channel_id)
    all_program_in_a_channel: dict = channel_item_loader.get_all_programs()
    with open('all_program_in_a_channel.json', 'w') as f:
        f.write(json.dumps(all_program_in_a_channel))
    print('写入channel programs information成功！')


def load_programs_in_channel_json(json_path: str) -> None:
    with open(json_path, 'r')as f:
        all_programs_info_json = f.read()
    all_programs_info_dict: dict = json.loads(all_programs_info_json)
    all_programs_url: list = all_programs_info_dict['all_programs_url']
    all_programs_url_copied:list=copy.deepcopy(all_programs_url)
    channel_id: str = all_programs_info_dict['channel_id']
    if len(all_programs_url)!=0:
        try:
            for item in all_programs_url:
                program_id = item['id']
                program_name: str = item['title']
                AudioLoader(channel_id, program_id, program_name)
                all_programs_url_copied.pop(all_programs_url_copied.index(item))
                sleep_time = random.randint(2, 6)
                print(f'完成{program_name}下载，当前进度为{all_programs_url.index(item) + 1}/{len(all_programs_url)}')
                time.sleep(sleep_time)
                # all_programs_url.pop(all_programs_url.index(item))
                # all_programs_info_dict['all_programs_url'] = all_programs_url
                # with open(json_path, 'w')as f:
                #     f.write(json.dumps(all_programs_info_dict))
        except Exception as e:
            print('遇到错误了，请重启继续，错误原因为：',e)
        finally:
            all_programs_info_dict['all_programs_url'] = all_programs_url_copied
            with open(json_path, 'w')as f:
                f.write(json.dumps(all_programs_info_dict))
                print('json文件重新写入完成')
    else:
        print('没有等待下载的任务了')



if __name__ == '__main__':
    # get_all_programs_info_write_to_json('353596')
    load_programs_in_channel_json('all_program_in_a_channel.json')
