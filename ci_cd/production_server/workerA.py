from celery import Celery
from sklearn.metrics import r2_score, mean_squared_error
from sklearn import preprocessing
import pickle
import pandas as pd
import time
import numpy as np

data_file = 'final_dataset_predict.csv'

# Celery configuration
CELERY_BROKER_URL = 'amqp://rabbitmq:rabbitmq@rabbit:5672/'
CELERY_RESULT_BACKEND = 'rpc://'

# Initialize Celery
celery = Celery('workerA', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)

def load_data():
    df =  pd.read_csv(data_file, delimiter=',')

    #drop duplicates using the id
    df = df.drop_duplicates(subset=['id'])
    X = df[[ "created_at" , "size", "forks_count", "open_issues_count", "subscribers_count", "has_issues", "has_projects","has_pages"]]
    #created_at returns utc time and we need float
    X["created_at"] = pd.to_datetime(X["created_at"]).astype(int) / 10**9
    y = df[["stargazers_count"]]
    info =  df[["name","stargazers_count","forks_count", "subscribers_count"]]
    return X, y, info

def load_model():
    bagging = pickle.load(open('bagging_regressor.sav', 'rb'))
    grad_boost = pickle.load(open('gradientboosting_regressor.sav', 'rb'))
    neural_network = pickle.load(open('nn_regressor.sav', 'rb'))
    voting = pickle.load(open('voting_regressor.sav', 'rb'))
    tree = pickle.load(open('tree_regressor.sav', 'rb'))
    random_forest = pickle.load(open('randomForest_regressor.sav', 'rb'))
    return bagging, grad_boost, neural_network, voting, tree, random_forest

@celery.task
def get_predictions():
    X = load_data()[0]
    bagging, grad_boost, neural_network, voting, tree, random_forest = load_model()

    pred_bagging = bagging.predict(X)
    pred_grad_boost = grad_boost.predict(X)
    pred_neural_network = neural_network.predict(X)
    pred_voting = voting.predict(X)
    pred_tree = tree.predict(X)
    pred_random_forest = random_forest.predict(X)
    return pred_bagging, pred_grad_boost, pred_neural_network, pred_voting, pred_tree, pred_random_forest

@celery.task
def get_metrics():
    start_time = time.time()
    X,y,info = load_data()
    predictions = list(get_predictions())
    r2 = []

    for i in range(len(predictions)):
        #print(predictions[i])
        r2.append(np.round(r2_score(y, predictions[i]), 3))
    
    #Take the predictions of the best performance method (bagging)
    pred_boosting = predictions[1]
    #top 5 highest values from the stars predictions
    index = np.argpartition(pred_boosting,-5)[-5:]
    index = index[::-1]
    top_predicted_stars = np.partition(pred_boosting,-5)[-5:]
    top_predicted_stars = top_predicted_stars[::-1]

    #dataframe to array
    info = info.values
    
    #top_repos: name, predicted_stars, real_Stars, forks, subscribers
    top_repos = []
    for i in range(len(index)):
        top_repos.append([info[index[i],0], top_predicted_stars[i], info[index[i],1], info[index[i],2], info[index[i],3]])


    #print(top_repos[0][0])
    #print(top_repos[0][1])
    #print(top_repos[0][2])
    #print(top_repos[0][3]) 
    #print(top_repos[0][4])
    time_elapsed = time.time() - start_time
    print(f'Elapsed time: {np.round(time_elapsed, 2)} seconds')

    return r2,top_repos, time_elapsed

#get_metrics()
