import os
import re
from Crypto.Util.Padding import pad
from concurrent.futures import ThreadPoolExecutor
from Crypto.Cipher import AES
import requests
import m3u8
from tqdm import tqdm

# 以下为可修改部分
# 请按F12打开开发者选项，进入浏览器network视图，筛选m3u8，并右键复制地址，粘贴在下方单引号内
url = "https://livingapihqy.pku.edu.cn/play/harpocrates/..../playlist.m3u8"
# 请按F12打开开发者选项，进入控制台，输入document.cookie,复制所有输出，粘贴在下方单引号内
cookie = "JSESSIONID=BEB640A45044D2F4ED4A5D4E......9%26sub_id%3D5...9"
# 存储名称，随便改
name = "Lesson.mp4"


# 修改部分结束

def decrypt(cipher_text, key, iv):
    cipher_text = pad(data_to_pad=cipher_text, block_size=AES.block_size)
    aes = AES.new(key=key, mode=AES.MODE_CBC, iv=key)
    cipher_text = aes.decrypt(cipher_text)
    return cipher_text


def down_thread(url, key, i):
    r = requests.get(url, headers=headers, timeout=5)
    data = r.content
    data = decrypt(data, key=key, iv=key)
    tsid = os.path.basename(url)
    with open(f"tmp/{tsid}", "ab") as ts:
        ts.write(data)
    print(f"\r{tsid} Downloaded ", end="  ")
    
def auto_name(save_name):
    pattern = "(\d+)\)\."
    while os.path.isfile(save_name):
        if re.search(pattern, save_name) is None:
            save_name = save_name.replace(".", "(1).") if os.path.exists(save_name) else save_name
        else:
            current_number = int(re.findall(pattern, save_name)[-1])
            new_number = current_number + 1
            save_name = save_name.replace(f"({current_number}).", f"({new_number}).")
    return save_name


def down(real_url, save_name):
    if not os.path.exists("tmp"):
        os.mkdir("tmp")
    playlist = m3u8.load(uri=real_url, headers=headers)
    key = requests.get(playlist.keys[-1].uri, headers=headers, timeout=5).content
    save_name = auto_name(save_name)
    n = len(playlist.segments)
    print(f"{n} segments detected")
    with ThreadPoolExecutor(max_workers=16) as pool:
        for i, seg in enumerate(playlist.segments):
            pool.submit(down_thread, seg.absolute_uri, key, i)
            

    with open(save_name, "wb") as fw:
        files = os.listdir("tmp")
        files.sort(key=lambda x: int(x.split(".")[0][8:]))
        with tqdm(total=n, desc="0") as pbar:
            for file in files:
                with open("tmp/" + file, "rb") as fr:
                    fw.write(fr.read())
                    pbar.set_description(f"\r {file} processed，Progress")
                    pbar.update(1)
                os.remove("tmp/" + file)
    if not os.listdir("tmp"):
        os.rmdir("tmp")
    print(f"\r{save_name} download successful. Directory:", end="     ")
    
size=0
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/73.0.3683.75 Chrome/73.0.3683.75 Safari/537.36",
    "Cookie": cookie,
}
down(url, name)
