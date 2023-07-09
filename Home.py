import streamlit as st
import os


def home():
    # Set title
    st.title("Conversation Practice")

    # Show detail information about the application
    st.markdown("Welcome to the Conversation Practice app!")

if __name__ == "__main__":
    # 检查plugins文件夹是否存在
    if os.path.isdir("plugins") is False:
        os.mkdir("plugins")
    home()