import yaml
import os

# 默认配置
default_config = {
    "plugins": {
        "port": {
            "conversation": 11111,
            "grammar_checker": 11112,
            "pronunciation_checker": 11113,
            "stt": 11114,
            "tts": 11115,
        },
    },
}

# 配置路径
config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.yaml")

def check_config_file_existence() -> bool:
    '''检查配置文件是否存在'''
    if os.path.isfile(config_path):
        return True
    else:
        create_default_config()
        return False

def create_default_config() -> bool:
    '''创建默认配置'''
    return write_config(default_config) 

def read_config() -> dict:
    with open(config_path, "r", encoding="utf-8") as fp:
        return yaml.load(stream=fp, Loader=yaml.SafeLoader)
    
def write_config(config_dict: dict) -> bool:
    with open(config_path, "w", encoding="utf-8") as fp:
        yaml.dump(data=config_dict, stream=fp, Dumper=yaml.SafeDumper)
    return True