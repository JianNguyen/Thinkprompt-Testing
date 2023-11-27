import pandas as pd
import numpy as np
from datetime import datetime
import json
from tqdm import tqdm
from sklearn.preprocessing import LabelEncoder

data = "test"

df = pd.read_csv(f"{data}.csv", low_memory=False)
f_id2name = open("id2name_league.json")
id2name = json.load(f_id2name)

# drop id, league_name, league_id, home_team_history_league_id, away_team_history_league_id cols
del df["id"]
del df["league_name"]
del df["league_id"]
for i in range(1, 11):
    del df[f"home_team_history_league_id_{i}"]
    del df[f"away_team_history_league_id_{i}"]
    del df[f"home_team_history_coach_{i}"]
    del df[f"away_team_history_coach_{i}"]
del df["home_team_name"]
del df["away_team_name"]
del df["home_team_coach_id"]
del df["away_team_coach_id"]
# check row have Nan value
is_have_nan = df.isnull().sum(axis=1).to_list()
for i in range(len(is_have_nan)):
    if is_have_nan[i] > 0:
        is_have_nan[i] = 1
# replace Nan value
df.fillna(value=-1, inplace=True)
# history match date to break time
home_team_match_date_current = []
away_team_match_date_current = []
for i in tqdm(range(len(df.index))):
    home_total = []
    away_total = []
    for site in list(["home", "away"]):
        for j in range(10, 0, -1):
            if df.iloc[i][f"{site}_team_history_match_date_{j}"] != -1:
                before = df.iloc[i][f"{site}_team_history_match_date_{j}"]
                t1 = datetime.strptime(before, '%Y-%m-%d %H:%M:%S')
                if j > 1:
                    after = df.iloc[i][f"{site}_team_history_match_date_{j-1}"]
                else:
                    after = df.iloc[i][f"match_date"]
                t2 = datetime.strptime(after, '%Y-%m-%d %H:%M:%S')
                time_date = t2 - t1
                num_day = time_date.days
                secs = time_date.seconds
                total = secs/3600/24 + num_day
                if site == "home":
                    home_total.append(total)
                elif site == "away":
                    away_total.append(total)
            else:
                if site == "home":
                    home_total.append(-1)
                elif site == "away":
                    away_total.append(-1)
    home_total.reverse()
    away_total.reverse()
    for j in range(1, 10):
        df.at[i, f"home_team_history_match_date_{j}"] = home_total[j]
        df.at[i, f"away_team_history_match_date_{j}"] = away_total[j]

    home_team_match_date_current.append(float(home_total[0]))
    away_team_match_date_current.append(float(away_total[0]))   

    # if i == 19:
    #     break

# df = df.head(20)

# drop home_team_history_match_date_10, match_daycol
del df["home_team_history_match_date_10"]
del df["away_team_history_match_date_10"]
del df["match_date"]
# change coach_id to str
df["is_cup"] = df["is_cup"].astype(str)
# df["away_team_coach_id"] = df["away_team_coach_id"].astype(str)
# for i in range(1, 11):
#     df[f"home_team_history_coach_{i}"] = df[f"home_team_history_coach_{i}"].astype(str)
#     df[f"away_team_history_coach_{i}"] = df[f"away_team_history_coach_{i}"].astype(str)
for i in range(1, 10):
    df[f"home_team_history_match_date_{i}"] = df[f"home_team_history_match_date_{i}"].astype("float64")
    df[f"away_team_history_match_date_{i}"] = df[f"away_team_history_match_date_{i}"].astype("float64")

# tokenize str
le = LabelEncoder()
is_category = df.dtypes == object
category_column = df.columns[is_category].to_list()
# print(category_column)
df[category_column] = df[category_column].apply(lambda col: le.fit_transform(col))
# add is_have_nan, home_team_match_date_current,  cols
data_join = dict()
# data_join["is_have_nan"] = is_have_nan[0:20]
data_join["is_have_nan"] = is_have_nan
data_join["home_team_match_date_current"] = home_team_match_date_current
data_join["away_team_match_date_current"] = away_team_match_date_current
df = pd.concat([df, pd.DataFrame(data_join)], axis=1)
df.to_csv(f"cleaned_{data}.csv", encoding='utf-8', index=False)
