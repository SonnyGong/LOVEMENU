# PyCharm 变量语法
"""
@file    func.py
@brief   
@details 

@author  nottoday <776038371@qq.com>
@version v1.0.0
@date    2025/4/21
@license MIT (See LICENSE in project root)

@history 
@depends 
"""
import os
from pathlib import Path
import streamlit as st
import pandas as pd
from BarkNotificator import BarkNotificator


def get_image_files(directory):
    # 定义常见的图片扩展名
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp'}
    pic_name = []
    pic_path = []
    # 使用 pathlib 遍历目录及其子目录
    img_dict = {}
    for img_path in Path(directory).rglob('*'):
        if img_path.is_file() and img_path.suffix.lower() in image_extensions:
            # 获取文件名（不含扩展名）和相对路径
            img_name = img_path.stem
            # img_relative_path = os.path.relpath(img_path, start=directory)
            pic_name.append(img_name)
            pic_path.append(img_path)
    return pic_name,pic_path


# 添加按钮的回调函数
def add_to_table(var1, var2):
    if var1 and var2:
        new_row = pd.DataFrame([[var1, var2, False]], columns=['时间', '下单的菜', '_delete'])
        st.session_state.table_data = pd.concat([st.session_state.table_data, new_row], ignore_index=True)
        # 这里可以添加打印语句，检查添加后的 st.session_state.table_data
        print("添加菜品后 st.session_state.table_data:", st.session_state.table_data)

def notice(message):
    bark = BarkNotificator(device_token="###")###内填入自己的token
    print(message)
    #
    bark.send(title="传菜系统", content=message)

# 方法一：使用 iterrows() 遍历（推荐用于数据量小的情况）
def chuancai(table):
    return_message = "传小X旨意：\n"
    for index, row in table.iterrows():
        time = row['时间']
        menu = row['下单的菜']
        return_message += f"{time} 下单了 {menu}\n"
    return_message += "一级响应！赶紧去买菜！快快快！动起来！！！\n"
    notice(return_message)
