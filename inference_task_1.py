import xgboost as xgb
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split


model= xgb.XGBClassifier()
model.load_model("model_task_1.json")

test = pd.read_csv("cleaned_test.csv", low_memory=False)
df = pd.read_csv("test.csv", low_memory=False)
df = df["id"]
away_list = []
draw_list = []
home_list = []

y_pred = model.predict_proba(test)
for y in y_pred:
    away_list.append(y[0])
    draw_list.append(y[1])
    home_list.append(y[2])
data_join = dict()
data_join['home'] = home_list
data_join['draw'] = draw_list
data_join['away'] = away_list

df = pd.concat([df, pd.DataFrame(data_join)], axis=1)

df.to_csv(f"out.csv", encoding='utf-8', index=False)
# predictions = [round(value) for value in y_pred]
# accuracy = accuracy_score(y_test, predictions)
# print(accuracy)
