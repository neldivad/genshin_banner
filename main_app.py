import streamlit as st
import streamlit.components.v1 as components
from streamlit_player import st_player
from streamlit_option_menu import option_menu

import pandas as pd
import plotly

from datetime import datetime
import pytz

from gsheetsdb import connect

#-------------------------------------------
# Run app 
#-------------------------------------------
current_date = datetime.now(pytz.timezone('US/Eastern'))

def main():
  hide_st_style = """
              <style>
              #MainMenu {visibility: hidden;}
              footer {visibility: hidden;}
              header {visibility: hidden;}
              </style>
              """

  # st.markdown(hide_st_style, unsafe_allow_html=True)    

  # st.write('^ this is a placeholder image')

  # st.sidebar.write(' ')
  with st.sidebar:
    # st.image('assets/placeholder.jpg')
    # st.write('^ this is a placeholder image')
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

  #----------------
  
  # st.write(current_date)

  sheet_url = 'https://docs.google.com/spreadsheets/d/1EGl6QfXxbinI4z8WqJ80Gu5lyQhfUy9KuLVPJNaruIA/edit?pli=1#gid=0'
  df = df_from_gsheet(sheet_url)

  # st.write(df)

  ordering = list( df['character'].unique() )
  # st.write(len(ordering))

  fig2 = make_timeline_chart(
    df,
    xstart= 'start_date',
    xend= 'end_date',
    ydata= 'character',
    cdata= 'character',
    ordering=ordering,
  )
  st.plotly_chart(fig2, use_container_width=True)


#----
# Create a connection object.
#------
@st.cache(ttl=600)
def df_from_gsheet(url):
  import gsheetsdb
  conn = connect() 
  rows = conn.execute(f'SELECT * FROM "{url}"')
  df_gsheet = pd.DataFrame(rows)
  return df_gsheet

def make_timeline_chart(df, xstart, xend, ydata, cdata, ordering, legend=True):
  import plotly.express as px

  n = len(ordering)
  height = 200 + 20*n

  fig = px.timeline(
    df,
    x_start=xstart,
    x_end=xend,
    y=ydata,
    color=cdata,
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
    hovermode="x unified",
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
        dict(count=1, label="1m", step="month", stepmode="backward"),
        dict(count=6, label="6m", step="month", stepmode="backward"),
        dict(count=1, label="YTD", step="year", stepmode="todate"),
        dict(count=1, label="1y", step="year", stepmode="backward"),
        dict(count=5, label="5y", step="year", stepmode="backward"),
        dict(count=10, label="10y", step="year", stepmode="backward"),
        dict(step="all")
        ])
    ),
    rangeslider= dict(visible=True,),
  )
  fig.add_vline(x= current_date,line_dash= 'dot')
  return fig

#-----------
# Run app
#------------
if __name__ == "__main__":
  main()
