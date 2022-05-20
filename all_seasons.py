import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st


def all_seasons_info(df_mat, df_bb, selected_radio) : 

    df_mat_sea = df_mat[df_mat['Season'] == selected_radio].copy()
    merge = pd.merge(df_mat_sea, df_bb, left_on='ID', right_on='ID')
    
    
    def team_opt(row) : 
        res = ""
        res += row[2]
        res += " | "
        res += row[0] + " vs " + row[1]
        return res



    all_matches = list(df_mat_sea[['Team1', 'Team2', 'MatchNumber']].apply(team_opt, axis = 1).values)
    # st.write(type(all_matches))
    all_matches.insert(0, 'Overall')
    
    select_team = st.sidebar.selectbox('Select Teams', all_matches)



    # start writing code
    total_team = {}
    def win_team(row) : 
        
        if row['Team1'] in total_team : 
            total_team[row['Team1']][1] += 1
        else : 
            total_team[row['Team1']] = [0,1]
        
        
        if row['Team2'] in total_team : 
            total_team[row['Team2']][1] += 1
        else : 
            total_team[row['Team2']] = [0,1]

        if not row['WinningTeam'] != row['WinningTeam'] :
            total_team[row['WinningTeam']][0] += 1
            
    df_mat_sea.apply(win_team, axis = 1)

    # overall analysis of particular season
    if(select_team == 'Overall') :
        st.write(f"#### IPL Season {selected_radio} Overall Details")
        
        with st.container() : 
            txt1, txt2 = st.columns([2,1])

            with txt1 : 
                st.write(f"###### Matches Open : {df_mat_sea.tail(1)['Date'].values[0]},  End : {df_mat_sea.head(1)['Date'].values[0]}")
            with txt2 : 
                st.write(f"###### Total Matches : {df_mat_sea.shape[0]} ")


        with st.container() : 
            txt1, txt2, txt3 = st.columns(3)
            with txt1 : 
                st.write(f"###### Overall Runs : {merge['total_run'].sum()} ")
            with txt2 : 
                st.write(f"###### Overall Wickets : {merge['isWicketDelivery'].sum()}")
            with txt3 : 
                st.write(f"###### Overall bowls : {merge.shape[0]}")
        
        check_maiden_all = merge[~(( merge['extra_type'] == 'legbyes' ) | (merge['extra_type'] == 'byes') ) ].groupby(['ID' ,'overs']).total_run.sum().reset_index()
        
        with st.container() : 
            txt1, txt2, txt3 = st.columns(3)
            with txt1 : 
                st.write(f"###### Overall Sixes : {merge[(merge['extras_run'] == 6) & (merge['non_boundary'] == 0) ].shape[0] + merge[(merge['batsman_run'] == 6) & (merge['non_boundary'] == 0) ].shape[0]} ")
            with txt2 : 
                st.write(f"###### Overall Fours : {merge[(merge['extras_run'] == 4) & (merge['non_boundary'] == 0) ].shape[0] + merge[(merge['batsman_run'] == 4) & (merge['non_boundary'] == 0) ].shape[0]}")
            with txt3 : 
                st.write(f"###### Overall Maiden : {check_maiden_all[check_maiden_all['total_run'] == 0].shape[0]}")


        # for orange cap
        batter_gp = merge.groupby(['ID', 'batter'])['batsman_run'].sum().reset_index()

        top5_batter = batter_gp.groupby('batter')['batsman_run'].sum().reset_index().sort_values(by = 'batsman_run', ascending = False)[:5]
        st.write(f"##### Orange Cap : {top5_batter.iloc[0,0]}, Runs : {top5_batter.iloc[0,1]}, In {batter_gp[batter_gp['batter'] == top5_batter.iloc[0,0]].shape[0]} Matches")


        #  purple cap 
        # Season_wise_info[~(Season_wise_info['kind'] == 'run out')]['isWicketDelivery'].sum()
        top5_bowler = merge[~(merge['kind'] == 'run out')].groupby(['bowler'])['isWicketDelivery'].sum().reset_index().sort_values(by = 'isWicketDelivery', ascending = False).head(5)
        
        st.write(f"##### Purple Cap : {top5_bowler.iloc[0,0]}, Wickets : {top5_bowler.iloc[0,1]}, In {merge[merge['bowler'] == top5_bowler.iloc[0,0]].shape[0]} Bowls")



        # In final Match
        final_detail = df_mat_sea[ df_mat_sea['MatchNumber'] == 'Final']
        st.write(f"#### Final Match : {final_detail['Team1'].values[0]} vs {final_detail['Team2'].values[0]}")
        with st.container() : 
            txt1, txt2 = st.columns((1,2))
            with txt1 : 
                st.write(f"###### Date : {final_detail['Date'].values[0]}")
            
            with txt2 : 
                st.write(f"###### Venue : {final_detail['Venue'].values[0]} / ( {final_detail['City'].values[0]} )")

        with st.container() : 
            txt1, txt2, txt3 = st.columns(3)
            with txt1 : 
                st.write(f"###### Winning Team : {final_detail['WinningTeam'].values[0]}")
            with txt2 : 
                st.write(f"###### Won By : {final_detail['Margin'].values[0]} / ( {final_detail['WonBy'].values[0]} )")
            with txt3 : 
                st.write(f"###### POM : {final_detail['Player_of_Match'].values[0]}")

        
        # each team win details
        st.write(f"#### Total Number Of Teams participate {len(total_team)} : ")


        for itm in total_team : 
            with st.container() :
                txt1, txt2, txt3, txt4 = st.columns([2,1,1,1])
                with txt1 : 
                    st.write(f"###### {itm}")
                with txt2 : 
                    st.write(f"###### Wins : {total_team[itm][0]}")
                with txt3 : 
                    st.write(f"###### Loss : {total_team[itm][1] - total_team[itm][0]}")
                with txt4 : 
                    st.write(f"###### Total {total_team[itm][1]}")

        
        arr_teams = []
        arr_wins = []
        for itm in total_team :
            arr_teams.append(itm) 
            arr_wins.append(total_team[itm][0])
        
        fig, axis = plt.subplots()
        sns_obj = sns.barplot(y = arr_teams, x = arr_wins, ax=axis)
        sns_obj.bar_label(sns_obj.containers[0])
        axis.set_title('Numbers Of Won Matches')
        st.pyplot(fig)

        
        
        
        # top 5 batter

        fig_ba, axis_ba = plt.subplots()
        sns_obj_ba = sns.barplot(y = 'batter', x = 'batsman_run',data=top5_batter, ax=axis_ba)
        sns_obj_ba.bar_label(sns_obj_ba.containers[0])
        axis_ba.set_title('Top 5 Batter')
        st.pyplot(fig_ba)


        # top 5 bowler

        fig_bo, axis_bo = plt.subplots()
        sns_obj_bo = sns.barplot(y = 'bowler', x = 'isWicketDelivery',data=top5_bowler, ax=axis_bo)
        sns_obj_bo.bar_label(sns_obj_bo.containers[0])
        axis_bo.set_title('Top 5 Bowler')
        axis_bo.set_xlabel('Wickets')
        st.pyplot(fig_bo)


        # top 5 sixes
        top5_sixes = merge[(merge['non_boundary'] == 0) & (merge['batsman_run'] == 6)][['batter', 'batsman_run']].groupby('batter').count().sort_values(by = 'batsman_run', ascending = False).head(5).reset_index()

        fig_6, axis_6 = plt.subplots()
        sns_obj_6 = sns.barplot(y = 'batter', x = 'batsman_run',data=top5_sixes, ax=axis_6)
        sns_obj_6.bar_label(sns_obj_6.containers[0])
        axis_6.set_title('Top 5 batter which are hitting most sixes')
        axis_6.set_xlabel('Number of sixes')
        st.pyplot(fig_6)



        # top 5 fours
        top5_fours = merge[(merge['non_boundary'] == 0) & (merge['batsman_run'] == 4)][['batter', 'batsman_run']].groupby('batter').count().sort_values(by = 'batsman_run', ascending = False).head(5).reset_index()

        fig_4, axis_4 = plt.subplots()
        sns_obj_4 = sns.barplot(y = 'batter', x = 'batsman_run',data=top5_fours, ax=axis_4)
        sns_obj_4.bar_label(sns_obj_4.containers[0])
        axis_4.set_title('Top 5 batter which are hitting most fours')
        axis_4.set_xlabel('Number of fours')
        st.pyplot(fig_4)


        # top 5 team to score high
        top5_high_score_team = merge.groupby(['ID', 'BattingTeam'])['total_run'].sum().reset_index().sort_values(by = 'total_run', ascending  = False).head(5)

        fig_high_score_team, axis_high_score_team = plt.subplots()
        sns_obj_high_score_team = sns.barplot(y = 'BattingTeam', x = 'total_run',data=top5_high_score_team, ax=axis_high_score_team)
        
        sns_obj_high_score_team.bar_label(sns_obj_high_score_team.containers[0])
        
        axis_high_score_team.set_title('Top 5 Team whose score high')
        axis_high_score_team.set_xlabel('Total Runs')

        st.pyplot(fig_high_score_team)

        # top 5 team to score low
        top5_low_score_team = merge.groupby(['ID', 'BattingTeam'])['total_run'].sum().reset_index().sort_values(by = 'total_run').head(5)

        fig_low_score_team, axis_low_score_team = plt.subplots()
        sns_obj_low_score_team = sns.barplot(y = 'BattingTeam', x = 'total_run',data=top5_low_score_team, ax=axis_low_score_team)
        sns_obj_low_score_team.bar_label(sns_obj_low_score_team.containers[0])
        axis_low_score_team.set_title('Top 5 Team whose score low')
        axis_low_score_team.set_xlabel('Total Runs')
        st.pyplot(fig_low_score_team)


        # top 5 batter performance in single match

        top5_batter_sig_mat = merge.groupby(['ID', 'batter'])['batsman_run'].sum().reset_index().sort_values(by = 'batsman_run', ascending  = False).head(5)
        
        fig_batter_sig_mat, axis_batter_sig_mat = plt.subplots()
        sns_obj_batter_sig_mat = sns.barplot(y = 'batter', x = 'batsman_run',data=top5_batter_sig_mat, ax=axis_batter_sig_mat)
        sns_obj_batter_sig_mat.bar_label(sns_obj_batter_sig_mat.containers[0])
        axis_batter_sig_mat.set_title('Top 5 Batter whose score high in single match')
        axis_batter_sig_mat.set_xlabel('Total Runs')
        st.pyplot(fig_batter_sig_mat)


        # top 5 bowler performance in single match

        top5_bowler_sig_mat = merge[merge['kind'] != 'run out'].groupby(['ID', 'bowler'])['isWicketDelivery'].sum().reset_index().sort_values(by = 'isWicketDelivery', ascending  = False).head(5)
        
        fig_bowler_sig_mat, axis_bowler_sig_mat = plt.subplots()
        sns_obj_bowler_sig_mat = sns.barplot(y = 'bowler', x = 'isWicketDelivery',data=top5_bowler_sig_mat, ax=axis_bowler_sig_mat)
        sns_obj_bowler_sig_mat.bar_label(sns_obj_bowler_sig_mat.containers[0])
        axis_bowler_sig_mat.set_title('Top 5 Bowler whose wickets high in single match')
        axis_bowler_sig_mat.set_xlabel('Total wickets')
        st.pyplot(fig_bowler_sig_mat)
    
        # top 5 caught performance players

        top5_caught_player = merge[merge['kind'] == 'caught'].groupby('fielders_involved')['isWicketDelivery'].sum().reset_index().sort_values(by = 'isWicketDelivery', ascending = False).head(5)

        fig_caught_player, axis_caught_player = plt.subplots()
        sns_obj_caught_player = sns.barplot(y = 'fielders_involved', x = 'isWicketDelivery',data=top5_caught_player, ax=axis_caught_player)
        sns_obj_caught_player.bar_label(sns_obj_caught_player.containers[0])
        axis_caught_player.set_title(f'Top 5 Players Whose Most Caught In {selected_radio}')
        axis_caught_player.set_xlabel('Number Of Caught')
        st.pyplot(fig_caught_player)
    



    # select box team by team analysis
    # Now we analysis X-Team vs Y-Team


     
    else : 
        match_num, x_vs_y = select_team.split(' | ')
        st.subheader(x_vs_y)

        sig_match = df_mat_sea[df_mat_sea['MatchNumber'] == match_num]
        sig_merge = merge[merge['MatchNumber'] == match_num]

        # Date and Venue details        
        with st.container() : 
            txt1, txt2 = st.columns((1,4))
            with txt1 : 
                st.write(f"###### Date : {sig_match['Date'].values[0]}")
            with txt2 : 
                st.write(f"###### Venue : {sig_match['Venue'].values[0]} / {sig_match['City'].values[0]}")

        
        # Toss decision
        with st.container() : 
            txt1, txt2 = st.columns(2)
            with txt1 : 
                st.write(f"###### Toss Winner : {sig_match['TossWinner'].values[0]}")
            with txt2 : 
                st.write(f"###### Decision : {sig_match['TossDecision'].values[0]}")

        # winning team
        with st.container() : 
            txt1, txt2 = st.columns(2)
            with txt1 : 
                st.write(f"###### Winnig Team : {sig_match['WinningTeam'].values[0]}")
            with txt2 : 
                st.write(f"###### Won By : {sig_match['Margin'].values[0]} / {sig_match['WonBy'].values[0]}")
        
        # umpire name
        with st.container() : 
            txt1, txt2 = st.columns(2)
            with txt1 : 
                st.write(f"###### UMP1 : {sig_match['Umpire1'].values[0]}")
            with txt2 : 
                st.write(f"###### UMP2 : {sig_match['Umpire2'].values[0]}")
        

        # player of match
        pom_player = sig_match['Player_of_Match'].values[0]
        pom_run = sig_merge[sig_merge['batter'] == pom_player]['batsman_run']
        pom_wic = sig_merge[(sig_merge['bowler'] == pom_player) & (sig_merge['kind'] != 'run out')]['isWicketDelivery']
        pom_wic_bts_run = sig_merge[sig_merge['bowler'] == pom_player]
        with st.container() : 
            txt1, txt2, txt3 = st.columns(3)
            with txt1 : 
                st.write(f"###### Player Of Match : {pom_player}")
            
            with txt2 : 
                st.write(f"###### R / B : {pom_run.sum()} / {pom_run.shape[0]}")
            
            with txt3 : 
                st.write(f"###### W / B / R : {pom_wic.sum()} / {pom_wic_bts_run.shape[0]} / {pom_wic_bts_run['batsman_run'].sum()}")



        # all player run, wic, and caught
        
        Team1_Team2 = {
            sig_match['Team1'].values[0] : {},
            sig_match['Team2'].values[0] : {}
        }

        player_all_d = {"run" : 0, "six" : 0, "four" : 0, "run_b" : 0, 
                        "wic" : [], 'wic_b' : 0, 'wic_r' : 0, 'maiden' : 0, 
                        'cau' : []}
        def all_players_lis1(row) :
            
            for itm1 in row['Team1Players'].split("'") :
                if itm1[0] >= 'A' and itm1[0] <= 'Z' or itm1[0] >= 'a' and itm1[0] <= 'z' : 
                    Team1_Team2[sig_match['Team1'].values[0]][itm1] = player_all_d.copy()
            
            for itm2 in row['Team2Players'].split("'") :
                if itm2[0] >= 'A' and itm2[0] <= 'Z' or itm2[0] >= 'a' and itm2[0] <= 'z' : 
                    Team1_Team2[sig_match['Team2'].values[0]][itm2] = player_all_d.copy()

        sig_match.apply(all_players_lis1, axis = 1)


        # 'run': 0,
        # 'six': 0,
        # 'four': 0,
        # 'run_b': 0,
        # 'wic': [],
        # 'wic_b': 0,
        # 'wic_r': 0,
        # 'maiden': 0,
        # 'cau': []
        for tm in Team1_Team2 : 
            for player in Team1_Team2[tm] : 
                pay_bat = sig_merge[sig_merge['batter'] == player]
                tot_6th = sig_merge[ (sig_merge['batter'] == player ) & (sig_merge['non_boundary'] == 0) & (sig_merge['batsman_run'] == 6)].shape[0]
                tot_4th = sig_merge[ (sig_merge['batter'] == player ) & (sig_merge['non_boundary'] == 0) & (sig_merge['batsman_run'] == 4)].shape[0]
                
                pay_bow = sig_merge[sig_merge['bowler'] == player]
                tot_wic = sig_merge[(sig_merge['bowler'] == player) & (sig_merge['kind'] != 'run out') & (sig_merge['isWicketDelivery'] == 1) ]['player_out'].values
                check_maiden = sig_merge[(sig_merge['bowler'] == player) & (~((sig_merge['extra_type'] == 'legbyes') | (sig_merge['extra_type'] == 'byes')))].groupby('overs')['total_run'].sum().reset_index()
                
                tot_cau = sig_merge[ (sig_merge['kind'] == 'caught') & (sig_merge['fielders_involved'] == player) ]['player_out'].values
                
                Team1_Team2[tm][player]['run'] = pay_bat['batsman_run'].sum()
                Team1_Team2[tm][player]['six'] = tot_6th
                Team1_Team2[tm][player]['four'] = tot_4th
                Team1_Team2[tm][player]['run_b'] = pay_bat.shape[0]
                
                Team1_Team2[tm][player]['wic'] = tot_wic
                Team1_Team2[tm][player]['wic_b'] = pay_bow.shape[0]
                Team1_Team2[tm][player]['wic_r'] = pay_bow['batsman_run'].sum()
                Team1_Team2[tm][player]['maiden'] = check_maiden[check_maiden['total_run'] == 0].shape[0]
                
                Team1_Team2[tm][player]['cau'] = tot_cau
                

        # Team1_Team2 is final dictionary in which all palyers all info inseted
        tm1, tm2 = list(Team1_Team2.keys())[0], list(Team1_Team2.keys())[1]

        tm1_details = sig_merge[sig_merge['BattingTeam'] == tm1]
        tm2_details = sig_merge[sig_merge['BattingTeam'] == tm2]
        
        # st.write(f"###### Team : {tm1} Runs {tm1_details['total_run'].sum()}, Wickets : {tm1_details['isWicketDelivery'].sum()} Bowls : {tm1_details.shape[0]}")

        # st.write(f"###### Team : {tm2} Runs {tm2_details['total_run'].sum()}, Wickets : {tm2_details['isWicketDelivery'].sum()} Bowls : {tm2_details.shape[0]}")
        
        # each team details : 

        # y_label = ['Runs', 'Sixes', 'Fours', 'Runs/Balls', 'Wickets', 'Wickets/Balls', 'Wickets/Runs', 'Maiden', 'Catches']

        def ten_col(c1 = 'Name', c2 = 'R', c3 = '6', c4 = '4', c5 = 'B/R', c6 = 'W', c7 = 'B/W', c8 = 'R/W', c9 = 'M', c10 = "C") : 
            with st.container() : 
                txt0, txt1, txt2, txt3, txt4, txt5, txt6, txt7, txt8, txt9 = st.columns(10)
                with txt0 : 
                    st.write(f"###### {c1}")
                with txt1 : 
                    st.write(f"###### {c2}")
                with txt2 : 
                    st.write(f"###### {c3}")
                with txt3 : 
                    st.write(f"###### {c4}")
                with txt4 : 
                    st.write(f"###### {c5}")
                with txt5 : 
                    st.write(f"###### {c6}")
                with txt6 : 
                    st.write(f"###### {c7}")
                with txt7 : 
                    st.write(f"###### {c8}")
                with txt8 : 
                    st.write(f"###### {c9}")
                with txt9 : 
                    st.write(f"###### {c10}")

        
        # first Team details 
        with st.container() : 
            txt1, txt2 = st.columns(2)
            with txt1 : 
                st.write(f"#### Team : {tm1}")
            with txt2 : 
                st.write(f"#### R / W / B : {tm1_details['total_run'].sum()} / {tm1_details['isWicketDelivery'].sum()} / {tm1_details.shape[0]}")
                
        ten_col()
        
        no_of_player = 1
        for plys in Team1_Team2[tm1] :
            x_label = []
            x_label.append(f"{no_of_player}-{plys}")
            for typ in Team1_Team2[tm1][plys] : 
                if typ == 'wic' or typ == 'cau' : 
                    x_label.append(len(Team1_Team2[tm1][plys][typ]))
                else : 
                    x_label.append(int(Team1_Team2[tm1][plys][typ]))
            ten_col(x_label[0], x_label[1], x_label[2],x_label[3],x_label[4],x_label[5],x_label[6],x_label[7],x_label[8],x_label[9])
            no_of_player += 1


        st.markdown("""---""")


        # second Team details 
        with st.container() : 
            txt1, txt2 = st.columns(2)
            with txt1 : 
                st.write(f"#### Team : {tm2}")
            with txt2 : 
                st.write(f"#### R / W / B : {tm2_details['total_run'].sum()} / {tm2_details['isWicketDelivery'].sum()} / {tm2_details.shape[0]}")
                
        ten_col()
        
        no_of_player = 1
        for plys in Team1_Team2[tm2] :
            x_label = []
            x_label.append(f"{no_of_player}-{plys}")
            for typ in Team1_Team2[tm2][plys] : 
                if typ == 'wic' or typ == 'cau' : 
                    x_label.append(len(Team1_Team2[tm2][plys][typ]))
                else : 
                    x_label.append(int(Team1_Team2[tm2][plys][typ]))
            ten_col(x_label[0], x_label[1], x_label[2],x_label[3],x_label[4],x_label[5],x_label[6],x_label[7],x_label[8],x_label[9])
            no_of_player += 1



        # top 3 players

        # top 3 batter
        top3_batter = sig_merge.groupby('batter')['batsman_run'].sum().reset_index().sort_values(by = 'batsman_run', ascending = False)[:3]
         
        # Season_wise_info[~(Season_wise_info['kind'] == 'run out')]['isWicketDelivery'].sum()
        top3_bowler = sig_merge[~(sig_merge['kind'] == 'run out')].groupby(['bowler'])['isWicketDelivery'].sum().reset_index().sort_values(by = 'isWicketDelivery', ascending = False).head(3)
        
        # top 3 batter

        fig_ba, axis_ba = plt.subplots()
        sns_obj_ba = sns.barplot(y = 'batter', x = 'batsman_run',data=top3_batter, ax=axis_ba)
        sns_obj_ba.bar_label(sns_obj_ba.containers[0])
        axis_ba.set_title('Top 3 Batter')
        st.pyplot(fig_ba)


        # top 3 bowler

        fig_bo, axis_bo = plt.subplots()
        sns_obj_bo = sns.barplot(y = 'bowler', x = 'isWicketDelivery',data=top3_bowler, ax=axis_bo)
        sns_obj_bo.bar_label(sns_obj_bo.containers[0])
        axis_bo.set_title('Top 3 Bowler')
        axis_bo.set_xlabel('Wickets')
        st.pyplot(fig_bo)


        # top 3 sixes
        top3_sixes = sig_merge[(sig_merge['non_boundary'] == 0) & (sig_merge['batsman_run'] == 6)][['batter', 'batsman_run']].groupby('batter').count().sort_values(by = 'batsman_run', ascending = False).head(3).reset_index()

        fig_6, axis_6 = plt.subplots()
        sns_obj_6 = sns.barplot(y = 'batter', x = 'batsman_run',data=top3_sixes, ax=axis_6)
        sns_obj_6.bar_label(sns_obj_6.containers[0])
        axis_6.set_title('Top 3 batter which are hitting most sixes')
        axis_6.set_xlabel('Number of sixes')
        st.pyplot(fig_6)



        # top 5 fours
        top3_fours = sig_merge[(sig_merge['non_boundary'] == 0) & (sig_merge['batsman_run'] == 4)][['batter', 'batsman_run']].groupby('batter').count().sort_values(by = 'batsman_run', ascending = False).head(3).reset_index()

        fig_4, axis_4 = plt.subplots()
        sns_obj_4 = sns.barplot(y = 'batter', x = 'batsman_run',data=top3_fours, ax=axis_4)
        sns_obj_4.bar_label(sns_obj_4.containers[0])
        axis_4.set_title('Top 3 batter which are hitting most fours')
        axis_4.set_xlabel('Number of fours')
        st.pyplot(fig_4)


        # top 3 caught performance players

        top3_caught_player = sig_merge[sig_merge['kind'] == 'caught'].groupby('fielders_involved')['isWicketDelivery'].sum().reset_index().sort_values(by = 'isWicketDelivery', ascending = False).head(3)

        fig_caught_player, axis_caught_player = plt.subplots()
        sns_obj_caught_player = sns.barplot(y = 'fielders_involved', x = 'isWicketDelivery',data=top3_caught_player, ax=axis_caught_player)
        sns_obj_caught_player.bar_label(sns_obj_caught_player.containers[0])
        axis_caught_player.set_title(f'Top 3 Players Who catches Most')
        axis_caught_player.set_xlabel('Number Of Catch')
        st.pyplot(fig_caught_player)
    

        # All details Of Team1
        with st.container() : 
            txt1, txt2 = st.columns(2)
            with txt1 : 
                st.write(f"#### Team : {tm1}")
            with txt2 : 
                st.write(f"#### R / W / B : {tm1_details['total_run'].sum()} / {tm1_details['isWicketDelivery'].sum()} / {tm1_details.shape[0]}")


        no_of_player = 1
        y_label = ['Runs', 'Sixes', 'Fours', 'Balls/Runs', 'Wickets', 'Balls/Wickets', 'Runs/Wickets', 'Maiden', 'Catches']
        for plys in Team1_Team2[tm1] :
            x_label = []
            for typ in Team1_Team2[tm1][plys] : 
                if typ == 'wic' or typ == 'cau' : 
                    x_label.append(len(Team1_Team2[tm1][plys][typ]))
                else : 
                    x_label.append(int(Team1_Team2[tm1][plys][typ]))

            # for plot it
            fig_player, axis_player = plt.subplots()
            sns_obj_player = sns.barplot(x = x_label, y = y_label, ax=axis_player)
            sns_obj_player.bar_label(sns_obj_player.containers[0])
            axis_player.set_title(f"{no_of_player} - {plys} ({tm1})")
            axis_player.set_xlabel('Counts')
            st.pyplot(fig_player)
            # st.write(Team1_Team2[tm1][plys])
            st.markdown("""---""")
            no_of_player += 1


            # st.write(plys, x_label)
        # st.markdown("""---""")
        # st.markdown("""---""")
        with st.container() : 
            txt1, txt2 = st.columns(2)
            with txt1 : 
                st.write(f"#### Team : {tm2}")
            with txt2 : 
                st.write(f"#### R / W / B : {tm2_details['total_run'].sum()} / {tm2_details['isWicketDelivery'].sum()} / {tm2_details.shape[0]}")

        # for other team details
        no_of_player = 1
        for plys in Team1_Team2[tm2] :
            x_label = []
            for typ in Team1_Team2[tm2][plys] : 
                if typ == 'wic' or typ == 'cau' : 
                    x_label.append(len(Team1_Team2[tm2][plys][typ]))
                else : 
                    x_label.append(int(Team1_Team2[tm2][plys][typ]))

            # for plot it
            fig_player, axis_player = plt.subplots()
            sns_obj_player = sns.barplot(x = x_label, y = y_label, ax=axis_player)
            sns_obj_player.bar_label(sns_obj_player.containers[0])
            axis_player.set_title(f"{no_of_player} - {plys} ({tm1})")
            axis_player.set_xlabel('Counts')
            st.pyplot(fig_player)
            # st.write(Team1_Team2[tm1][plys])
            st.markdown("""---""")
            no_of_player += 1



        # st.write('Complete')
        # st.write(tm1)
        # st.write(Team1_Team2[tm1])
        



# <------------------Completed--------------------------->






# code for rotate x or y column text in any matplotlib or seaborn graph

# x = [1, 2, 3, 4]
# y = [1, 4, 9, 6]
# labels = ['Frogs', 'Hogs', 'Bogs', 'Slogs']

# fig, axis = plt.subplots()
# axis.plot(labels,y,'r-s')# axis.bar(label, y)
# # `ha` is just shorthand for horizontalalignment, which can also be used.
# for label in axis.get_xticklabels() : 
#     label.set_rotation(90)
#     label.set_ha('right')
# st.pyplot(fig)