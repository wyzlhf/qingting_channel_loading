from typing import List

from get_all_pages_url_in_channel import ChannelItemLoader
from get_audio import AudioLoader

def get_all_audios_in_channel(channel_id:str)->None:
    chanel_item_loader:ChannelItemLoader = ChannelItemLoader(channel_id)

    all_program_in_a_channel:dict = chanel_item_loader.get_all_programs()
    all_programs_url:List=all_program_in_a_channel['all_programs_url']
    for item in all_programs_url:
        program_id=item['id']
        program_name:str=item['title']
        audio_loader: AudioLoader = AudioLoader(channel_id,program_id,program_name)
if __name__ == '__main__':
    get_all_audios_in_channel('353596')