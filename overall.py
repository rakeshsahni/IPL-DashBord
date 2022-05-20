import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st


def all_overall(df_mat, df_bb):

    merge = pd.merge(df_mat, df_bb, left_on='ID', right_on='ID')
    st.subheader(f"In {df_mat.iloc[-1,3]} To {df_mat.iloc[0,3]} IPL History All Top Stats")
    t_t_parti = set()
    t_t_parti.update(merge['Team1'].values)
    t_t_parti.update(merge['Team2'].values)
    # st.write(t_t_parti)
    with st.container() : 
        txt1 , txt2 = st.columns(2)
        with txt1 : 
            st.write(f"###### Total Seasons : {df_mat['Season'].nunique()}")
        with txt2 : 
            st.write(f"###### Total Teams Participated : {len(t_t_parti)}")
    
    
    with st.container():
        txt1, txt2, txt3 = st.columns(3)
        
        with txt1:
            st.write(f"###### Total Matches : {df_mat['ID'].nunique()}")
        with txt2:
            st.write(f"###### Total Runs : {merge['total_run'].sum()} ")
        with txt3:
            st.write(
                f"###### Total Wickets : {merge['isWicketDelivery'].sum()}")
    


    check_maiden_all = merge[~((merge['extra_type'] == 'legbyes') | (merge['extra_type'] == 'byes'))].groupby(['ID', 'overs']).total_run.sum().reset_index()
    
    with st.container():
        txt1, txt2, txt3 = st.columns(3)
        with txt1:
            st.write(
                f"###### Total Sixes : {merge[(merge['extras_run'] == 6) & (merge['non_boundary'] == 0) ].shape[0] + merge[(merge['batsman_run'] == 6) & (merge['non_boundary'] == 0) ].shape[0]} ")
        with txt2:
            st.write(
                f"###### Total Fours : {merge[(merge['extras_run'] == 4) & (merge['non_boundary'] == 0) ].shape[0] + merge[(merge['batsman_run'] == 4) & (merge['non_boundary'] == 0) ].shape[0]}")

        with txt3:
            st.write(
                f"###### Total Maiden : {check_maiden_all[check_maiden_all['total_run'] == 0].shape[0]}")



        all_sea_win = df_mat[df_mat['MatchNumber'] == 'Final'][['Season', 'Team1', 'Team2', 'WinningTeam']]
        st.write("#### All Seasons Winner : ")
        for itm in all_sea_win.values : 
            with st.container() : 
                txt1, txt2, txt3 = st.columns((1,4,2))
                with txt1 : 
                    st.write(f"###### {itm[0]}")
                with txt2 : 
                    st.write(f"###### {itm[1]} vs {itm[2]}")
                with txt3 : 
                    st.write(f"###### Win : {itm[3]}")
    
    # Top Team
    fig_w, axis_w = plt.subplots()
    sns_obj_w = sns.barplot(y = all_sea_win['WinningTeam'].value_counts().index, x = all_sea_win['WinningTeam'].value_counts().values, ax=axis_w)
    sns_obj_w.bar_label(sns_obj_w.containers[0])
    axis_w.set_title('Top Team In IPL History')
    axis_w.set_xlabel("Number of times win")
    st.pyplot(fig_w)



    # top 10 most run batter

    top10_batter = df_bb.groupby('batter')['batsman_run'].sum().reset_index().sort_values(by = 'batsman_run', ascending = False).head(10)
    
    fig_ba, axis_ba = plt.subplots()
    sns_obj_ba = sns.barplot(y = 'batter', x = 'batsman_run',data=top10_batter, ax=axis_ba)
    sns_obj_ba.bar_label(sns_obj_ba.containers[0])
    axis_ba.set_title('Top 10 Most Runs Batsman')
    st.pyplot(fig_ba)


    # top 10 most wicket bowler
    
    top10_bowler = df_bb[~(df_bb['kind'] == 'run out')].groupby(['bowler'])['isWicketDelivery'].sum(
    ).reset_index().sort_values(by='isWicketDelivery', ascending=False).head(10)


    fig_bo, axis_bo = plt.subplots()
    sns_obj_bo = sns.barplot(y = 'bowler', x = 'isWicketDelivery',data=top10_bowler, ax=axis_bo)
    sns_obj_bo.bar_label(sns_obj_bo.containers[0])
    axis_bo.set_title('Top 10 Most Wicket Bowler')
    axis_bo.set_xlabel('Number of Wickets')
    st.pyplot(fig_bo)



    # top 10 batter performance in single match

    top10_batter_sig_mat = df_bb.groupby(['ID', 'batter'])['batsman_run'].sum().reset_index().sort_values(by = 'batsman_run', ascending  = False).head(10)
        
    fig_batter_sig_mat, axis_batter_sig_mat = plt.subplots()
    sns_obj_batter_sig_mat = sns.barplot(y = 'batter', x = 'batsman_run',data=top10_batter_sig_mat, ax=axis_batter_sig_mat,estimator=np.max , ci = None)
    sns_obj_batter_sig_mat.bar_label(sns_obj_batter_sig_mat.containers[0])
    axis_batter_sig_mat.set_title('Top 10 Batsman Highest Run In A Single  Match')
    axis_batter_sig_mat.set_xlabel('Total Runs')
    st.pyplot(fig_batter_sig_mat)



    # top 10 most wicket bowler performance in single match

    top10_bowler_sig_mat = df_bb[df_bb['kind'] != 'run out'].groupby(['ID', 'bowler'])['isWicketDelivery'].sum().reset_index().sort_values(by = 'isWicketDelivery', ascending  = False).head(10)
        
    fig_bowler_sig_mat, axis_bowler_sig_mat = plt.subplots()
    sns_obj_bowler_sig_mat = sns.barplot(y = 'bowler', x = 'isWicketDelivery',data=top10_bowler_sig_mat, ax=axis_bowler_sig_mat)
    sns_obj_bowler_sig_mat.bar_label(sns_obj_bowler_sig_mat.containers[0])
    axis_bowler_sig_mat.set_title('Top 10 Bowler Highest Wickets In Single Match')
    axis_bowler_sig_mat.set_xlabel('Total wickets')
    st.pyplot(fig_bowler_sig_mat)



    # top 10 batsman most sixes
    top10_sixes = df_bb[(df_bb['non_boundary'] == 0) & (df_bb['batsman_run'] == 6)].groupby('batter').count().sort_values(by = 'batsman_run', ascending = False).head(10).reset_index()

    fig_6, axis_6 = plt.subplots()
    sns_obj_6 = sns.barplot(y = 'batter', x = 'batsman_run',data=top10_sixes, ax=axis_6)
    sns_obj_6.bar_label(sns_obj_6.containers[0])
    axis_6.set_title('Top 10 Batsman which Are Hitting Most Sixes')
    axis_6.set_xlabel('Number of sixes')
    st.pyplot(fig_6)



    # top 10 batsman fours
    top10_fours = df_bb[(df_bb['non_boundary'] == 0) & (df_bb['batsman_run'] == 4)].groupby('batter').count().sort_values(by = 'batsman_run', ascending = False).head(10).reset_index()

    fig_4, axis_4 = plt.subplots()
    sns_obj_4 = sns.barplot(y = 'batter', x = 'batsman_run',data=top10_fours, ax=axis_4)
    sns_obj_4.bar_label(sns_obj_4.containers[0])
    axis_4.set_title('Top 10 Batsman Which Are Hitting Most Fours')
    axis_4.set_xlabel('Number of fours')
    st.pyplot(fig_4)


    # top 10 players most caughtes performance players

    top10_caught_player = df_bb[df_bb['kind'] == 'caught'].groupby('fielders_involved')['isWicketDelivery'].sum().reset_index().sort_values(by = 'isWicketDelivery', ascending = False).head(10)

    fig_caught_player, axis_caught_player = plt.subplots()
    sns_obj_caught_player = sns.barplot(y = 'fielders_involved', x = 'isWicketDelivery',data=top10_caught_player, ax=axis_caught_player)
    sns_obj_caught_player.bar_label(sns_obj_caught_player.containers[0])
    axis_caught_player.set_title('Top 10 Players Most Catches')
    axis_caught_player.set_xlabel('Number Of Caught')
    axis_caught_player.set_ylabel('Players Name')
    st.pyplot(fig_caught_player)


    # Top 10 players play of match
    top10_pom = df_mat['Player_of_Match'].value_counts()[:10]
    
    fig_pom, axis_pom = plt.subplots()
    sns_obj_pom = sns.barplot(y = top10_pom.index, x = top10_pom.values, ax=axis_pom)
    sns_obj_pom.bar_label(sns_obj_pom.containers[0])
    axis_pom.set_title('Top 10 Players Get Most Player Of Match')
    axis_pom.set_xlabel('Number Of Player Of Match')
    axis_pom.set_ylabel('Players Name')
    st.pyplot(fig_pom)



    # top 10 team to score high
    top10_high_score_team = df_bb.groupby(['ID', 'BattingTeam'])['total_run'].sum().reset_index().sort_values(by = 'total_run', ascending  = False).head(10)

    fig_high_score_team, axis_high_score_team = plt.subplots()
    sns_obj_high_score_team = sns.barplot(y = 'BattingTeam', x = 'total_run',data=top10_high_score_team, ax=axis_high_score_team, estimator=np.max, ci=None)
        
    sns_obj_high_score_team.bar_label(sns_obj_high_score_team.containers[0])
        
    axis_high_score_team.set_title('Top 10 Teams whose Score High In IPL History')
    axis_high_score_team.set_xlabel('Total Runs')

    st.pyplot(fig_high_score_team)



    # top 10 team to score low
    top10_low_score_team = df_bb.groupby(['ID', 'BattingTeam'])['total_run'].sum().reset_index().sort_values(by = 'total_run').iloc[1:11,:]

    fig_low_score_team, axis_low_score_team = plt.subplots()
    sns_obj_low_score_team = sns.barplot(y = 'BattingTeam', x = 'total_run',data=top10_low_score_team, ax=axis_low_score_team, estimator=np.max, ci=None)
    sns_obj_low_score_team.bar_label(sns_obj_low_score_team.containers[0])
    axis_low_score_team.set_title('Top 10 Teams Whose Score Low In IPL History')
    axis_low_score_team.set_xlabel('Total Runs')
    st.pyplot(fig_low_score_team)


    # plot year by year run in ipl history

    plot_yrun = merge.groupby('Season')['total_run'].sum().reset_index().set_index('Season', drop = True)
    fig_yrun, axis_yrun = plt.subplots()
    axis_yrun.plot(plot_yrun.index,plot_yrun.total_run, 'b-s')
    
    for label in axis_yrun.get_xticklabels() : 
            label.set_rotation(90)
            label.set_ha('right')
    axis_yrun.set_title('Yearly Score In IPL History')
    axis_yrun.set_xlabel('Seasons')
    axis_yrun.set_ylabel('Total Runs')
    st.pyplot(fig_yrun)



    # plot year by year wicket in ipl history

    plot_ywic = merge.groupby('Season')['isWicketDelivery'].sum().reset_index().set_index('Season', drop = True)
    fig_ywic, axis_ywic = plt.subplots()
    axis_ywic.plot(plot_ywic.index,plot_ywic.isWicketDelivery, 'b-s')
    
    for label in axis_ywic.get_xticklabels() : 
            label.set_rotation(90)
            label.set_ha('right')
    axis_ywic.set_title('Yearly Wickets In IPL History')
    axis_ywic.set_xlabel('Seasons')
    axis_ywic.set_ylabel('Total Wickets')
    st.pyplot(fig_ywic)


# End code----
