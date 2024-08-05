"""Sidebar message"""

import streamlit as st


def custom_sidebar():
    st.sidebar.markdown("<br>", unsafe_allow_html=True)
    st.sidebar.markdown(
        """
        [![Repo](https://badgen.net/badge/icon/GitHub?icon=github&label)](https://github.com/tmlnv/idifcy) 
        """
    )
    st.sidebar.markdown("<br>", unsafe_allow_html=True)
