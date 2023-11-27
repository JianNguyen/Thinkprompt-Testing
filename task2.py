import pandas as pd
import numpy as np
from datetime import datetime
import json
from tqdm import tqdm


def create_history_team():
    df = pd.read_csv(f"train.csv", low_memory=False)
    df.fillna(value=-1, inplace=True)

    teams_history = dict()

    for i in tqdm(range(len(df.index))):
        for x in ["home", "away"]:
            team = df.iloc[i][f'{x}_team_name']
            if  team not in teams_history.keys():
                teams_history[team] = []

                value = dict()
                value['match_date'] = df.iloc[i]['match_date']
                value['league_id'] = int(df.iloc[i]['league_id'])
                teams_history[team].append(value)

                for j in range(1, 11):
                    if df.iloc[i][f'{x}_team_history_match_date_{j}'] != -1:
                        value = dict()
                        value[f'match_date'] = df.iloc[i][f'{x}_team_history_match_date_{j}']
                        value['league_id'] = int(df.iloc[i][f'{x}_team_history_league_id_{j}'])
                        teams_history[team].append(value)


            elif team in teams_history.keys():
                add_current_date = True
                for ele in teams_history[team]:
                    if df.iloc[i]['match_date'] == ele['match_date']:
                        add_current_day = False
                        break
                if add_current_date:
                    value = dict()
                    value['match_date'] = df.iloc[i]['match_date']
                    value['league_id'] = int(df.iloc[i]['league_id'])
                
                for j in range(1, 11):
                    add_history_day_id = True
                    for ele in teams_history[team]:
                        if df.iloc[i][f'{x}_team_history_match_date_{j}'] == ele['match_date']:
                            add_history_day_id = False
                            break
                    if add_history_day_id:
                        value = dict()
                        value['match_date'] = df.iloc[i][f'{x}_team_history_match_date_{j}']
                        value['league_id'] = int(df.iloc[i][f'{x}_team_history_league_id_{j}'])

    with open("teams_history.json", "w") as outfile: 
            json.dump(teams_history, outfile, ensure_ascii=False)

def create_id2name_league():
    file = open("name2id_league.json")
    data = json.load(file)
    id_ = dict()
    for key in data.keys():
        for x in data[key]:
            if x not in id_.keys():
                id_[f"{x}"] = key

    with open("id2name_league.json", "w") as outfile: 
        json.dump(id_, outfile)


def create_name2id_league():
    df = pd.read_csv("train.csv", low_memory=False)
    league_df = df[["league_name", "league_id"]]
    league_name = dict()
    for i in range(len(league_df)):
        if league_df.iloc[i]["league_name"] not in league_name.keys():
            li = []
            li.append(str(league_df.iloc[i]["league_id"]))
            league_name[f'{league_df.iloc[i]["league_name"]}'] = li
        else:
            li = league_name[f'{league_df.iloc[i]["league_name"]}']
            if str(league_df.iloc[i]["league_id"]) not in league_name[f'{league_df.iloc[i]["league_name"]}']:
                li.append(str(league_df.iloc[i]["league_id"]))
                league_name[f'{league_df.iloc[i]["league_name"]}'] = li

    with open("league_name.json", "w") as outfile: 
        json.dump(league_name, outfile)

if __name__ == '__main__':
    f = open("teams_history.json")  # created by create_history_team function
    data = json.load(f)
    f1 = open("id2name_league.json")    # created by create_id2name_league function
    id2name = json.load(f1)

    print("Input team name 1: ")
    team_1 = input()
    print("Input team name 2: ")
    team_2 = input()
    
    result = []
    for his_1 in data[team_1]:
        for his_2 in data[team_2]:
            id_1 = his_1['league_id']
            id_2 = his_2['league_id']
            if his_1['match_date'] == his_2['match_date'] and id2name[f'{id_1}'] == id2name[f'{id_2}']:
                value = dict()
                value['match_date'] = his_1['match_date']
                value['league_name'] = id2name[f'{id_1}']
                result.append(value)

    if result:
        if len(result) > 1:
            min = result[0]
            for k in range(len(result)):
                for i in range(1, len(result) - 1):
                    if datetime.strptime(result[i]['match_date'], '%Y-%m-%d %H:%M:%S') < datetime.strptime(min['match_date'], '%Y-%m-%d %H:%M:%S'):
                        min = result[i]
                        result[i] = result[i-1]
                        result[i-1] = min

        print("Last match between two teams:")
        if len(result) > 5:
            for re in result[:5]:
                print(f"Match date: {re['match_date']} --- League name: {re['league_name']}\n")
        else:
            for re in result:
                print(f"Match date: {re['match_date']} --- League name: {re['league_name']}\n") 
    else:
        print("No history match between two teams")