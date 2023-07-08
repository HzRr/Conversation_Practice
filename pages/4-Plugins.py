import streamlit as st
import traceback
from utils import check_config_file_existence, read_config, write_config
from utils import get_plugins_list, get_plugin_type, plugins_path
import subprocess
import os


def select_plugins():
    # 获取不同类型插件字典
    pass

def install_plugins():
    # 标题
    st.title(body="插件安装")
    st.markdown(body="<hr>", unsafe_allow_html=True)

    def official_plugins():
        # TODO 获取github用户仓库列表
        pass
        
    def custom_plugins():
        # 用户输入插件地址
        repository_url = st.text_input(label="输入插件url(必须为公开的git仓库)可安装自定义插件")
        if st.button(label="安装") is True:
            if repository_url == '':
                st.warning("url不能为空")
            else:
                try: 
                    # 构建安装命令
                    plugin_name = repository_url.split("/")[-1]
                    plugin_path = os.path.join(plugins_path, plugin_name)
                    raw_install_cmd = f"git clone {repository_url} {plugin_path}"
                    install_cmd = raw_install_cmd.split(" ")

                    # git clone repository_url plugin_path
                    st.info(f"正在克隆{plugin_name}仓库到本地: {raw_install_cmd}")
                    subprocess.run(install_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)

                except subprocess.CalledProcessError as e:
                    st.error(f"克隆时出错, 请检查仓库url是否正确或重试: {e}")

                except Exception as e:
                    st.error(f"克隆时出错, 请检查仓库url是否正确或重试: {e}")
                    
                else:
                    st.success(f"插件 {plugin_name} 安装成功！")

    install_plugins_columns_pages_dict = {
        "官方插件": official_plugins,
        "自定义插件": custom_plugins,
    }
    son_column = st.sidebar.radio(label="选择子栏目", options=install_plugins_columns_pages_dict.keys())
    install_plugins_columns_pages_dict[son_column]()
                


def plugins_port_setting():
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
    if st.button(label="保存更改") is True:
        try:    
            write_config(config_dict=config_dict)
        except Exception as e:
            st.error(f"保存失败, 请重试或寻求他人帮助\n" \
                     f"{repr(e)}\n" \
                     f"{traceback.format_exc()}")
        else:
            st.success("保存成功！")

columns_pages_dict = {
    "选择插件": select_plugins,
    "安装插件": install_plugins,
    "插件端口设置": plugins_port_setting,
}

def plugins_main_page():
    # 选择栏目
    column = st.sidebar.radio(label="选择栏目", options=columns_pages_dict.keys())

    # 切换至相应栏目页
    st.empty()
    columns_pages_dict[column]()


plugins_main_page()