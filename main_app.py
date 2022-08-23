import streamlit as st
import streamlit.components.v1 as components
from streamlit_player import st_player
from streamlit_option_menu import option_menu

from gsheetsdb import connect
import pandas as pd
import plotly

from datetime import datetime
import pytz

#-----------------------

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
# Create a connection object.
conn = connect() 

@st.cache(ttl=600)
def df_from_gsheet(url):
  rows = conn.execute(f'SELECT * FROM "{url}"')
  df_gsheet = pd.DataFrame(rows)
  return df_gsheet

sheet_url = st.secrets['genshin_banner_gsheets_url']
df = df_from_gsheet(sheet_url)

st.write(df)

