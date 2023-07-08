import os


# 插件路径
plugins_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "plugins")

def get_plugins_list() -> list:
    '''获取已安装插件列表'''
    plugins_list = []
    for entry in os.listdir(plugins_path):
        if os.path.isdir(os.path.join(plugins_path, entry)):
            plugins_list.append(entry)
    return plugins_list

def get_plugin_type(plugin_name: str) -> str:
    '''根据插件名称获取插件类型'''
    pass