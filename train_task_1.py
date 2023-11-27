from sklearn.model_selection import train_test_split, GridSearchCV
import pandas as pd
import xgboost as xgb
from sklearn.metrics import accuracy_score
from matplotlib import pyplot
from sklearn.preprocessing import LabelEncoder

df = pd.read_csv("cleaned_train.csv", low_memory=False)

train, test = train_test_split(df, test_size=0.1, random_state=69)

x_train = train.drop(columns="target")
y_train = train["target"]

x_test = test.drop(columns="target")
y_test = test["target"]

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
xgb_model.save_model("model.json")
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
pyplot.savefig("chart.jpg")