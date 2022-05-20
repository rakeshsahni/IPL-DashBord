import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def all_palyer_info(df_mat, df_bb, all_players) : 

    # number of total matches
    curr_player = st.sidebar.selectbox('Select Player',sorted(all_players), index=345)
    # st.write(sorted(all_players))

    st.subheader(curr_player)
        
    sig_play = df_mat[df_mat.apply(lambda x : True if (x['Team1Players'] + x['Team2Players']).find(curr_player) != -1 else False, axis = 1)].copy()

    # for season selection : 
    All_seasons = sig_play['Season'].unique() 
    # st.write(All_seasons)


    def no_win(row,player) : 
        if row['WinningTeam'] == row['Team1'] :
            if row['Team1Players'].find(player) != -1 : 
                return 1
            else :
                if row['Team2Players'].find(player) != -1 : 
                    return 1

        return 0


    no_win_match = sig_play.apply(lambda x : no_win(x, curr_player), axis = 1).values.sum()
    with st.container () : 
        txt1, txt2, txt3 = st.columns(3)
        with txt1 : 
            st.write(f"##### Total Matches Played ({sig_play['Season'].tail(1).values[0]}-{sig_play['Season'].head(1).values[0]}) : {sig_play.shape[0]}")
            
        with txt2 : 
            st.write(f"##### Total Matches Won : {no_win_match}")
            
        with txt3 : 
            st.write(f"##### Total Matches Loos : {sig_play.shape[0] - no_win_match}")
        
    
    # batter or bowler analysis
    is_baller = df_bb[df_bb['bowler'] == curr_player]
    is_batter = df_bb[df_bb['batter'] == curr_player]
    mrg = pd.merge(df_mat, df_bb, left_on='ID', right_on='ID')


    # only batter Analysis
    if is_batter.shape[0] != 0: 
        st.subheader("Batting Performance")

        with st.container() : 
            txt1, txt2, txt3 = st.columns(3)
            with txt1 : 
                st.write(f"#### Total Runs : {is_batter['batsman_run'].sum()}")
            
            with txt2 : 
                st.write(f"#### Total Sixes : {is_batter[is_batter['batsman_run'] == 6].shape[0]}")

            with txt3 : 
                st.write(f"#### Total Fours : {is_batter[is_batter['batsman_run'] == 4].shape[0]}")
        
        with st.container() : 
            txt1, txt2 = st.columns(2)
            
            with txt1 : 
                st.write(f"#### Total Bowls : {is_batter.shape[0]}")
            
            with txt2 : 
                st.write(f"#### Over all Strike Rate : {round(is_batter['batsman_run'].sum() / is_batter.shape[0],2)*100}")

        
        sr = df_bb[df_bb['batter'] == curr_player].sort_values(by='ID').batsman_run.reset_index(drop = True).reset_index()
        sr['cumsum_run'] = np.cumsum(sr['batsman_run'])
        sr['sr_ratio'] = np.round(sr['cumsum_run'] / sr['index'],2)*100
        
        
        # sticke rate graph
        fig, ax = plt.subplots()
        ax.set_ylabel(f"{curr_player} Strike Rate")
        ax.set_xlabel('No Of Matches Played')
        ax.plot(sr['sr_ratio'].values)
        st.pyplot(fig)
        
        # st.write('# Nice to meet you')
        # st.write(All_seasons)
        for itm in All_seasons : 
            Season_wise_info = mrg[(mrg['batter'] == curr_player) & (mrg['Season'] == itm)]
            itm_balls = Season_wise_info.shape[0]
            itm_runs = Season_wise_info['batsman_run'].sum()
            itm_6th = Season_wise_info[Season_wise_info['batsman_run'] == 6].shape[0]
            itm_4th = Season_wise_info[Season_wise_info['batsman_run'] == 4].shape[0]
            itm_fig, itm_ax = plt.subplots()
            itm_ax.set_title(f"In {itm} Season {curr_player} Performance")
            ax_obj = sns.barplot(['Total Runs', 'Total Bowls', 'Total 6th', 'Total 4th'], [itm_runs, itm_balls, itm_6th, itm_4th], ax = itm_ax
            )
            ax_obj.bar_label(ax_obj.containers[0])

            st.pyplot(itm_fig)

        



    
    # only baller
    if is_baller.shape[0] != 0 :
        st.subheader("Bowling Performance")        
        # total balls
        # st.write()
        # total runs
        # st.write(is_baller['batsman_run'].sum())
        # maiden over
        check_maiden = is_baller[~(( is_baller['extra_type'] == 'legbyes' ) | (is_baller['extra_type'] == 'byes') ) ].groupby(['ID' ,'overs']).total_run.sum().reset_index()
        #st.write(check_maiden[check_maiden['total_run'] == 0].shape[0])
        # overall strick rate
        # st.write(round(is_baller.shape[0] / is_baller[~(is_baller['kind'] == 'run out')]['isWicketDelivery'].sum(),2)*100)
        

        with st.container() : 
            txt1, txt2, txt3 = st.columns(3)
            
            # total wickets
            with txt1 : 
                st.write(f"#### Total Wickets : {is_baller[~(is_baller['kind'] == 'run out')]['isWicketDelivery'].sum()}")
            
            # total bowls 
            with txt2 : 
                st.write(f"#### Total Bowls : {is_baller.shape[0]}")

            with txt3 : 
                st.write(f"#### Total Maiden Overs : {check_maiden[check_maiden['total_run'] == 0].shape[0]}")
        
        with st.container() : 
            txt1, txt2 = st.columns(2)
            
            with txt1 : 
                st.write(f"#### Total Runs : {is_baller['batsman_run'].sum()}")
            
            with txt2 : 
                st.write(f"#### Over all Strike Rate (bowls/wickets) : {round(is_baller.shape[0] / is_baller[~(is_baller['kind'] == 'run out')]['isWicketDelivery'].sum(),2)}")



        # strick rate graph
        sr = is_baller.sort_values(by='ID').copy()
        cum_wic = sr['kind'].apply(lambda x : 0 if x == 'run out' or x != x else 1)
        cum_ball = np.array(range(1, is_baller.shape[0] + 1))
        cum_wic = np.cumsum(cum_wic.values)
        
        wic_st_ratio = np.round(cum_ball / cum_wic,2)

        fig, ax = plt.subplots()
        ax.set_ylabel(f"{curr_player} Strike Rate (balls/wickets)")
        ax.set_xlabel('No Of Matches Played')
        ax.set_ylabel("balls/wickets strike rate")
        ax.plot(wic_st_ratio)
        st.pyplot(fig)



        # st.write(All_seasons)
        for itm in All_seasons : 
            Season_wise_info = mrg[(mrg['bowler'] == curr_player) & (mrg['Season'] == itm)]
            itm_wic = Season_wise_info[~(Season_wise_info['kind'] == 'run out')]['isWicketDelivery'].sum()
            itm_balls = Season_wise_info.shape[0]
            itm_runs = Season_wise_info['batsman_run'].sum()
            is_meaiden = Season_wise_info[~(( Season_wise_info['extra_type'] == 'legbyes' ) | (is_baller['extra_type'] == 'byes') ) ].groupby(['ID' ,'overs']).total_run.sum().reset_index()
            # check_medon[check_medon['total_run'] == 0].shape
            
            itm_fig, itm_ax = plt.subplots()
            itm_ax.set_title(f"In {itm} Season {curr_player} Performance")
            ax_obj = sns.barplot(['Total Wickets', 'Total Bowls', 'Total Runs', 'Total Meaiden'], [itm_wic, itm_balls, itm_runs, is_meaiden[is_meaiden['total_run'] == 0].shape[0]], ax = itm_ax
            )
            ax_obj.bar_label(ax_obj.containers[0])

            st.pyplot(itm_fig)





    pom = sig_play[sig_play['Player_of_Match']  == curr_player].copy()
    if pom.shape[0] > 0 :
        
        st.write(f"#### Total Number of Player Of Match : {pom.shape[0]}")
            # st.dataframe(pom[[, , , , , , ]].reset_index(drop=True))
        for i in range(pom.shape[0]) :
            row_i = pom.iloc[i,:]
            
            bt_runs = df_bb[ (df_bb['ID'] == row_i['ID']) & (df_bb['batter'] == curr_player) ]['batsman_run']

            bw_wic = df_bb[ (df_bb['ID'] == row_i['ID']) & (df_bb['bowler'] == curr_player) ]
            
            st.write(f"")
            with st.container() :
                with st.container() : 
                    st.markdown(f"<h5 style='text-align: center; color: black;'>{i+1} : {row_i['Team1']} VS {row_i['Team2']}</h5>", unsafe_allow_html=True)
                    
                with st.container() : 
                    t1,t2 = st.columns(2)
                    with t1 : 
                        st.write(f"###### {row_i['MatchNumber']}, {row_i['Season']} ({row_i['Date']})")
                    with t2 : 
                        st.write(f"###### Venue : {row_i['Venue']} ({row_i['City']})")
                    
                with st.container() : 
                    st.markdown(f"<h6 style='text-align: center;'>Runs/Balls : {bt_runs.sum()}/{bt_runs.shape[0]}, Wickets/Balls/Runs : {bw_wic[(df_bb['kind'] == 'caught') | (df_bb['kind'] == 'bowled') | (df_bb['kind'] == 'caught and bowled')| (df_bb['kind'] == 'stumped') | (df_bb['kind'] == 'hit wicket')].shape[0]}/{bw_wic.shape[0]}/{bw_wic['batsman_run'].sum()}, Winner : {row_i['WinningTeam']}/{row_i['Margin']}-{row_i['WonBy']}</h6>", unsafe_allow_html=True)
                    










