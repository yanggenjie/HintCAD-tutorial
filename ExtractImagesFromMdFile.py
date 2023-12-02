import misaka
import os
import requests
import uuid
from bs4 import BeautifulSoup
import urllib
import shutil

def get_files_list(dir):
    """
    获取一个目录下所有文件列表，包括子目录
    :param dir:
    :return:
    """
    files_list = []
    for root, dirs, files in os.walk(dir, topdown=False):
        for file in files:
            if(file.endswith('.md')):
                files_list.append(os.path.join(root, file))

    return files_list


def get_pics_list(md_content):
    """
    获取一个markdown文档里的所有图片链接
    :param md_content:
    :return:
    """
    md_render = misaka.Markdown(misaka.HtmlRenderer())
    html = md_render(md_content)
    soup = BeautifulSoup(html, features='html.parser')
    pics_list = []
    for img in soup.find_all('img'):
        imgSrc=img.get('src')
        parseQuote= urllib.parse.unquote(imgSrc)
        pics_list.append(parseQuote)

    return pics_list

def create_dir_not_exist(path):
    if not os.path.exists(path):
        os.mkdir(path)

def download_pics(url, file):
    img_data = requests.get(url).content
    filename = os.path.basename(file)
    dirname = os.path.dirname(file)
    targer_dir = os.path.join(dirname, f'{filename}.assets')
    if not os.path.exists(targer_dir):
        os.mkdir(targer_dir)

    with open(os.path.join(targer_dir, f'{uuid.uuid4().hex}.jpg'), 'w+') as f:
        f.buffer.write(img_data)

rootdir=os.path.dirname(__file__)
def MoveToIndependentDir(piclist,fileName):
    for p in piclist:
        srcImg=rootdir+"\\"+p.replace('./','').replace('/',"\\")
        imgName=os.path.basename(srcImg)
        tarDir=rootdir+"\\"+fileName
        tarfile=tarDir+"\\"+imgName
        if not os.path.exists(tarfile):
            create_dir_not_exist(tarDir)
            if os.path.exists(srcImg):
                shutil.move(srcImg,tarfile)
                print("移动"+imgName)
        

if __name__ == '__main__':
    files_list = get_files_list(rootdir)

    for file in files_list:
        with open(file, encoding='utf-8') as f:
            md_content = f.read()
        pics_list = get_pics_list(md_content)
        dirName,ext=os.path.splitext(file)
        fileName=dirName.split("\\")[-1]
        if(len(pics_list)>0):
            print(f'发现图片 {len(pics_list)} 张')
            MoveToIndependentDir(pics_list,fileName)
    print(f'处理完成。')