from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.ensemble import GradientBoostingRegressor
import numpy as np
import csv
import pandas as pd
import pickle
from os import path

# reading the csv file using read_csv
# storing the data frame in variable called df

basepath = path.dirname(__file__)
df = pd.read_csv(basepath + '/datasets/final_dataset_train.csv')


# creating a list of column names by calling the .columns
#features = list(df.columns)

'''
print("Features : ", features)
Features :  ['Unnamed: 0', 'id', 'node_id', 'name', 'full_name', 'private', 'owner', 'html_url', 'description', 'fork', 'url', 'forks_url', 'keys_url',
'collaborators_url', 'teams_url', 'hooks_url', 'issue_events_url', 'events_url', 'assignees_url', 'branches_url', 'tags_url', 'blobs_url', 'git_tags_url',
'git_refs_url', 'trees_url', 'statuses_url', 'languages_url', 'stargazers_url', 'contributors_url', 'subscribers_url', 'subscription_url', 'commits_url',
'git_commits_url', 'comments_url', 'issue_comment_url', 'contents_url', 'compare_url', 'merges_url', 'archive_url', 'downloads_url', 'issues_url',
'pulls_url', 'milestones_url', 'notifications_url', 'labels_url', 'releases_url', 'deployments_url', 'created_at', 'updated_at', 'pushed_at', 'git_url', 
'ssh_url', 'clone_url', 'svn_url', 'homepage', 'size', 'stargazers_count', 'watchers_count', 'language', 'has_issues', 'has_projects', 'has_downloads', 
'has_wiki', 'has_pages', 'forks_count', 'mirror_url', 'archived', 'disabled', 'open_issues_count', 'license', 'forks', 'open_issues', 'watchers', 
'default_branch', 'permissions', 'temp_clone_token', 'network_count', 'subscribers_count', 'organization', 'parent', 'source']
'''
#drop duplicates using the id
df = df.drop_duplicates(subset=['id'])
print(df)
#watchers_count is the same than strargazers_count so we can`t use it
#network_count is the same than forks_count

features_selected = df[[ "created_at" , "size", "forks_count", "open_issues_count", "subscribers_count", "has_issues", "has_projects","has_pages"]]
#created_at returns utc time and we need float
features_selected["created_at"] = pd.to_datetime(features_selected["created_at"]).astype(int) / 10**9
target = df[["stargazers_count"]]

#print(features_selected)


#X_train, X_test, y_train, y_test = train_test_split(features_selected, target.values.ravel(), test_size=0.2, random_state=1)


gradBost = GradientBoostingRegressor().fit(features_selected,  target.values.ravel())
#score = gradBost.score(X_test,y_test)

# Score returns the coefficient of determination R^2 of the prediction
#print(score)

pickle.dump(gradBost, open(basepath + '/models/gradientboosting_regressor.sav', 'wb'))