# curr_player = st.sidebar.selectbox('Select Player',sorted(all_players))
    # st.subheader(curr_player)
    
    # sig_play = df_mat[df_mat.apply(lambda x : True if (x['Team1Players'] + x['Team2Players']).find(curr_player) != -1 else False, axis = 1)].copy()

    # def no_win(row,player) : 
    #     if row['WinningTeam'] == row['Team1'] :
    #         if row['Team1Players'].find(player) != -1 : 
    #             return 1
    #     else :
    #         if row['Team2Players'].find(player) != -1 : 
    #             return 1

    #     return 0


    # no_win_match = sig_play.apply(lambda x : no_win(x, curr_player), axis = 1).values.sum()
    # with st.container () : 
    #     txt1, txt2, txt3 = st.columns(3)
    #     with txt1 : 
    #         st.write(f"##### Total Matches Played ({sig_play['Season'].tail(1).values[0]}-{sig_play['Season'].head(1).values[0]}) : {sig_play.shape[0]}")
        
    #     with txt2 : 
    #         st.write(f"##### Total Matches Won : {no_win_match}")
        
    #     with txt3 : 
    #         st.write(f"##### Total Matches Loos : {sig_play.shape[0] - no_win_match}")
    
    # pom = sig_play[sig_play['Player_of_Match']  == curr_player].copy()
    # if pom.shape[0] > 0 :
        
    #     st.write(f"#### Total Number of Player Of Match : {pom.shape[0]}")
    #     # st.dataframe(pom[[, , , , , , ]].reset_index(drop=True))
    #     for i in range(pom.shape[0]) :
    #         row_i = pom.iloc[i,:]
    #         with st.container() :
    #             with st.container() : 
    #                 st.markdown(f"<h5 style='text-align: center; color: black;'>{i+1} : {row_i['Team1']} VS {row_i['Team2']}</h5>", unsafe_allow_html=True)
                
    #             with st.container() : 
    #                 t1,t2 = st.columns(2)
    #                 with t1 : 
    #                    st.write(f"###### {row_i['MatchNumber']}, {row_i['Season']} ({row_i['Date']})")
    #                 with t2 : 
    #                     st.write(f"###### Venue : {row_i['Venue']} ({row_i['City']})")
                
    #             with st.container() : 
    #                 st.markdown(f"<h6 style='text-align: center;'>Win : {row_i['WinningTeam']}/{int(row_i['Margin'])}-{row_i['WonBy']}</h6>", unsafe_allow_html=True)
                



    # st.dataframe(sig_play)
    # st.dataframe(df_bb[df_bb['batter'] == curr_player])
    # st.write(all_players)
