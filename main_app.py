import streamlit as st
import streamlit.components.v1 as components
from streamlit_player import st_player
from streamlit_option_menu import option_menu

import numpy as np
import pandas as pd
import plotly

from datetime import datetime
import pytz

from gsheetsdb import connect

#--------------------------------------------
# Run app 
#-------------------------------------------
st.session_state.current_date = datetime.today().strftime('%Y-%m-%d')
st.set_page_config(
  page_title="Genshin Impact | Banner Timeline",
  page_icon='assets/miko.jpg',
  layout="wide",
  initial_sidebar_state="expanded",
)

def main():
  hide_st_style = """
              <style>
              #MainMenu {visibility: hidden;}
              footer {visibility: hidden;}
              header {visibility: hidden;}
              </style>
              """

  st.markdown(hide_st_style, unsafe_allow_html=True)    
  st.sidebar.write(' ')
  with st.sidebar:
    st.subheader('Tired of waiting your banner? I know that feel...')
    st.image('assets/qiqi.jpg')
    # st.write('^ this is a placeholder image')
    # st.title('App Navigation')

    st.write('---')
    st.title('Resources')
    with st.expander('Developed by', expanded=False):
      st.markdown("""
      © u/neldivad - All rights reserved
      """)
    with st.expander('Contact', expanded=False):
      st.markdown("""
      - [Medium](https://medium.com/@just_neldivad)
      - [Twitter](https://twitter.com/just_neldivad)
      """)
    with st.expander('Version', expanded=False):
      st.write(f'Plotly: {plotly.__version__}')
      st.write(f'Streamlit: {st.__version__}')
      st.write(f'Pandas: {pd.__version__}')
      pass
    st.write('')
    st.write('---')

  #----------------
  sheet_url = st.secrets['genshin_banner_gsheets_url']
  df = df_from_gsheet(sheet_url)
  
  current_date = pd.to_datetime( st.session_state.current_date )
  df['start_date'] = pd.to_datetime( df['start_date'])
  df['end_date'] = pd.to_datetime( df['end_date'])
  df['days_since_last_banner'] = ( (current_date - df['end_date']) / np.timedelta64(1, 'D')).astype(int)

  anemos = ['Venti', 'Xiao', 'Kazuha']
  cryos = ['Ganyu', 'Eula', 'Ayaka', 'Shenhe']
  dendros = ['Tighnari']
  electros = ['Keqing', 'Raiden', 'Yae']
  geos = ['Zhongli', 'Albedo', 'Itto']
  hydros = ['Tartaglia', 'Kokomi', 'Ayato','Yelan']
  pyros = ['Klee', 'Hutao', 'Yoimiya']

  element_dict = {
    'Anemo': anemos, 
    'Cryo': cryos, 
    'Dendro': dendros,
    'Electro': electros,
    'Geo': geos,
    'Hydro': hydros,
    'Pyro': pyros,
  }

  color_discrete_map = {
    'Anemo': '#40F0AF', 
    'Cryo': '#A9DEF9', 
    'Dendro': '#277559',
    'Electro': '#67489A',
    'Geo': '#CBA328',
    'Hydro': '#4558EB',
    'Pyro': '#E1081E', 
  }

  color_discrete_map_char = {
    '#40F0AF': anemos, 
    '#A9DEF9': cryos, 
    '#277559':  dendros,
    '#67489A': electros,
    '#CBA328': geos,
    '#4558EB': hydros,
    '#E1081E': pyros, 
  }

  def flatten_dict(d):
    nd = {}
    for k,v in d.items():
      # Check if it's a list, if so then iterate through
      if ((hasattr(v, '__iter__') and not isinstance(v, str))):
        for item in v:
          nd[item] = k
      else:
        nd[v] = k
    return nd

  flat_d = flatten_dict(element_dict)
  flat_color = flatten_dict(color_discrete_map_char)
  df['element'] = df['character'].map(flat_d)

  with st.expander('Data', expanded=False):
    st.write(df)
    
  ordering = list( df['character'].unique() )

  fig = make_timeline_chart(
    df,
    xstart= 'start_date',
    xend= 'end_date',
    ydata= 'character',
    cdata= 'character',
    hdata= ['days_since_last_banner'],
    color_discrete_map=flat_color,
    ordering=ordering,
  )
  st.plotly_chart(fig, use_container_width=True)

#----
# Create a connection object.
#------
@st.cache(ttl=600, allow_output_mutation=True)
def df_from_gsheet(url):
  import gsheetsdb
  conn = connect() 
  rows = conn.execute(f'SELECT * FROM "{url}"')
  df_gsheet = pd.DataFrame(rows)
  return df_gsheet

def make_timeline_chart(df, xstart, xend, ydata, cdata, hdata, ordering, color_discrete_map='', legend=True):
  import plotly.express as px

  n = len(ordering)
  height = 200 + 20*n

  fig = px.timeline(
    df,
    x_start=xstart,
    x_end=xend,
    y=ydata,
    color=cdata,
    hover_data=hdata,
    color_discrete_map=color_discrete_map,
    category_orders= { 
      ydata: ordering
    },
  )

  fig.update_layout(
    height=height,
    title= f'Displaying selected <b>{ydata}</b>,</b>',
    xaxis_tickfont_size=10,
    xaxis=dict(
      title= f'Date',
    ),
    yaxis= dict(
      title= f'{ydata}',
      titlefont_size=10,
      tickfont_size=10,
    ),
    #hovermode="x unified",
    showlegend= legend,
    legend=dict(
      title_text=f'{cdata.upper()}',
      font=dict(
        family="Times New Roman",
        size=10,
        color="black"
      ),
      bgcolor= 'rgba(0,0,0,0)',
      bordercolor="black",
      borderwidth=1
    ),
  )
  fig.for_each_yaxis(lambda yaxis: yaxis.update(title=''))
  fig.update_yaxes(title_text= '', autorange= True, fixedrange = False)
  fig.update_xaxes(
    title_text= '',
    rangeselector=dict(
      buttons=list([
        dict(count=7, label="1w", step="day", stepmode="backward"),
        dict(count=1, label="1m", step="month", stepmode="backward"),
        dict(count=6, label="6m", step="month", stepmode="backward"),
        dict(count=1, label="YTD", step="year", stepmode="todate"),
        dict(count=1, label="1y", step="year", stepmode="backward"),
        dict(count=5, label="5y", step="year", stepmode="backward"),
        dict(step="all")
        ])
    ),
    rangeslider= dict(visible=True,),
  )
  fig.add_vline(x= st.session_state.current_date,line_dash= 'dot')
  return fig

#-----------
# Run app
#------------
if __name__ == "__main__":
  main()
