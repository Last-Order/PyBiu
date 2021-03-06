#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @author:Hieda no Chiaki <i@wind.moe>

import codecs
import json
import logging
import os
import sys
from src.init import system

logging.basicConfig(level=logging.INFO)


def getID3(file):
    """获取音乐文件的ID3"""
    if system() == "Windows":
        f = os.path.split(os.path.realpath(__file__))[0] + "\media.json"
        cmd = r"cd src\win & ffprobe -v quiet -print_format json -show_format " + file + " > " + f
        # reload(sys)
        # sys.setdefaultencoding("utf-8")

        # tf = codecs.open('./src/tmp.txt','w','utf-8')
        # txt = unicode(cmd, 'utf-8')
        # tf.write(txt)
        # cmd = tf.read()
        # tf.close()

        os.system(cmd) # 处理编码  新函数负责写入文件
        temp_file = codecs.open(f, 'rb', 'utf-8')
    else:
        # f = os.path.split(os.path.realpath(__file__))[0] + "/media.json"
        # file = file[1:-1]
        # file = os.path.split(file)
        # # logging.info("-》"+file)
        cmd = "ffprobe -v quiet -print_format json -show_format " + file + " > " + "./src/media.json"
        os.system(cmd)
        temp_file = codecs.open('./src/media.json', 'rb', 'utf-8')
    tmp_json = temp_file.read()
    temp_file.close()
    s = json.loads(tmp_json)
    flag = 1
    try:
        bit_rate = int(s['format']['bit_rate'])
        format_name = s['format']['format_name']
        if format_name == "mp3" and bit_rate / 1000 < 300:
            return "", "", "", 0
        elif format_name == "aac" and bit_rate / 1000 < 200:
            return "", "", "", 0
        elif format_name in ["flac", "ape", "wav", "tta", "tak", "alac"]:
            pass
    except KeyError:
        return "", "", "", 0
    # 使用两层异常捕获来获取可能的大小写格式
    try:
        title = s['format']['tags']['title']
    except KeyError:
        try:
            title = s['format']['tags']['TITLE']
        except KeyError:
            return "", "", "", 2

    try:
        artist = s['format']['tags']['artist']
    except KeyError:
        try:
            artist = s['format']['tags']['ARTIST']
        except KeyError:
            artist = ""

    try:
        album = s['format']['tags']['album']
    except KeyError:
        try:
            album = s['format']['tags']['ALBUM']
        except KeyError:
            album = ""

    return title, artist, album, flag


if __name__ == "__main__":
    pass
