import streamlit as st
import numpy as np
import pandas as pd
import matplotlib as plt 
import seaborn as sns
import pickle
from all_players import all_palyer_info
from all_seasons import all_seasons_info
from overall import all_overall

st.set_page_config(page_title="IPL DashBoard", page_icon="./ipl_logo.jpg",)

st.title('IPL DashBoard')
st.write("###### Created By [Rakesh Sahni](https://rakeshsahni.github.io/rakesh/), [Source Code](https://github.com/rakeshsahni/IPL-DashBord.git)")

df_bb = pd.read_csv('ball_by_ball.csv')
df_mat = pd.read_csv('matches.csv')

with open('players_list.pkl', 'rb') as spl : 
    all_players = pickle.load(spl)

Seasons = ['Overall', 'Players Wise', '2021', '2020/21', '2019', '2018', '2017', '2016', '2015', '2014',
       '2013', '2012', '2011', '2009/10', '2009', '2007/08']

sns.set_style('darkgrid')

selected_radio = st.sidebar.radio("What do you want?", Seasons)
# ['Season Wise', 'Players Wise','Season Wise', 'Players Wise','Season Wise', 'Players Wise','Season Wise', 'Players Wise']


# Overall analysis

if selected_radio == 'Overall' : 
    all_overall(df_mat.copy(), df_bb.copy())
    # sel_sea = st.sidebar.selectbox('Select Seson',Seasons)
    # if sel_sea != 'Overall' :

    

# Players wise analysis...

elif selected_radio == 'Players Wise':
    all_palyer_info(df_mat.copy(), df_bb.copy(), all_players)



# Season wise analysis

else:
    all_seasons_info(df_mat.copy(), df_bb.copy(), selected_radio)
    