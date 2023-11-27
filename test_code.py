from sklearn.model_selection import train_test_split, GridSearchCV
import pandas as pd
import xgboost as xgb
from sklearn.metrics import accuracy_score
from matplotlib import pyplot
from sklearn.preprocessing import LabelEncoder
import json



df = pd.read_csv("cleaned_train.csv", low_memory=False)
df_scores = pd.read_csv("train_target_and_scores.csv", low_memory=False)
f = open("label_scores.json")
labels = json.load(f)
scores = df_scores['score'].to_list()

for c, s in enumerate(scores):
    if s in labels.keys():
        scores[c] = labels[s]
    else:
        scores[c] = 0

df = df.drop(columns="target")
data_join = dict()
data_join["score"] = scores
df = pd.concat([df, pd.DataFrame(data_join)], axis=1)
df.to_csv(f"cleaned_scores.csv", encoding='utf-8', index=False)

# df = df.drop(columns="target")
# data_join = dict()
# data_join["score"] = df_scores['score']
# df = pd.concat([df, pd.DataFrame(data_join)], axis=1)
# df.to_csv(f"cleaned_score.csv", encoding='utf-8', index=False)