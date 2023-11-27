import xgboost as xgb
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split


model= xgb.XGBClassifier()
model.load_model("model_task_3.json")

test = pd.read_csv("cleaned_test.csv", low_memory=False)

y_pred = model.predict_proba(test)
print(y_pred)
