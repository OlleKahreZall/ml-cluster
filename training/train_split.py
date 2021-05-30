from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.ensemble import BaggingRegressor

import csv
import pandas as pd
import pickle
from os import path

# reading the csv file using read_csv
# storing the data frame in variable called df
basepath = path.dirname(__file__)
df = pd.read_csv(basepath + 'datasets/final_dataset.csv')
df = df.drop_duplicates(subset=['id'])


features_selected = df[[ "created_at" , "size", "forks_count", "open_issues_count", "subscribers_count", "has_issues", "has_projects","has_pages"]]
#created_at returns utc time and we need float
features_selected["created_at"] = pd.to_datetime(features_selected["created_at"]).astype(int) / 10**9
target = df[["stargazers_count"]]

X_train, X_test, y_train, y_test = train_test_split(features_selected, target.values.ravel(), test_size=0.2, random_state=1)

test = pd.concat([X_train, y_train], axis=1)
train = pd.concat([X_test, y_test], axis=1)
