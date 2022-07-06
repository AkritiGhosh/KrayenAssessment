
import streamlit as st
import pandas as pd
import numpy as np

PAGE_CONFIG = {"page_title":"IPL EDA.io","page_icon":"chart_with_upwards_trend","layout":"centered"}
st.set_page_config(**PAGE_CONFIG)

hr = '''

----

'''

def fillna(matches, deliveries, df_eda):
  df_eda.loc[df_eda['venue'] == 'Dubai International Cricket Stadium', 'city'] = 'Dubai'
  matches.loc[matches['venue'] == 'Dubai International Cricket Stadium', 'city'] = 'Dubai'
  df_eda['winner'].fillna('Tie', inplace=True)
  matches['winner'].fillna('Tie', inplace=True)
  df_eda['player_dismissed'].fillna('None', inplace=True)
  deliveries['player_dismissed'].fillna('None', inplace=True)
  df_eda['dismissal_kind'].fillna('None', inplace=True)
  deliveries['dismissal_kind'].fillna('None', inplace=True)
  df_eda = df_eda.fillna('NA')


st.title("Krayen Assessment")
st.subheader('IPL EDA')
matches = pd.read_csv('/content/matches.csv')
deliveries = pd.read_csv('/content/deliveries.csv')
df_eda = pd.merge(deliveries,matches, left_on='match_id', right_on='id', how ='outer')
del df_eda['id']
del df_eda['umpire3']
del df_eda['result']
del df_eda['fielder']
st.write('The merged data set -')
st.write(df_eda.head())
fillna(matches, deliveries, df_eda)
st.write('After filling empty values - ',df_eda.head())
st.markdown(hr)
seasons = np.sort(matches.season.unique())
st.write('Seasons-', seasons)
teams = list(set(matches.team1.unique()) | set(matches.team2.unique()))
players = list(set(df_eda.batsman.unique()) | set(df_eda.bowler.unique()))
st.write('Teams-', teams)
st.subheader('Team Performance')
st.write('Matches won by teams - ',pd.Series(matches['winner'].value_counts(), name = 'Matches Win'))
winners = list(matches['winner'].unique())
st.markdown(hr)
st.write("No of teams who didn't win any game -", len(list(set(teams) - set(winners))))
st.markdown(hr)
total_win = pd.Series(matches['winner'].value_counts(), name = 'Matches Win')
team_play = {}
for i in teams:
  team_play[i] = int(matches['team1'].value_counts()[i]) + int(matches['team2'].value_counts()[i])
total_play = pd.Series(team_play, name = 'Matches Play')
team_score = pd.merge(total_play, total_win, right_index = True,
               left_index = True)
team_score['Win%'] = (team_score['Matches Win'] / team_score['Matches Play']) * 100
st.write('Stats for each team',team_score.sort_values('Win%', ascending=False))

st.subheader('Season Performance')
season_winners = []
season = st.select_slider(
     'Select an year',
     options=seasons)
st.write('Season - ', season)
st.write('Season winner - ', matches[matches['season']==season].iloc[-1,:].winner) 
season_winners.append(matches[matches['season']==season].iloc[-1,:].winner)
st.write('Total number of matches - ', matches[matches['season']==season]['id'].count())
st.write('Matches won - ')
st.write(matches[matches['season']==season]['winner'].value_counts())
st.write(hr)


st.subheader('Dismissal')
dms_player = df_eda[df_eda['player_dismissed'] != 'None'][['player_dismissed','dismissal_kind']].value_counts().to_frame().reset_index()
dms_player['count'] = dms_player[0]
del dms_player[0]

st.write('',dms_player)

player_name = st.selectbox(
     'Select a player',
     players)
dms_player[dms_player['player_dismissed'] == player_name]
st.write(hr)

st.subheader('Bowlers')
bowlers = df_eda['bowler'].unique()
bowler_dismiss = df_eda[df_eda['player_dismissed'] != 'None'][['bowler']].value_counts().to_frame().reset_index()
bowler_dismiss['count'] = bowler_dismiss[0]
del bowler_dismiss[0]
bowler_name = st.selectbox('Number of outs by a bowler', bowlers)
st.write(bowler_dismiss[bowler_dismiss['bowler']==bowler_name])
st.write(hr)

st.subheader('Deliveries')
run_types = ['wide_runs','bye_runs','legbye_runs','noball_runs', 'penalty_runs', 'batsman_runs','extra_runs']
run_type = st.selectbox('Select a category of run', run_types)
rtb = df_eda.groupby(['season','bowler'])[run_type].sum().reset_index().sort_values(run_type, ascending=False)
st.write(rtb[:1])
st.write(hr)

st.write('Which batsman has highest number of runs in all seasons')
st.write(deliveries.groupby(['batsman'])['total_runs'].sum().reset_index().sort_values('total_runs', ascending=False)[:1])
st.write(hr)
st.write('How many runs by a player(batsman) in a season were batsman runs')
bat_total = df_eda.groupby(['season','batsman'])[['batsman_runs','total_runs']].sum().reset_index()
bat_total['bat_runs_percent'] = (bat_total['batsman_runs'])/(bat_total['total_runs'])
player_name1 = st.selectbox('Select a player', players,key='p1')
bat_total = bat_total[bat_total['batsman'] == player_name1]
st.write(bat_total)
season1 = st.select_slider('Select an year', options=seasons,key='s1')
bat_total = bat_total[bat_total['season'] == season1]
st.write(bat_total)

st.write(hr)
st.write('Which batsman has highest number of runs in per seasons, and in what season')
st.write(df_eda.groupby(['season','batsman'])['total_runs'].sum().reset_index().sort_values('total_runs', ascending=False)[:1])

st.write(hr)
st.write('In which match, the highest number of runs were scored in an over')
highest_run_over = deliveries.groupby(['match_id','inning','over','batsman'])['total_runs'].sum().reset_index().sort_values('total_runs', ascending=False)[:1]
st.write(highest_run_over) 
cols = st.multiselect(
     'Information about the match to be displayed',
     matches.columns)
matchID = highest_run_over['match_id']
matches[(matches['id']==int(matchID))][cols]