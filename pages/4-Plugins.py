import streamlit as st
import traceback
from utils import check_config_file_existence, read_config, write_config
from utils import get_plugins_list, get_plugin_type, plugins_path
import subprocess
import os
import shutil
import requests


def select_plugins_page():
    # 获取不同类型插件字典
    pass
    # TODO 等到插件数目较多时再写

def install_plugins_page():
    # 标题
    st.title(body="插件安装")
    st.markdown(body="<hr>", unsafe_allow_html=True)

    def official_plugins_page():
        # 获取github用户仓库列表
        api_url = "https://api.github.com/users/conversationpractice/repos"
        repositories_list = requests.post(api_url).json()
        for repository in repositories_list:
            pass
            # TODO 等到插件数目较多时再写，以便测试功能
            
        
    def custom_plugins_page():
        # 用户输入插件地址
        repository_url = st.text_input(label="输入插件url(必须为公开的git仓库)可安装自定义插件")
        if st.button(label="安装", key="install_confirm_button") is True:
            check_plugin(repository_url=repository_url)
    
    def check_plugin(repository_url: str): 
        if repository_url == '':
            st.warning("url不能为空")

        plugin_name = repository_url.split("/")[-1]
        plugin_path = os.path.join(plugins_path, plugin_name)
        if os.path.isdir(s=plugin_path) is True:
            reinstall_or_update_plugin(repository_url=repository_url, plugin_path=plugin_path, plugin_name=plugin_name)
        else:
            install_plugin(repository_url=repository_url, plugin_name=plugin_name, plugin_path=plugin_path)

    def reinstall_or_update_plugin(repository_url: str, plugin_name: str, plugin_path: str):
        st.warning(body="警告: 该插件已安装, 若想重新安装或更新插件, 请点击对应按钮, 注意: 重新安装插件可能会覆盖原有配置文件")
        st.button(label="重新安装",
                  key="reinstall_confirm_button",
                  on_click=lambda: reinstall_plugin(repository_url=repository_url, plugin_name=plugin_name, plugin_path=plugin_path))
        st.button(label="更新插件",
                  key="update_confirm_button",
                  on_click=lambda: update_plugin(plugin_name=plugin_name, plugin_path=plugin_path))

    def install_plugin(repository_url: str, plugin_name: str, plugin_path: str):
        try:
            raw_install_cmd = f"git clone {repository_url} {plugin_path}"
            install_cmd = raw_install_cmd.split(" ")

            # git clone repository_url plugin_path
            st.info(f"正在克隆{plugin_name}仓库到本地: {raw_install_cmd}")
            subprocess.run(install_cmd, stdout=subprocess.PIPE, check=True)

        except subprocess.CalledProcessError as e:
            st.error(f"克隆时出错, 请查看控制台报错")

        except Exception as e:
            st.error(f"克隆时出错, 请检查仓库url是否正确或重试: {e}")
            
        else:
            st.success(f"插件 {plugin_name} 安装成功！")

    def reinstall_plugin(repository_url: str, plugin_name: str, plugin_path: str):
        shutil.rmtree(plugin_path)           
        install_plugin(repository_url=repository_url, plugin_name=plugin_name, plugin_path=plugin_path)

    def update_plugin(plugin_name: str, plugin_path: str):
        os.chdir(plugin_path)
        raw_update_cmd = "git pull"
        # TODO 无法直接pull的情况下强制覆盖原仓库，并提示用户
        update_cmd = raw_update_cmd.split(" ")
        st.info(f"正在更新插件: {plugin_name}")

        try:
            subprocess.run(update_cmd, stdout=subprocess.PIPE, check=True)

        except subprocess.CalledProcessError as e:
            st.error(f"尝试更新插件时出错, 请查看控制台报错, 必要时请检查网络环境!")

        else:
            st.success(body=f"插件{plugin_name}更新成功!")

    install_plugins_columns_pages_dict = {
        "官方插件": official_plugins_page,
        "自定义插件": custom_plugins_page,
    }
    son_column = st.sidebar.radio(label="选择子栏目", options=install_plugins_columns_pages_dict.keys())
    install_plugins_columns_pages_dict[son_column]()

def plugins_port_setting_page():
    # 标题
    st.title(body="插件端口设置")
    st.markdown(body="<hr>", unsafe_allow_html=True)
    
    # 检查配置文件
    if check_config_file_existence() is False:
        st.warning(body="配置文件不存在，已创建默认配置文件！")
    
    # 读取配置文件
    config_dict = read_config()
    plugins_port_dict = config_dict["plugins"]["port"]
    for key in plugins_port_dict:
        plugins_port_dict[key] = st.text_input(label=f"{key}类型插件API端口", value=plugins_port_dict[key])
    
    # 保存按钮
    if st.button(label="保存更改", key="save_plugins_port_setting_button") is True:
        try:    
            write_config(config_dict=config_dict)
        except Exception as e:
            st.error(f"保存失败, 请重试或寻求他人帮助\n" \
                     f"{repr(e)}\n" \
                     f"{traceback.format_exc()}")
        else:
            st.success("保存成功！")

columns_pages_dict = {
    "选择插件": select_plugins_page,
    "安装插件": install_plugins_page,
    "插件端口设置": plugins_port_setting_page,
}

def plugins_main_page():
    # 选择栏目
    column = st.sidebar.radio(label="选择栏目", options=columns_pages_dict.keys())

    # 切换至相应栏目页
    st.empty()
    columns_pages_dict[column]()


plugins_main_page()