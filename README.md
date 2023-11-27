# Thinkprompt-Testing
Tested on ubuntu 20.4(LTS)
# Guide line
## Python 3.8 version 
## Env
  pip install -r requirements.txt
## Task 1
The result is **sample_submission.csv** file
## Task 2
The result is **task_2.py**
Run task_2.py and input name of two teams
## Task 3
Idea: train a model with output is the score. In my case i will label for 
{“0-0”: 0 , “0-1”: 1,... }. You can refer at **label_scores.json** for my own label rules 
I trained with XGboost model. You can load **model_task_3.json** for inference(refer at **inference_task_3.py**).
<br>
_Note: Use predict_proba() to see capabilities for labels_

## Others
Because the large limit on git have to lower than 100MB. You can refer files that i processed at [here](https://drive.google.com/drive/folders/1aNV8YyBJ1OmeWp6lpNo7CHp_pmryW1HN?usp=sharing)

