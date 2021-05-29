from celery import Celery
from sklearn.metrics import r2_score, mean_squared_error
from sklearn import preprocessing
import pickle
import pandas as pd
import time
import numpy as np

data_file = 'final_dataset.csv'

# Celery configuration
CELERY_BROKER_URL = 'amqp://rabbitmq:rabbitmq@rabbit:5672/'
CELERY_RESULT_BACKEND = 'rpc://'

# Initialize Celery
celery = Celery('workerA', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)

def load_data():
    df =  pd.read_csv(data_file, delimiter=',')

    # df = df.drop_duplicates(subset=['id'])
    # #df = df.head()
    # X = df[["size", "forks_count", "open_issues_count", "subscribers_count"]]
    # #X["created_at"] = pd.to_datetime(X["created_at"]).astype(int) / 10**9

    # # Normalizing the rows
    # X = X.values
    # min_max_scaler = preprocessing.MinMaxScaler()
    # X = min_max_scaler.fit_transform(X)
    # X = pd.DataFrame(X)
    # y = df[["stargazers_count"]]

    #drop duplicates using the id
    df = df.drop_duplicates(subset=['id'])
    X = df[[ "created_at" , "size", "forks_count", "open_issues_count", "subscribers_count", "has_issues", "has_projects","has_pages"]]
    #created_at returns utc time and we need float
    X["created_at"] = pd.to_datetime(X["created_at"]).astype(int) / 10**9
    y = df[["stargazers_count"]]
    return X, y

def load_model():
    bagging = pickle.load(open('bagging_regressor.sav', 'rb'))
    grad_boost = pickle.load(open('gradientboosting_regressor.sav', 'rb'))
    neural_network = pickle.load(open('nn_regressor.sav', 'rb'))
    #svm = pickle.load(open('svm_regressor.sav', 'rb'))
    voting = pickle.load(open('voting_regressor.sav', 'rb'))
    return bagging, grad_boost, neural_network, voting

@celery.task
def get_predictions():
    X = load_data()[0]
    bagging, grad_boost, neural_network, voting = load_model()

    pred_bagging = bagging.predict(X)
    pred_grad_boost = grad_boost.predict(X)
    pred_neural_network = neural_network.predict(X)
    #pred_svm = svm.predict(X)
    pred_voting = voting.predict(X)
    return pred_bagging, pred_grad_boost, pred_neural_network, pred_voting

@celery.task
def get_metrics():
    start_time = time.time()
    y = load_data()[1]
    predictions = list(get_predictions())
    r2, mse = [], []

    for i in range(len(predictions)):
        #print(predictions[i])
        r2.append(np.round(r2_score(y, predictions[i]), 3))
        mse.append(np.round(mean_squared_error(y, predictions[i]), 3))
    #print(r2, mse)
    time_elapsed = time.time() - start_time
    print(f'Elapsed time: {np.round(time_elapsed, 2)} seconds')
    return r2, mse