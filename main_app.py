import streamlit as st
import streamlit.components.v1 as components
from streamlit_player import st_player
from streamlit_option_menu import option_menu

import pandas as pd
import plotly

from datetime import datetime
import pytz

from google.oauth2 import service_account
import pygsheets

#-----------------------
from functions import app_functions

# add folder as modules
import sys, os.path
func_dir = (os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))+ '/functions/') # name of function

if func_dir not in sys.path:
  sys.path.append(func_dir)

#--------------------
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True) 

#--------------
st.sidebar.write(' ')
with st.sidebar:
  # st.image('assets/placeholder.jpg')
  st.write('^ this is a placeholder image')
  st.title('App Navigation')

  st.write('---')
  st.title('Resources')
  with st.expander('Developed by', expanded=False):
    st.markdown("""
    © QED Insights - All rights reserved
    """)
  with st.expander('Contact', expanded=False):
    st.markdown("""
    - [Linkedin](https://www.linkedin.com/in/divadlen/)
    - [Email](dl.eeee.nv@gmail.com)
    - [Twitter](https://twitter.com/just_neldivad)
    """)
  with st.expander('Version', expanded=False):
    st.write(f'Plotly: {plotly.__version__}')
    st.write(f'Streamlit: {st.__version__}')
    st.write(f'Pandas: {pd.__version__}')
    pass
  
#----
st.write( app_functions.test_write() )


