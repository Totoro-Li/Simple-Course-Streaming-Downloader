import os
import re
import time
from Crypto.Util.Padding import pad
from Crypto.Cipher import AES
import requests
import m3u8
from tqdm import tqdm

# 以下为可修改部分
# 请按F12打开开发者选项，进入浏览器network视图，筛选m3u8，并右键复制地址，粘贴在下方单引号内
url = 'https://livingapihqy.pku.edu.cn/play/harpocrates/....../playlist.m3u8'
# 请按F12打开开发者选项，进入控制台，输入document.cookie,复制所有输出，粘贴在下方单引号内
cookie = 'JSESSIONID=9747AA82........'
# 存储名称，随便改
name = 'Lesson.mp4'


# 修改部分结束

def AESDecrypt(cipher_text, key, iv):
    cipher_text = pad(data_to_pad=cipher_text, block_size=AES.block_size)
    aes = AES.new(key=key, mode=AES.MODE_CBC, iv=key)
    cipher_text = aes.decrypt(cipher_text)
    return cipher_text


def auto_name(save_name):
    pattern = '(\d+)\)\.'
    while os.path.isfile(save_name):
        if re.search(pattern, save_name) is None:
            save_name = save_name.replace('.', '(1).') if os.path.exists(save_name) else save_name
        else:
            current_number = int(re.findall(pattern, save_name)[-1])
            new_number = current_number + 1
            save_name = save_name.replace(f'({current_number}).', f'({new_number}).')
    return save_name


def down(real_url, save_name):
    playlist = m3u8.load(uri=real_url, headers=headers)
    key = requests.get(playlist.keys[-1].uri, headers=headers).content
    save_name = auto_name(save_name)
    n = len(playlist.segments)
    size = 0
    start = time.time()
    with tqdm(total=n, desc='0') as pbar:
        for i, seg in enumerate(playlist.segments, 1):
            r = requests.get(seg.absolute_uri, headers=headers)
            data = r.content
            data = AESDecrypt(data, key=key, iv=key)
            size += len(data)
            with open(save_name, "ab" if i != 1 else "wb") as f:
                f.write(data)
            pbar.update(1)
            pbar.set_description(f"\r Downloaded:{size / 1024 / 1024:.2f}MB，Progress:")
        print(f'\r{save_name}download success.Total size:{size / 1024 / 1024:.2f}MB', end="     ")


headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/73.0.3683.75 Chrome/73.0.3683.75 Safari/537.36',
    'Cookie': cookie,
}
down(url, name)
