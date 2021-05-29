import requests
import pandas as pd

username='DanielCondeOrtiz'
git_token='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'
github_data = []

#url = "https://api.github.com/search/repositories"
url = "https://api.github.com/search/repositories?q=stars:>500&page=1&per_page=100"
res=requests.get(url,auth=(username,git_token))

#repos=res.json()
i=0
while 'next' in res.links.keys():
    for repo in res.json()["items"]:
        repo_name = repo['name']
        owner = repo['owner']['login']
        repo_info = requests.get('https://api.github.com/repos/'+owner+'/'+repo_name, auth=(username,git_token))
        if repo_info.status_code == 200 and repo_info.json()["stargazers_count"] >= 50:
            print(repo_info, i, repo_info.json()["stargazers_count"])
            github_data.append(repo_info.json())
            i += 1
        else:
            #print("PUPU", repo_info, i, repo_info.json()["stargazers_count"])
            print("PUPU")
        if (i > 999):
            break
    if (i > 999):
            break
    
    res=requests.get(res.links['next']['url'],auth=(username,git_token))
    #repos.extend(res.json())

df = pd.DataFrame(github_data).to_csv("new_dataset_more_than_500.csv")
