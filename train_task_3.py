from sklearn.model_selection import train_test_split, GridSearchCV
import pandas as pd
import xgboost as xgb
from sklearn.metrics import accuracy_score
from matplotlib import pyplot
from sklearn.preprocessing import LabelEncoder
import json

def create_label_scores():
    result = dict()
    count = 1
    for i in range(6):
        for j in range(6):
            result[f'{i}-{j}'] = count
            count += 1
    result['other'] = 0
    with open("label_scores.json", "w") as outfile: 
        json.dump(result, outfile)

def create_cleaned_scores():
    df = pd.read_csv("cleaned_train.csv", low_memory=False)
    df_scores = pd.read_csv("train_target_and_scores.csv", low_memory=False)
    f = open("label_scores.json")
    labels = json.load(f)
    scores = df_scores['score'].to_list()

    for c, s in enumerate(scores):
        scores[c] = labels[s]

    df = df.drop(columns="target")
    data_join = dict()
    data_join["score"] = scores
    df = pd.concat([df, pd.DataFrame(data_join)], axis=1)
    df.to_csv(f"cleaned_scores.csv", encoding='utf-8', index=False)

df = pd.read_csv("cleaned_scores.csv", low_memory=False)

train, test = train_test_split(df, test_size=0.1, random_state=69)


x_train = train.drop(columns="score")
y_train = train["score"]

x_test = test.drop(columns="score")
y_test = test["score"]

eval_set = [(x_train, y_train), (x_test, y_test)]
#model

early_stop = xgb.callback.EarlyStopping(
    rounds=5, metric_name='mlogloss', data_name='validation_1', save_best=True
)
xgb_model = xgb.XGBClassifier(n_estimators=10000, learning_rate=0.005, max_depth=2, objective='binary:logistic')
# optimization_dict = {'max_depth': [2,4,6,8],
#                      'n_estimators': [50,100,150,200]}
# model = GridSearchCV(xgb_model, optimization_dict, 
#                      scoring='accuracy', verbose=1)

#eval_metric="mlogloss"
xgb_model.fit(x_train, y_train, eval_set=eval_set, verbose=True, callbacks=[early_stop])
xgb_model.save_model("model_score.json")
# make predictions for test data
y_pred = xgb_model.predict(x_test)
predictions = [round(value) for value in y_pred]
# evaluate predictions
accuracy = accuracy_score(y_test, predictions)
print("Accuracy: %.2f%%" % (accuracy * 100.0))
# retrieve performance metrics
results = xgb_model.evals_result()
epochs = len(results['validation_0']['mlogloss'])
x_axis = range(0, epochs)
# plot log loss
fig, ax = pyplot.subplots()
ax.plot(x_axis, results['validation_0']['mlogloss'], label='Train')
ax.plot(x_axis, results['validation_1']['mlogloss'], label='Test')
ax.legend()
pyplot.ylabel('Log Loss')
pyplot.title('XGBoost Log Loss')
pyplot.savefig("chart_task_3.jpg")