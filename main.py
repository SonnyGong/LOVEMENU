# PyCharm 变量语法
"""
@file    main.py
@brief   
@details 

@author  nottoday <776038371@qq.com>
@version v1.0.0
@date    2025/4/21
@license MIT (See LICENSE in project root)

@history 
@depends 
"""
import base64
import os

import pandas as pd
import streamlit as st
from streamlit_image_select import image_select

from func import get_image_files, add_to_table, chuancai

from datetime import datetime

def get_timestamp(fmt="%Y-%m-%d %H:%M:%S"):
    """返回当前时间的格式化字符串"""
    return datetime.now().strftime(fmt)




# 初始化 session_state 存储表格数据
if 'table_data' not in st.session_state:
    st.session_state.table_data = pd.DataFrame(columns=['时间', '下单的菜','_delete'])
# 移动端优化CSS
st.markdown("""
<style>
/* 隐藏默认复选框列 */
[data-testid="stDataFrame"] thead th:first-child {
    display: none !important;
}

/* 调整操作列宽度 */
[data-testid="stDataFrame"] td:nth-child(1) {
    width: 80px !important;
    text-align: center !important;
}

/* 移动端按钮样式 */
@media (max-width: 600px) {
    [data-testid="stDataFrame"] td:nth-child(1) button {
        padding: 4px 8px !important;
        font-size: 12px !important;
    }
}
</style>
""", unsafe_allow_html=True)

def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

image_base64 = get_base64_image("back/title.webp")

st.markdown(
    f"""
        <style>
       .fullscreen-title {{
            background: url('data:image/png;base64,{image_base64}');
            background-size: cover;
            height: 40vh;  /* 使用相对单位 vh，根据视口高度调整 */
            width: 90vw;  /* 使用相对单位 vw，根据视口宽度调整 */
            max-width: 700px;  /* 设置最大宽度，避免在大屏幕上过大 */
            margin: 0 auto;  /* 水平居中 */
            position: relative;  /* 确保子元素可以相对于这个元素定位 */
        }}
       .fullscreen-title h1 {{
            position: absolute;
            bottom: 10px;  /* 调整这个值来控制标题离图片底部的距离 */
            left: 0;
            right: 0;
            text-align: center;
            color: white;
            font-style: italic;  /* 设置字体为斜体 */
            text-shadow: 
                -1px -1px 0 #000,  
                 1px -1px 0 #000,
                -1px  1px 0 #000,
                 1px  1px 0 #000; /* 实现黑色描边效果 */
        }}
        /* 媒体查询，针对小屏幕设备（如手机）进一步调整样式 */
        @media (max-width: 600px) {{
           .fullscreen-title {{
                height: 30vh;
                width: 95vw;
            }}
        }}
        </style>
        <div class="fullscreen-title">
            <h1>小Xの深夜食堂</h1>
        </div>
    """,
    unsafe_allow_html=True
)

pic_name,pic_path = get_image_files("pic")
st.divider()
st.subheader("👨‍🍳️:rainbow[欢迎光临！小X请点单～]")
st.divider()
if pic_name:
    img = image_select("", images=pic_path,captions=pic_name)
    # 获取文件名（包含扩展名）
    file_name_with_extension = os.path.basename(img)

    # 获取文件名（不包含扩展名）
    file_name_without_extension = os.path.splitext(file_name_with_extension)[0]
    if file_name_without_extension:
        st.write(f"您选择了：:rainbow[{file_name_without_extension}]  ,确认添加吗？")
        # 显示添加按钮
        st.button("添加", on_click=add_to_table,args=[get_timestamp(),file_name_without_extension])
        # print(st.session_state.table_data)
        # 显示表格
        st.divider()
        st.write("当前已经点的菜：")
        # 关键修改：捕获返回值
        edited_df = st.data_editor(
            st.session_state.table_data,
            column_config={
                "_delete": st.column_config.CheckboxColumn(
                    "删除",
                    help="勾选要删除的行",
                    default=False,
                    width="small"
                )
            },
            num_rows="dynamic",
            use_container_width=True,
            hide_index=True,
            key="data_editor"
        )

        # 删除操作处理
        col1, col2 = st.columns([0.7, 0.3])
        with col2:
            if st.button("🗑️ 执行删除", type="primary", disabled=not edited_df['_delete'].any()):
                edited_df['_delete'] = edited_df['_delete'].astype(bool)
                # 保留未删除的行
                print("编辑表格的 _delete 列的类型和内容：", edited_df['_delete'].dtype, edited_df['_delete'])
                new_df = edited_df[~edited_df['_delete']].copy()
                # 重置删除状态
                new_df['_delete'] = False
                # 更新数据
                st.session_state.table_data = new_df
                st.rerun()


    if len(st.session_state.table_data) > 0:
        if st.button("就这么多了，通知小X去准备吧",on_click=chuancai,args=[st.session_state.table_data]):
            st.write("已经通知后厨了，首席 cook 小X将为您一对一服务！请您耐心等待～")

