import pickle
import numpy as np
import pandas as pd
def get_regressor():
    # Load the Random Forest CLassifier model
    regressor = pickle.load(open('src/first-innings-score-lr-model.pkl', 'rb'))
    return regressor

def predict_final_score(request):
    # To predict the final score.
    temp_array = list()
    batting_team = request.form['batting-team']
    bowling_team = request.form['bowling-team']
    venue = request.form['venue']
    team_array = ['CSK', 'DD', 'KXP', 'KKR', 'MI', 'RR', 'RCB', 'SRH']
    temp_array = [ 1 if batting_team == team_array[i] else 0 for i in range(len(team_array))]
    print(temp_array)

    temp_array += [ 1 if bowling_team == team_array[i] else 0 for i in range(len(team_array))]
    print('now', temp_array)
        
    overs = float(request.form['overs'])
    runs = int(request.form['runs'])
    wickets = int(request.form['wickets'])
    runs_in_prev_5 = int(request.form['runs_in_prev_5'])
    wickets_in_prev_5 = int(request.form['wickets_in_prev_5'])
    
    temp_array += [overs, runs, wickets, runs_in_prev_5, wickets_in_prev_5]
    
    data = np.array([temp_array])
    regressor = get_regressor()
    final_score = int(regressor.predict(data)[0])
    return final_score

def get_teams():
    teams = {"MI":  "Mumbai Indians", "DD":  "Delhi Daredevils",
             "CSK":  "Chennai Super Kings", "RCB":  "Royal Challengers Bangalore",
             "KKR":  "Kolkata Knight Riders","RR":  "Rajasthan Royals",
             "KXP":  "Kings XI Punjab", "SRH":  "Sunrisers Hyderabad",
             "all": "all_teams"}
    return teams

def get_venues():
    venues = {"Mumbai":  "Mumbai", "Kolkata":  "Kolkata",
              "Chennai":  "Chennai", "Jaipur":  "Jaipur",
              "Mohali":  "Mohali", "Bangalore":  "Banglore",
              "Delhi":  "Delhi" ,"Hyderabad":  "Hyderabad"}
    return venues

def get_all_venues():
    df = pd.read_csv('static/data/match.csv')
    df1 = df["Venue_Name"].unique()
    df2 = df1.tolist()
    df3 = []
    for ele in df2:
        if type(ele) == str:
            df3.append(ele)
    df3.sort()
    return df3

def get_match_record(teams_key):
    df = pd.read_csv('static/data/match.csv')
    if (teams_key != "all"):
        team_name = get_teams()
        team_name = team_name[teams_key]
        df = df[df["Team1"] == team_name]
    df.drop(['City_Name', 'Country_Name', 'Outcome_Type', 'id'], axis=1, inplace=True)
    df.reset_index()
    return df

def get_toss_data(venue_name):
    df = pd.read_csv('static/data/match.csv')
    df1 = df[(df["Venue_Name"] == venue_name)]
    df2 = df1[['Toss_Winner', 'match_winner', 'Toss_Name']]
    total = len(df2)

    df3 = df2[(df2["Toss_Winner"] == df2["match_winner"])&(df2["Toss_Name"] == "field")]
    df4 = df2[(df2["Toss_Winner"] != df2["match_winner"])&(df2["Toss_Name"] == "bat")]
    
    field_win = len(df3.index) + len(df4.index)

    df5 = df2[(df2["Toss_Winner"] == df2["match_winner"])&(df2["Toss_Name"] == "bat")]
    df6 = df2[(df2["Toss_Winner"] != df2["match_winner"])&(df2["Toss_Name"] == "field")]
    bat_win = len(df4.index) + len(df6.index)
    message = ""
    draw = ((total - field_win + bat_win)/total)*100
    if field_win>bat_win:
        message = "Choose Fielding as There are " + str(round(((field_win/(field_win+bat_win))*100), 2)) + "% Chance of Winning."
    else:
        message = "Choose Batting as There are " + str(round(((bat_win/(field_win+bat_win))*100), 2)) + "% Chance of Winning."

    data = {
            "field_win": field_win,
            "bat_win": bat_win, 
            "total": total, 
            "no_result": total - (field_win + bat_win),
            "message": message,
            "field_win_percent": round((field_win/(field_win+bat_win))*100, 2),
            "bat_win_percent": round((bat_win/(field_win+bat_win))*100, 2),
            }
    return data

def get_average_scores():
    df = pd.read_csv('static/data/ipl.csv')
    df1 = df[["venue", "total"]]
    grouped_df = df1.groupby("venue")
    mean_df = grouped_df.mean()
    mean_df = mean_df.reset_index()
    return mean_df





